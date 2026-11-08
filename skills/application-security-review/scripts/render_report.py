#!/usr/bin/env python3
"""Validate canonical security review JSON and render Markdown/HTML reports."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse


SEVERITIES = {"Critical", "High", "Medium", "Low", "Informational"}
STATUSES = {"Open", "In Progress", "Resolved", "Accepted Risk", "False Positive"}
CONTROL_STATUSES = {"Passed", "Finding", "Not Assessed", "Not Applicable"}
MODES = {"Analyze", "Review", "Audit", "Remediation"}
COMPLETIONS = {"Complete", "Partial"}
ID_PATTERN = re.compile(r"^SEC-\d{3,}$")
REVIEW_ID_PATTERN = re.compile(r"^SEC-REVIEW-[A-Za-z0-9._-]+$")


class InputError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InputError(message)


def nonempty(value: Any, field: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{field} must be a non-empty string")
    return value.strip()


def valid_date(value: Any, field: str, optional: bool = False) -> str:
    if optional and value == "":
        return ""
    text = nonempty(value, field)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise InputError(f"{field} must use YYYY-MM-DD") from exc
    require(len(text) == 10, f"{field} must use YYYY-MM-DD")
    return text


def string_list(value: Any, field: str) -> list[str]:
    require(isinstance(value, list), f"{field} must be an array")
    return [nonempty(item, f"{field}[]") for item in value]


def validate(data: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    require(isinstance(data, dict), "root must be an object")
    review = data.get("review")
    findings = data.get("findings")
    require(isinstance(review, dict), "review must be an object")
    require(isinstance(findings, list), "findings must be an array containing the complete known register")

    review_id = nonempty(review.get("id"), "review.id")
    require(REVIEW_ID_PATTERN.fullmatch(review_id) is not None, "review.id must start with SEC-REVIEW-")
    valid_date(review.get("date"), "review.date")
    require(review.get("mode") in MODES, f"review.mode must be one of {sorted(MODES)}")
    require(review.get("completion") in COMPLETIONS, f"review.completion must be one of {sorted(COMPLETIONS)}")
    for field in ("title", "target", "summary"):
        nonempty(review.get(field), f"review.{field}")
    for field in ("scope", "exclusions", "methodology", "standards", "limitations", "related_artifacts", "history"):
        string_list(review.get(field), f"review.{field}")
    require(isinstance(review.get("controls_reviewed"), list), "review.controls_reviewed must be an array")
    for index, control in enumerate(review["controls_reviewed"]):
        prefix = f"review.controls_reviewed[{index}]"
        require(isinstance(control, dict), f"{prefix} must be an object")
        nonempty(control.get("name"), f"{prefix}.name")
        require(control.get("status") in CONTROL_STATUSES, f"{prefix}.status is invalid")
        for field in ("evidence", "notes"):
            require(isinstance(control.get(field), str), f"{prefix}.{field} must be a string")

    ids: set[str] = set()
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        require(isinstance(finding, dict), f"{prefix} must be an object")
        finding_id = nonempty(finding.get("id"), f"{prefix}.id")
        require(ID_PATTERN.fullmatch(finding_id) is not None, f"{prefix}.id must match SEC-###")
        require(finding_id not in ids, f"duplicate finding id: {finding_id}")
        ids.add(finding_id)
        for field in ("title", "category", "location", "evidence", "evidence_type", "description", "scenario", "impact", "likelihood", "recommendation", "mitigation", "review_id"):
            nonempty(finding.get(field), f"{prefix}.{field}")
        require(finding.get("severity") in SEVERITIES, f"{prefix}.severity is invalid")
        require(finding.get("status") in STATUSES, f"{prefix}.status is invalid")
        valid_date(finding.get("detected_date"), f"{prefix}.detected_date")
        valid_date(finding.get("resolution_date"), f"{prefix}.resolution_date", optional=True)
        require(isinstance(finding.get("references"), list), f"{prefix}.references must be an array")
        for ref_index, reference in enumerate(finding["references"]):
            require(isinstance(reference, dict), f"{prefix}.references[{ref_index}] must be an object")
            nonempty(reference.get("label"), f"{prefix}.references[{ref_index}].label")
            url = nonempty(reference.get("url"), f"{prefix}.references[{ref_index}].url")
            parsed_url = urlparse(url)
            require(parsed_url.scheme == "https" and bool(parsed_url.netloc), f"{prefix}.references[{ref_index}].url must be an https URL")
        require(isinstance(finding.get("history"), list), f"{prefix}.history must be an array")
        require(isinstance(finding.get("validation_evidence"), str), f"{prefix}.validation_evidence must be a string")
        accepted = finding.get("accepted_risk")
        require(isinstance(accepted, dict), f"{prefix}.accepted_risk must be an object")
        for field in ("rationale", "owner", "review_date"):
            require(isinstance(accepted.get(field), str), f"{prefix}.accepted_risk.{field} must be a string")
        if finding["status"] == "Resolved":
            valid_date(finding.get("resolution_date"), f"{prefix}.resolution_date")
            nonempty(finding.get("validation_evidence"), f"{prefix}.validation_evidence")
        if finding["status"] == "Accepted Risk":
            nonempty(accepted.get("rationale"), f"{prefix}.accepted_risk.rationale")
            nonempty(accepted.get("owner"), f"{prefix}.accepted_risk.owner")
            if accepted.get("review_date"):
                valid_date(accepted["review_date"], f"{prefix}.accepted_risk.review_date")
    return review, findings


def md_lines(lines: list[str]) -> str:
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(review: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    counts = Counter(item["severity"] for item in findings)
    lines = [f"# {review['title']}", "", f"**Review ID:** {review['id']}  ", f"**Date:** {review['date']}  ", f"**Mode:** {review['mode']} ({review['completion']})  ", f"**Target:** {review['target']}", "", "## Executive summary", "", review["summary"], "", "## Scope", "", *[f"- {item}" for item in review["scope"]]]
    if review["exclusions"]:
        lines += ["", "### Exclusions", "", *[f"- {item}" for item in review["exclusions"]]]
    lines += ["", "## Methodology", "", *[f"- {item}" for item in review["methodology"]], "", "## Finding distribution", "", "| Severity | Count |", "|---|---:|"]
    lines += [f"| {severity} | {counts.get(severity, 0)} |" for severity in ("Critical", "High", "Medium", "Low", "Informational")]
    lines += ["", "## Findings", ""]
    if not findings:
        lines += ["No findings are recorded in the supplied dataset. This does not establish absence of vulnerabilities.", ""]
    for finding in findings:
        lines += [f"### {finding['id']} — {finding['title']}", "", f"- **Severity:** {finding['severity']}", f"- **Category:** {finding['category']}", f"- **Status:** {finding['status']}", f"- **Location:** `{finding['location']}`", f"- **Detected:** {finding['detected_date']}", f"- **Evidence type:** {finding['evidence_type']}", "", "**Evidence**", "", finding["evidence"], "", "**Description**", "", finding["description"], "", "**Scenario**", "", finding["scenario"], "", "**Impact and likelihood**", "", f"- Impact: {finding['impact']}", f"- Likelihood: {finding['likelihood']}", "", "**Recommendation and mitigation**", "", f"- Recommendation: {finding['recommendation']}", f"- Mitigation: {finding['mitigation']}"]
        if finding["references"]:
            lines += ["", "**References**", "", *[f"- [{ref['label']}]({ref['url']})" for ref in finding["references"]]]
        if finding["status"] == "Resolved":
            lines += ["", f"**Resolved:** {finding['resolution_date']}", "", f"**Validation evidence:** {finding['validation_evidence']}"]
        if finding["status"] == "Accepted Risk":
            accepted = finding["accepted_risk"]
            lines += ["", "**Accepted risk**", "", f"- Rationale: {accepted['rationale']}", f"- Owner: {accepted['owner']}", f"- Review date: {accepted['review_date'] or 'Not specified'}"]
        if finding["history"]:
            lines += ["", "**History**", "", *[f"- {entry}" for entry in finding["history"]]]
        lines += [""]
    lines += ["## Controls reviewed", "", "| Control | State | Evidence | Notes |", "|---|---|---|---|"]
    for control in review["controls_reviewed"]:
        cells = [control["name"], control["status"], control["evidence"], control["notes"]]
        lines.append("| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
    lines += ["", "## Standards and references", "", *([f"- {item}" for item in review["standards"]] or ["- None recorded."]), "", "## Limitations", "", *([f"- {item}" for item in review["limitations"]] or ["- None recorded."]), "", "## Related artifacts", "", *([f"- {item}" for item in review["related_artifacts"]] or ["- None recorded."]), "", "## Review history", "", *([f"- {item}" for item in review["history"]] or ["- No prior review history supplied."]), "", "> Generated from the supplied canonical review data. This report is not a certification and does not establish that the system is free of vulnerabilities."]
    return md_lines(lines)


def html_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>" if items else "<p>None recorded.</p>"


def render_html(review: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    counts = Counter(item["severity"] for item in findings)
    severity_rows = "".join(f"<div class='metric {severity.lower()}'><strong>{counts.get(severity, 0)}</strong><span>{escape(severity)}</span></div>" for severity in ("Critical", "High", "Medium", "Low", "Informational"))
    cards = []
    for finding in findings:
        refs = "".join(f"<li><a href='{escape(ref['url'], quote=True)}' rel='noreferrer'>{escape(ref['label'])}</a></li>" for ref in finding["references"])
        resolved = f"<h4>Resolution validation</h4><p>{escape(finding['resolution_date'])}: {escape(finding['validation_evidence'])}</p>" if finding["status"] == "Resolved" else ""
        accepted = finding["accepted_risk"]
        risk = f"<h4>Accepted risk</h4><p><b>Rationale:</b> {escape(accepted['rationale'])}<br><b>Owner:</b> {escape(accepted['owner'])}<br><b>Review date:</b> {escape(accepted['review_date'] or 'Not specified')}</p>" if finding["status"] == "Accepted Risk" else ""
        history = html_list(finding["history"])
        cards.append(f"<article class='finding' id='{escape(finding['id'], quote=True)}'><header><span class='badge {finding['severity'].lower()}'>{escape(finding['severity'])}</span><span class='badge state'>{escape(finding['status'])}</span><span class='finding-id'>{escape(finding['id'])}</span></header><h3>{escape(finding['title'])}</h3><p class='meta'>{escape(finding['category'])} · {escape(finding['location'])} · Detected {escape(finding['detected_date'])}</p><h4>Evidence <small>({escape(finding['evidence_type'])})</small></h4><p>{escape(finding['evidence'])}</p><h4>Description</h4><p>{escape(finding['description'])}</p><h4>Scenario</h4><p>{escape(finding['scenario'])}</p><div class='two'><section><h4>Impact</h4><p>{escape(finding['impact'])}</p></section><section><h4>Likelihood</h4><p>{escape(finding['likelihood'])}</p></section></div><h4>Recommendation</h4><p>{escape(finding['recommendation'])}</p><h4>Mitigation</h4><p>{escape(finding['mitigation'])}</p>{'<h4>References</h4><ul>'+refs+'</ul>' if refs else ''}{resolved}{risk}<details><summary>Finding history</summary>{history}</details></article>")
    controls = "".join(f"<tr><td>{escape(item['name'])}</td><td>{escape(item['status'])}</td><td>{escape(item['evidence'])}</td><td>{escape(item['notes'])}</td></tr>" for item in review["controls_reviewed"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><title>{escape(review['title'])} · Security Review</title>
<style>
:root{{--bg:#f3f6fa;--surface:#fff;--text:#172033;--muted:#596579;--line:#d8dfeb;--accent:#2257a5;--critical:#9e1b20;--high:#bd4517;--medium:#8c6500;--low:#276343;--info:#445b79}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.58 system-ui,-apple-system,"Segoe UI",sans-serif}}a{{color:var(--accent);overflow-wrap:anywhere}}header.hero{{background:linear-gradient(125deg,#10284c,#2257a5);color:white;padding:2.5rem max(1rem,calc((100% - 1100px)/2))}}.wrap{{max-width:1100px;margin:auto;padding:1.5rem}}h1{{margin:.2rem 0;font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.15}}.meta{{color:var(--muted)}}.hero .meta{{color:#d9e7ff}}main{{max-width:1100px;margin:auto;padding:1.5rem}}section,.panel,.finding{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1.2rem;margin:1rem 0;box-shadow:0 5px 18px #14213b0a}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.65rem}}.metric{{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--info);border-radius:10px;padding:.8rem;display:flex;flex-direction:column}}.metric strong{{font-size:1.8rem}}.metric.critical{{border-top-color:var(--critical)}}.metric.high{{border-top-color:var(--high)}}.metric.medium{{border-top-color:var(--medium)}}.metric.low{{border-top-color:var(--low)}}.finding header{{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}}.badge{{border-radius:999px;padding:.15rem .65rem;font-size:.8rem;font-weight:700;background:#e8edf5;color:var(--text)}}.badge.critical{{background:#f9dfe0;color:var(--critical)}}.badge.high{{background:#ffeadf;color:var(--high)}}.badge.medium{{background:#fff2c9;color:var(--medium)}}.badge.low{{background:#def2e6;color:var(--low)}}.finding-id{{margin-left:auto;color:var(--muted);font-family:ui-monospace,monospace}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}table{{width:100%;border-collapse:collapse;display:block;overflow:auto}}th,td{{border-bottom:1px solid var(--line);padding:.6rem;text-align:left;vertical-align:top}}th{{background:var(--bg)}}code{{overflow-wrap:anywhere}}details{{margin-top:1rem}}footer{{max-width:1100px;margin:auto;padding:1rem 1.5rem 2rem;color:var(--muted);font-size:.9rem}}@media(max-width:640px){{.two{{grid-template-columns:1fr}}main{{padding:.8rem}}.wrap{{padding:1.4rem 1rem}}}}@media print{{body{{background:white}}.finding,section,.panel{{box-shadow:none;break-inside:avoid}}a{{color:inherit}}}}
</style></head><body>
<header class="hero"><div class="wrap"><p>APPLICATION SECURITY REVIEW · {escape(review['mode'].upper())} · {escape(review['completion'].upper())}</p><h1>{escape(review['title'])}</h1><p class="meta">{escape(review['target'])} · {escape(review['date'])} · Review {escape(review['id'])}</p></div></header>
<main><section><h2>Executive summary</h2><p>{escape(review['summary'])}</p><h3>Scope</h3>{html_list(review['scope'])}<h3>Exclusions</h3>{html_list(review['exclusions'])}</section>
<section><h2>Finding distribution</h2><div class="metrics">{severity_rows}</div></section>
<section><h2>Findings</h2>{''.join(cards) if cards else '<p>No findings are recorded in the supplied dataset. This does not establish absence of vulnerabilities.</p>'}</section>
<section><h2>Controls reviewed</h2><table><thead><tr><th>Control</th><th>State</th><th>Evidence</th><th>Notes</th></tr></thead><tbody>{controls}</tbody></table></section>
<section><h2>Methodology</h2>{html_list(review['methodology'])}<h3>Standards and references</h3>{html_list(review['standards'])}<h3>Limitations</h3>{html_list(review['limitations'])}<h3>Related artifacts</h3>{html_list(review['related_artifacts'])}<h3>Review history</h3>{html_list(review['history'])}</section></main>
<footer>Generated from canonical review data. This report is not a certification and does not establish that the system is free of vulnerabilities.</footer></body></html>\n"""


