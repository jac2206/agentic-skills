#!/usr/bin/env python3
"""Lint a .drawio file against the house style and find overlaps before you even render it.

Errors (exit code 1): invalid XML, duplicated ids, edges pointing to missing cells, icons overlapping icons,
labels overlapping other labels.
Warnings: label text running into an icon, icons that are not 78x78 / 46x46 or lack the white stroke,
icons with an inline label, edges that are not sharp orthogonal or carry a label, edges whose explicit
route crosses an unrelated icon.

Label sizes are estimated from the text (draw.io only stores the size of the last save), so a label that
was edited by hand is still measured correctly.

Usage: python3 check_drawio.py diagram.drawio [more.drawio ...]
"""
import base64
import html
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

TOL = 4.0  # px of overlap tolerated (anti aliasing, shared borders)


def load_models(path):
    root = ET.parse(path).getroot()
    models = []
    diagrams = root.findall("diagram") if root.tag == "mxfile" else []
    if root.tag == "mxGraphModel":
        return [("page-1", root)]
    for d in diagrams:
        m = d.find("mxGraphModel")
        if m is None and (d.text or "").strip():  # compressed page: base64 + raw deflate + url encoding
            raw = zlib.decompress(base64.b64decode(d.text.strip()), -15)
            m = ET.fromstring(urllib.parse.unquote(raw.decode("utf-8")))
        if m is not None:
            models.append((d.get("name", "page"), m))
    return models


def style_map(s):
    out = {}
    for part in (s or "").split(";"):
        if not part:
            continue
        k, _, v = part.partition("=")
        out[k] = v if _ else True
    return out


def text_lines(value):
    v = html.unescape(value or "")
    v = re.sub(r"(?i)<br\s*/?>|<div[^>]*>|</div>|<p[^>]*>|</p>|&#xa;|&#10;", "\n", v)
    v = re.sub(r"<[^>]+>", "", v)
    return [x for x in v.split("\n") if x.strip()] or [""]


def label_box(c):
    """Estimated box of a text cell (center aligned like the house style uses)."""
    st, (x, y, w, h) = c["style"], c["geo"]
    fs = float(st.get("fontSize", 12))
    lines = text_lines(c["value"])
    bold = 1.06 if "1" in str(st.get("fontStyle", "0")) else 1.0
    est_w = max(len(line) for line in lines) * fs * 0.56 * bold
    est_h = len(lines) * fs * 1.25
    cx, cy = x + w / 2, y + h / 2
    W, H = max(w if st.get("autosize") != "1" else 0, est_w), max(est_h, 1)
    align = st.get("align", "center")
    if align == "left":
        return (x, cy - H / 2, x + W, cy + H / 2)
    if align == "right":
        return (x + w - W, cy - H / 2, x + w, cy + H / 2)
    return (cx - W / 2, cy - H / 2, cx + W / 2, cy + H / 2)


def overlap(a, b):
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    return (dx, dy) if dx > TOL and dy > TOL else None


def seg_hits_box(p, q, box, pad=2.0):
    """Axis aligned segment (orthogonal edges) against a box."""
    x1, y1, x2, y2 = box[0] + pad, box[1] + pad, box[2] - pad, box[3] - pad
    if abs(p[1] - q[1]) < 0.5:  # horizontal
        y = p[1]
        return y1 < y < y2 and min(p[0], q[0]) < x2 and max(p[0], q[0]) > x1
    if abs(p[0] - q[0]) < 0.5:  # vertical
        x = p[0]
        return x1 < x < x2 and min(p[1], q[1]) < y2 and max(p[1], q[1]) > y1
    return False


