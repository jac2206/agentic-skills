// Optional real-browser checks. Reuse host tooling; never install dependencies.
import test from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { sampleReview, fingerprint } from './fixtures.mjs';
import { writeReport, cleanupReview } from '../report.mjs';
import { importDecisions } from '../model.mjs';

test('Offline Chromium: filters, navigation, diff comments, decisions/export, CSP and responsive themes', {
  skip: !process.env.CODE_REVIEW_PLAYWRIGHT || !process.env.CODE_REVIEW_BROWSER ? 'Existing Playwright entry and browser paths not supplied' : false,
  timeout: 90_000
}, async () => {
  const { chromium } = await import(pathToFileURL(process.env.CODE_REVIEW_PLAYWRIGHT).href);
  const { fixture, data } = sampleReview();
  const injection = '</script><img src="https://invalid.example/collect" onerror="globalThis.pwned=1">';
  data.findings[1].title = injection; data.snapshot.files[0].diffs[0].rows[1].text += injection;
  const before = fingerprint(fixture.root), out = writeReport(data, { json: true, markdown: true });
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.CODE_REVIEW_BROWSER, headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, offline: true, acceptDownloads: true });
    const page = await context.newPage();
    const errors = [], network = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => { if (/^https?:/.test(request.url())) network.push(request.url()); });
    await page.goto(pathToFileURL(out.report).href);
    await page.locator('.finding').first().waitFor();
    assert.equal(await page.locator('.finding').count(), 2);
    assert.equal(await page.evaluate(() => globalThis.pwned), undefined); assert.equal(await page.locator('img').count(), 0);
    assert.equal(await page.locator('#metrics .metric strong').first().textContent(), '80%');
    await page.selectOption('#severity', 'High'); assert.equal(await page.locator('.finding').count(), 1);
    await page.selectOption('#severity', ''); await page.selectOption('#category', 'testing'); assert.equal(await page.locator('.finding').count(), 1);
    await page.selectOption('#category', ''); await page.fill('#search', 'Permission predicate accepts'); assert.equal(await page.locator('.finding').count(), 1);
    await page.fill('#search', '');
    await page.getByRole('button', { name: 'new.js', exact: false }).first().click(); assert.equal(await page.locator('#file-title').textContent(), 'new.js');
    await page.getByRole('button', { name: 'auth.js', exact: false }).first().click();
    assert.equal(await page.locator('.diff-table.split').count(), 1); assert(await page.locator('.diff-table .add').count() > 0);
    assert(await page.locator('.diff-table .delete').count() > 0);
    await page.selectOption('#diff-mode', 'unified'); assert.equal(await page.locator('.diff-table.unified').count(), 1);
    await page.locator('.comment button').first().click(); assert.equal(await page.locator('.finding.highlight').count(), 1);
    const first = page.locator('[data-finding-id="F1"]');
    await first.getByRole('button', { name: 'Reject with reason' }).click();
    assert.match(await first.locator('p').last().textContent(), /pending/);
    await first.getByRole('textbox').fill('Fixture policy already handled elsewhere');
    await first.getByRole('button', { name: 'Reject with reason' }).click();
    await first.getByRole('textbox').fill('');
    await page.getByRole('button', { name: 'Copy decisions for Codex' }).click();
    assert.match(await page.locator('#notice').textContent(), /rejection reason/);
    await first.getByRole('textbox').fill('Fixture policy already handled elsewhere');
    await page.locator('[data-finding-id="F2"]').getByRole('button', { name: 'Defer', exact: true }).click();
    await page.selectOption('#decision-filter', 'rejected'); assert.equal(await page.locator('.finding').count(), 1);
    await page.selectOption('#decision-filter', '');
    await first.getByRole('button', { name: 'Accept recommendation' }).click();
    assert.match(await page.locator('#decision-summary').textContent(), /1 accepted.*1 deferred/);
    // Force clipboard restrictions to exercise the visible copy fallback.
    await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', { value: undefined, configurable: true }));
    await page.getByRole('button', { name: 'Copy decisions for Codex' }).click();
    await page.locator('#transfer:not([hidden])').waitFor();
    const payload = JSON.parse(await page.locator('#transfer-text').inputValue());
    assert.equal(importDecisions(data, payload).decisions[0].status, 'accepted'); assert.equal(payload.decisions[1].status, 'deferred');
    const download = page.waitForEvent('download'); await page.getByRole('button', { name: 'Export decisions JSON' }).click();
    const exported = await download; assert.deepEqual(JSON.parse(readFileSync(await exported.path(), 'utf8')), payload);
    await page.getByRole('button', { name: 'Copy manual commands' }).click();
    assert.match(await page.locator('#transfer-text').inputValue(), /git --literal-pathspecs add -- 'auth.js'/);
    await page.selectOption('#diff-mode', 'split'); await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: join(out.directory, 'desktop.png') });
    await page.locator('#workspace').screenshot({ path: join(out.directory, 'workspace.png') });
    await page.getByRole('button', { name: 'Light theme' }).click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
    await page.setViewportSize({ width: 390, height: 844 }); await page.selectOption('#diff-mode', 'unified'); await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: join(out.directory, 'mobile.png') });
    await page.locator('#workspace').screenshot({ path: join(out.directory, 'mobile-workspace.png') });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    const contrasts = await page.evaluate(() => {
      const style = getComputedStyle(document.documentElement);
      const luminance = hex => {
        const v = hex.trim().replace('#', '').match(/../g).map(x => parseInt(x, 16) / 255).map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4);
        return .2126 * v[0] + .7152 * v[1] + .0722 * v[2];
      };
      return ['text', 'muted', 'primary', 'error', 'success', 'warning'].map(name => {
        const a = luminance(style.getPropertyValue(`--${name}`)), b = luminance(style.getPropertyValue('--surface'));
        return [name, (Math.max(a, b) + .05) / (Math.min(a, b) + .05)];
      });
    });
    assert(contrasts.every(([, ratio]) => ratio >= 4.5), JSON.stringify(contrasts));
    await page.getByRole('button', { name: 'Dark theme' }).click();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []); assert.deepEqual(network, []); assert.equal(fingerprint(fixture.root), before);
    console.log(JSON.stringify({ browser: await browser.version(), report: out.report, screenshots: ['desktop.png', 'workspace.png', 'mobile.png', 'mobile-workspace.png'], lightTextContrast: contrasts }));
  } finally {
    if (browser) await browser.close(); fixture.close();
    if (process.env.CODE_REVIEW_KEEP_REPORT !== '1') cleanupReview({ ...out, confirmed: true });
  }
});