def registry_markdown(findings: list[dict[str, Any]]) -> str:
    lines = ["# Security Findings Register", "", "This register is rendered from the complete finding set supplied in the canonical review JSON. Reconcile prior records before replacing it.", "", "| ID | Finding | Severity | Status | Location | Detected | Resolved |", "|---|---|---|---|---|---|---|"]
    for item in findings:
        cells = [item["id"], item["title"], item["severity"], item["status"], item["location"], item["detected_date"], item["resolution_date"]]
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
    if not findings:
        lines.append("| — | No findings recorded | — | — | — | — | — |")
    lines += ["", "See the dated review reports for evidence, rationale, remediation guidance, and finding history."]
    return md_lines(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Canonical review JSON")
    parser.add_argument("--out", type=Path, help="Project root for security/ outputs; omit with --check")
    parser.add_argument("--check", action="store_true", help="Validate only; create or modify no files")
    args = parser.parse_args()
    if args.check and args.out:
        parser.error("--check and --out cannot be used together")
    if not args.check and not args.out:
        parser.error("--out is required unless --check is used")
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        review, findings = validate(data)
        if args.check:
            print(f"Valid: {review['id']}, {len(findings)} finding(s)")
            return 0
        assert args.out is not None
        root = args.out.resolve()
        history = root / "security" / "reports" / "history"
        stem = f"security-review-{review['date']}-{review['id']}"
        historical = [history / f"{stem}.md", history / f"{stem}.html"]
        collisions = [path for path in historical if path.exists()]
        if collisions:
            raise InputError("historical report exists; choose a new review.id: " + ", ".join(str(p) for p in collisions))
        report_md = render_markdown(review, findings)
        report_html = render_html(review, findings)
        targets = {
            root / "security" / "findings" / "findings.md": registry_markdown(findings),
            historical[0]: report_md,
            historical[1]: report_html,
        }
        if review["mode"] == "Audit" and review["completion"] == "Complete":
            targets[root / "security" / "reports" / "latest.md"] = report_md
            targets[root / "security" / "reports" / "latest.html"] = report_html
        for path, content in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        latest = "; latest reports updated" if review["mode"] == "Audit" and review["completion"] == "Complete" else "; latest reports left unchanged"
        print(f"Generated {len(targets)} file(s) for {review['id']}{latest}")
        return 0
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