def check_model(name, model, errors, warnings):
    root = model.find("root")
    cells, seen = {}, set()
    for el in root.iter("mxCell"):
        cid = el.get("id")
        if cid in seen:
            errors.append(f"[{name}] duplicated id {cid!r}")
        seen.add(cid)
        g = el.find("mxGeometry")
        geo = None
        if g is not None and el.get("vertex") == "1":
            geo = (float(g.get("x", 0)), float(g.get("y", 0)), float(g.get("width", 0)), float(g.get("height", 0)))
        cells[cid] = {"id": cid, "el": el, "style": style_map(el.get("style")), "value": el.get("value") or "",
                      "parent": el.get("parent"), "geo": geo, "edge": el.get("edge") == "1"}

    # absolute coordinates for nested cells
    def absolute(c):
        x, y, w, h = c["geo"]
        p = cells.get(c["parent"])
        while p is not None and p["geo"] is not None:
            x, y = x + p["geo"][0], y + p["geo"][1]
            p = cells.get(p["parent"])
        return (x, y, w, h)

    for c in cells.values():
        if c["geo"] is not None:
            c["geo"] = absolute(c)

    def label(c):
        t = " / ".join(text_lines(c["value"]))[:40]
        return f"{c['id']} ({t})" if t else c["id"]

    icons, texts = [], []
    for c in cells.values():
        st = c["style"]
        if c["geo"] is None or c["edge"]:
            continue
        shape = str(st.get("shape", ""))
        style_text = c["el"].get("style", "").lower()
        is_aws_native = "resIcon" in st or shape.startswith("mxgraph.aws4")
        is_provider_icon = (
            is_aws_native
            or shape.startswith(("mxgraph.gcp", "mxgraph.azure"))
            or "image" in st
            or "image;" in style_text
        )
        if is_provider_icon:
            icons.append(c)
            x, y, w, h = c["geo"]
            if (round(w), round(h)) not in ((78, 78), (46, 46)) and "resIcon" in st:
                warnings.append(f"[{name}] icon {label(c)} is {w:g}x{h:g} (house style: 78x78, sub icons 46x46)")
            if is_aws_native and "resIcon" in st and str(st.get("strokeColor", "")).lower() != "#ffffff":
                warnings.append(f"[{name}] icon {label(c)} without strokeColor=#ffffff")
            if text_lines(c["value"]) != [""]:
                warnings.append(f"[{name}] icon {label(c)} has an inline label: use a separate text cell below it")
        elif "text" in st:
            texts.append(c)

    boxes = {c["id"]: (c["geo"][0], c["geo"][1], c["geo"][0] + c["geo"][2], c["geo"][1] + c["geo"][3]) for c in icons}
    lboxes = {c["id"]: label_box(c) for c in texts}

    for i, a in enumerate(icons):
        for b in icons[i + 1:]:
            o = overlap(boxes[a["id"]], boxes[b["id"]])
            if o:
                errors.append(f"[{name}] icons overlap: {label(a)} and {label(b)} ({o[0]:.0f}x{o[1]:.0f}px)")
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            o = overlap(lboxes[a["id"]], lboxes[b["id"]])
            if o:
                errors.append(f"[{name}] labels overlap: {label(a)} and {label(b)} ({o[0]:.0f}x{o[1]:.0f}px)")
        for ic in icons:
            o = overlap(lboxes[a["id"]], boxes[ic["id"]])
            if o:
                warnings.append(f"[{name}] label {label(a)} runs into icon {label(ic)} ({o[0]:.0f}x{o[1]:.0f}px)")

    for c in cells.values():
        if not c["edge"]:
            continue
        st, el = c["style"], c["el"]
        src, tgt = el.get("source"), el.get("target")
        for end, ref in (("source", src), ("target", tgt)):
            if ref and ref not in cells:
                errors.append(f"[{name}] edge {c['id']} {end} points to missing cell {ref!r}")
        if not src or not tgt:
            warnings.append(f"[{name}] edge {c['id']} is not connected at both ends (it will not follow moved icons)")
        if st.get("edgeStyle") != "orthogonalEdgeStyle" or str(st.get("rounded", "0")) != "0":
            warnings.append(f"[{name}] edge {c['id']} is not sharp orthogonal (edgeStyle=orthogonalEdgeStyle;rounded=0)")
        if text_lines(c["value"]) != [""]:
            warnings.append(f"[{name}] edge {c['id']} has a label: use a red annotation text cell instead")
        # explicit route: exit anchor -> waypoints -> entry anchor
        pts = [(float(p.get("x", 0)), float(p.get("y", 0)))
               for p in el.findall("./mxGeometry/Array[@as='points']/mxPoint")]
        if src in boxes and tgt in boxes:
            def anchor(box, kx, ky):
                return (box[0] + (box[2] - box[0]) * kx, box[1] + (box[3] - box[1]) * ky)
            a = anchor(boxes[src], float(st.get("exitX", 0.5)), float(st.get("exitY", 0.5)))
            b = anchor(boxes[tgt], float(st.get("entryX", 0.5)), float(st.get("entryY", 0.5)))
            path = [a] + pts + [b]
            for p, q in zip(path, path[1:]):
                for ic in icons:
                    if ic["id"] in (src, tgt):
                        continue
                    if seg_hits_box(p, q, boxes[ic["id"]]):
                        warnings.append(f"[{name}] edge {c['id']} ({label(cells[src])} -> {label(cells[tgt])}) "
                                        f"crosses icon {label(ic)}")
    return len(icons), len(texts), sum(1 for c in cells.values() if c["edge"])


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    failed = False
    for path in paths:
        errors, warnings = [], []
        try:
            models = load_models(path)
        except (ET.ParseError, ValueError, zlib.error) as exc:
            print(f"[ERROR] {path}: cannot parse ({exc})")
            failed = True
            continue
        totals = [check_model(n, m, errors, warnings) for n, m in models]
        n_icons, n_texts, n_edges = (sum(t[i] for t in totals) for i in range(3))
        print(f"{path}: {len(models)} page(s), {n_icons} icons, {n_texts} labels, {n_edges} edges")
        for w in warnings:
            print(f"  [WARN]  {w}")
        for e in errors:
            print(f"  [ERROR] {e}")
        print(f"  -> {len(errors)} errors, {len(warnings)} warnings")
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