test('Spanish report preserves decision payload and English commit message', {
  skip: !process.env.CODE_REVIEW_PLAYWRIGHT || !process.env.CODE_REVIEW_BROWSER ? 'Existing Playwright entry and browser paths not supplied' : false,
  timeout: 90_000
}, async () => {
  const { chromium } = await import(pathToFileURL(process.env.CODE_REVIEW_PLAYWRIGHT).href);
  const { fixture, data } = sampleReview();
  const out = writeReport(data, { locale: 'es', json: true });
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.CODE_REVIEW_BROWSER, headless: true });
    const context = await browser.newContext({ offline: true, acceptDownloads: true });
    const page = await context.newPage();
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(out.report).href);
    await page.getByRole('heading', { name: 'Hallazgos y recomendaciones' }).waitFor();
    assert.equal(await page.locator('html').getAttribute('lang'), 'es');
    assert.equal(await page.locator('.finding').count(), 2);
    await page.selectOption('#severity', 'High'); assert.equal(await page.locator('.finding').count(), 1);
    await page.selectOption('#severity', '');
    await page.locator('[data-finding-id="F1"]').getByRole('button', { name: 'Aceptar recomendación' }).click();
    await page.locator('[data-finding-id="F2"]').getByRole('button', { name: 'Posponer', exact: true }).click();
    const download = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Exportar decisiones en JSON' }).click();
    const payload = JSON.parse(readFileSync(await (await download).path(), 'utf8'));
    assert.equal(importDecisions(data, payload).decisions[0].status, 'accepted');
    assert.equal(payload.decisions[1].status, 'deferred');
    assert.match(await page.locator('#commit-content').textContent(), /fix\(auth\): restore caller permission check/);
    assert.deepEqual(errors, []);
  } finally {
    if (browser) await browser.close(); fixture.close(); cleanupReview({ ...out, confirmed: true });
  }
});
