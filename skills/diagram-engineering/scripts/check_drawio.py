#!/usr/bin/env python3
"""Validate native Draw.io structure, component/icon collisions and portable SVGs.

Adapted from architecture-documentation 1.8.13; see references/reuse-provenance.md.

Errors (exit code 1): invalid XML/hierarchy/geometry, duplicated IDs, invalid
endpoints, native component/icon/label collisions, and invalid SVG/resources.
Warnings: label text running into an icon, icons that are not 78x78 / 46x46 or lack the white stroke,
icons with an inline label, edges that are not sharp orthogonal or carry a label, edges whose explicit
route crosses an unrelated icon.

Label sizes are estimated from the text (draw.io only stores the size of the last save), so a label that
was edited by hand is still measured correctly.

Usage: python3 check_drawio.py [--require-provider-icons aws|azure|google|ibm]
       [--icon-inventory icons.json] diagram.drawio [more.drawio ...]

The provider-icon option is a markup-presence heuristic. It cannot verify the SVG source,
service-to-glyph mapping, or that diagrams.net rendered a stencil correctly; inspect a preview.
"""
import base64
import argparse
import html
import json
import math
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

TOL = 4.0  # px of overlap tolerated (anti aliasing, shared borders)
PICTORIAL_SHAPE = re.compile(r"(?:umlactor|person|user|smartphone|mobile|tablet|laptop|computer|browser|device)", re.I)


def load_models(path):
    root = ET.parse(path).getroot()
    models = []
    diagrams = root.findall("diagram") if root.tag == "mxfile" else []
    if root.tag == "mxGraphModel":
        return [("page-1", root)]
    if root.tag != "mxfile":
        raise ValueError("expected <mxfile> or <mxGraphModel>")
    for d in diagrams:
        m = d.find("mxGraphModel")
        if m is None and (d.text or "").strip():  # compressed page: base64 + raw deflate + url encoding
            raw = zlib.decompress(base64.b64decode(d.text.strip()), -15)
            m = ET.fromstring(urllib.parse.unquote(raw.decode("utf-8")))
        if m is not None:
            models.append((d.get("name", "page"), m))
        else:
            raise ValueError("diagram page has no model")
    if not models:
        raise ValueError("document has no diagram models")
    return models


def style_map(s):
    out = {}
    # Draw.io styles use semicolons between properties, but SVG data URIs can
    # also contain semicolons in their metadata (for example ;base64,). Keep
    # those header separators until the data URI's first comma.
    source = s or ""
    parts = []
    start = 0
    for index, char in enumerate(source):
        if char != ";":
            continue
        part = source[start:index]
        if part.lower().startswith("image=data:image/svg+xml") and "," not in part:
            continue
        parts.append(part)
        start = index + 1
    parts.append(source[start:])
    for part in parts:
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


def validate_embedded_svg(uri):
    """Return an error message when an embedded SVG data URI is malformed."""
    header, sep, payload = uri.partition(",")
    if not sep or not header.lower().startswith("data:image/svg+xml"):
        return "not an SVG data URI"
    try:
        if ";base64" in header.lower():
            raw = base64.b64decode(payload, validate=True)
        else:
            raw = urllib.parse.unquote_to_bytes(payload)
        svg = ET.fromstring(raw)
    except (ValueError, ET.ParseError) as exc:
        return f"invalid embedded SVG ({exc})"
    if svg.tag.split("}")[-1].lower() != "svg":
        return "embedded image root element is not <svg>"
    for element in svg.iter():
        if element.tag.split("}")[-1].lower() in ("script", "foreignobject"):
            return "embedded SVG contains active content"
        for key, value in element.attrib.items():
            local = key.split("}")[-1].lower()
            if local.startswith("on"):
                return "embedded SVG contains an event handler"
            if local in ("href", "src") and not value.startswith(("#", "data:")):
                return "embedded SVG references an external resource"
        css = element.get("style", "") + (element.text or "" if element.tag.split("}")[-1] == "style" else "")
        if re.search(r"@import|url\(\s*['\"]?(?!#|data:)[^\s'\"]", css, re.I):
            return "embedded SVG references external CSS/resources"
    return None


def preflight(name, model):
    """Reject malformed hierarchies before walking parents or measuring geometry."""
    problems = []
    root = model.find("root")
    if root is None:
        return [f"[{name}] model has no root"]
    cells = {}
    for element in root.iter("mxCell"):
        cid = element.get("id")
        if not cid or cid in cells:
            problems.append(f"[{name}] empty or duplicated id {cid!r}")
        cells[cid] = element
    if "0" not in cells or "1" not in cells or cells.get("1").get("parent") != "0":
        problems.append(f"[{name}] required base cells 0 and 1 are missing or invalid")
    if cells.get("0") is not None and cells["0"].get("parent"):
        problems.append(f"[{name}] base cell 0 must not have a parent")
    if not any(el.get("vertex") == "1" for el in cells.values()):
        problems.append(f"[{name}] model has no vertices")
    for cid, element in cells.items():
        parent = element.get("parent")
        if cid != "0" and parent not in cells:
            problems.append(f"[{name}] cell {cid!r} has a missing parent {parent!r}")
        seen = {cid}
        while parent in cells:
            if parent in seen:
                problems.append(f"[{name}] parent cycle involving {cid!r}")
                break
            seen.add(parent)
            parent = cells[parent].get("parent")
        if element.get("vertex") != "1" and element.get("edge") != "1":
            continue
        geo = element.find("mxGeometry")
        if geo is None:
            problems.append(f"[{name}] cell {cid!r} has no geometry")
            continue
        for point in geo.iter():
            for key in ("x", "y", "width", "height"):
                try:
                    number = float(point.get(key, 0))
                    if not math.isfinite(number) or (key in ("width", "height") and number < 0):
                        raise ValueError()
                except (ValueError, TypeError):
                    problems.append(f"[{name}] invalid {key} geometry on {cid!r}")
        if element.get("vertex") == "1" and element.get("data-role") != "anchor":
            try:
                if float(geo.get("width", 0)) <= 0 or float(geo.get("height", 0)) <= 0:
                    problems.append(f"[{name}] vertex {cid!r} needs positive dimensions")
            except ValueError:
                pass  # Reported by the numeric check above.
        if element.get("edge") == "1" and element.get("data-role") != "decoration":
            for endpoint in ("source", "target"):
                target = cells.get(element.get(endpoint))
                if target is None or target.get("vertex") != "1":
                    problems.append(f"[{name}] edge {cid!r} {endpoint} must resolve to a vertex/anchor")
    return problems


def check_model(name, model, errors, warnings):
    provider_counts = {"aws": 0, "azure_native": 0, "google_native": 0, "ibm_native": 0, "embedded_svg": 0}
    problems = preflight(name, model)
    if problems:
        errors.extend(problems)
        return 0, 0, 0, provider_counts
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

    # Keep original offsets immutable: otherwise deeper nesting double-counts ancestors.
    local_geometry = {cid: c["geo"] for cid, c in cells.items()}
    absolute_geometry = {}
    def absolute(c):
        if c["id"] in absolute_geometry:
            return absolute_geometry[c["id"]]
        x, y, w, h = local_geometry[c["id"]]
        p = cells.get(c["parent"])
        if p is not None and local_geometry[p["id"]] is not None:
            px, py, pw, ph = absolute(p)
            if c["el"].find("mxGeometry").get("relative") == "1":
                x, y = x * pw, y * ph
            x, y = x + px, y + py
        offset = c["el"].find("./mxGeometry/mxPoint[@as='offset']")
        if offset is not None:
            x, y = x + float(offset.get("x", 0)), y + float(offset.get("y", 0))
        absolute_geometry[c["id"]] = (x, y, w, h)
        return absolute_geometry[c["id"]]

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
        is_actor_or_device = bool(PICTORIAL_SHAPE.search(shape))
        is_aws_native = "resIcon" in st or shape.startswith("mxgraph.aws4")
        is_provider_icon = (
            is_aws_native
            or shape.startswith(("mxgraph.gcp", "mxgraph.azure", "mxgraph.ibm"))
            or "image" in st
            or "image;" in style_text
        )
        image_data = str(st.get("image", ""))
        if "resIcon" in st and str(st.get("resIcon", "")).startswith("mxgraph.aws4."):
            provider_counts["aws"] += 1
        elif shape.startswith("mxgraph.aws4."):
            provider_counts["aws"] += 1
        elif shape.startswith("mxgraph.azure."):
            provider_counts["azure_native"] += 1
        elif shape.startswith(("mxgraph.gcp.", "mxgraph.gcp2.", "mxgraph.gcp3.")):
            provider_counts["google_native"] += 1
        elif shape.startswith("mxgraph.ibm."):
            provider_counts["ibm_native"] += 1
        elif shape == "image" and image_data.lower().startswith("data:image/svg+xml"):
            # SVG source/provider provenance and service-to-icon correctness are reviewed separately.
            provider_counts["embedded_svg"] += 1
            svg_error = validate_embedded_svg(image_data)
            if svg_error:
                errors.append(f"[{name}] icon {label(c)}: {svg_error}")
        if image_data and not image_data.lower().startswith("data:image/svg+xml"):
            errors.append(f"[{name}] icon {label(c)} must embed SVG instead of an external/raster image")
        if is_provider_icon or is_actor_or_device:
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
    vertex_boxes = {
        c["id"]: (c["geo"][0], c["geo"][1], c["geo"][0] + c["geo"][2], c["geo"][1] + c["geo"][3])
        for c in cells.values() if c["geo"] is not None and not c["edge"]
    }
    lboxes = {c["id"]: label_box(c) for c in texts}

    # Check native component cards as well as pictograms. Containers may enclose
    # their members; unrelated siblings must not overlap. Explicit roles cover
    # sequence anchors and visual frames with children on the base layer.
    parents = {c["parent"] for c in cells.values()}
    def is_frame(c):
        st = c["style"]
        return (c["id"] in parents or c["el"].get("data-role") in ("boundary", "anchor", "decoration")
                or "swimlane" in st or st.get("shape") == "swimlane"
                or (st.get("fillColor") == "none" and st.get("dashed") == "1"
                    and st.get("verticalAlign") == "top" and st.get("align") == "left"))
    def related(a, b):
        parent = a["parent"]
        while parent in cells:
            if parent == b["id"]:
                return True
            parent = cells[parent]["parent"]
        return False
    already_checked = {c["id"] for c in icons + texts}
    solids = [c for c in cells.values() if c["geo"] is not None and not c["edge"] and not is_frame(c)]
    for i, a in enumerate(solids):
        for b in solids[i + 1:]:
            if related(a, b) or related(b, a):
                continue
            if a["id"] in already_checked and b["id"] in already_checked:
                continue  # Existing icon/text checks below handle these pairs.
            if overlap(vertex_boxes[a["id"]], vertex_boxes[b["id"]]):
                errors.append(f"[{name}] components overlap: {label(a)} and {label(b)}")
    for c in cells.values():
        if c["geo"] is None or c["edge"]:
            continue
        p = cells.get(c["parent"])
        if p is not None and p["geo"] is not None and c["el"].get("data-role") != "anchor":
            x, y, w, h = c["geo"]
            px, py, pw, ph = p["geo"]
            if x < px - TOL or y < py - TOL or x + w > px + pw + TOL or y + h > py + ph + TOL:
                errors.append(f"[{name}] component {label(c)} extends outside parent {label(p)}")

    for i, a in enumerate(icons):
        for b in icons[i + 1:]:
            if related(a, b) or related(b, a):
                continue
            o = overlap(boxes[a["id"]], boxes[b["id"]])
            if o:
                errors.append(f"[{name}] icons overlap: {label(a)} and {label(b)} ({o[0]:.0f}x{o[1]:.0f}px)")
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if related(a, b) or related(b, a):
                continue
            o = overlap(lboxes[a["id"]], lboxes[b["id"]])
            if o:
                errors.append(f"[{name}] labels overlap: {label(a)} and {label(b)} ({o[0]:.0f}x{o[1]:.0f}px)")
        for ic in icons:
            if related(a, ic) or related(ic, a):
                continue
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
        if src in vertex_boxes and tgt in vertex_boxes:
            def anchor(box, kx, ky):
                return (box[0] + (box[2] - box[0]) * kx, box[1] + (box[3] - box[1]) * ky)
            a = anchor(vertex_boxes[src], float(st.get("exitX", 0.5)), float(st.get("exitY", 0.5)))
            b = anchor(vertex_boxes[tgt], float(st.get("entryX", 0.5)), float(st.get("entryY", 0.5)))
            path = [a] + pts + [b]
            for p, q in zip(path, path[1:]):
                for ic in icons:
                    if ic["id"] in (src, tgt):
                        continue
                    if seg_hits_box(p, q, boxes[ic["id"]]):
                        warnings.append(f"[{name}] edge {c['id']} ({label(cells[src])} -> {label(cells[tgt])}) "
                                        f"crosses icon {label(ic)}")
                for txt in texts:
                    if txt["id"] in (src, tgt):
                        continue
                    if seg_hits_box(p, q, lboxes[txt["id"]], pad=0.0):
                        warnings.append(f"[{name}] edge {c['id']} ({label(cells[src])} -> {label(cells[tgt])}) "
                                        f"crosses label {label(txt)}")
    return len(icons), len(texts), sum(1 for c in cells.values() if c["edge"]), provider_counts


def inventory_counts(models, inventory):
    """Bind provider-neutral embedded SVGs to declared inventory rows, not device icons."""
    counts = {"aws": 0, "azure": 0, "google": 0, "ibm": 0}
    pages = {name: model for name, model in models}
    if len(pages) != len(models):
        raise ValueError("inventory needs unique page names")
    seen = set()
    if not isinstance(inventory, dict) or not isinstance(inventory.get("icons"), list):
        raise ValueError("icon inventory must contain an icons array")
    for row in inventory["icons"]:
        if not isinstance(row, dict):
            raise ValueError("icon inventory rows must be objects")
        page, cid, provider = row.get("page"), row.get("cell_id"), row.get("provider")
        if provider not in counts or not isinstance(row.get("source"), str) or not row["source"].strip():
            raise ValueError("inventory row requires a supported provider and nonempty source")
        key = (page, cid)
        if key in seen:
            raise ValueError(f"duplicate icon inventory row {key}")
        seen.add(key)
        model = pages.get(page)
        matches = [] if model is None else [c for c in model.iter("mxCell") if c.get("id") == cid]
        if len(matches) != 1 or matches[0].get("vertex") != "1":
            raise ValueError(f"inventory cell does not resolve uniquely: {key}")
        style = style_map(matches[0].get("style"))
        image = str(style.get("image", ""))
        if image.lower().startswith("data:image/svg+xml"):
            problem = validate_embedded_svg(image)
            if problem:
                raise ValueError(problem)
            counts[provider] += 1
        else:
            prefix = {"aws": ("mxgraph.aws4.",), "azure": ("mxgraph.azure.",),
                      "google": ("mxgraph.gcp.", "mxgraph.gcp2.", "mxgraph.gcp3."), "ibm": ("mxgraph.ibm.",)}[provider]
            if not str(style.get("resIcon", style.get("shape", ""))).startswith(prefix):
                raise ValueError(f"inventory provider conflicts with native icon: {key}")
    return counts


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-provider-icons", choices=("aws", "azure", "google", "ibm"),
                        help="fail if the diagram contains no recognized provider icon markup")
    parser.add_argument("--icon-inventory", help="JSON inventory binding SVG cells to providers; requires one input file")
    parser.add_argument("paths", nargs="+", help="one or more .drawio files")
    args = parser.parse_args(argv)
    if args.icon_inventory and len(args.paths) != 1:
        parser.error("--icon-inventory requires exactly one input file")
    if not args.paths:
        print(__doc__)
        return 2
    failed = False
    for path in args.paths:
        errors, warnings = [], []
        try:
            models = load_models(path)
        except (OSError, ET.ParseError, ValueError, zlib.error) as exc:
            print(f"[ERROR] {path}: cannot parse ({exc})")
            failed = True
            continue
        try:
            totals = [check_model(n, m, errors, warnings) for n, m in models]
        except (ValueError, TypeError, OverflowError) as exc:
            print(f"[ERROR] {path}: invalid diagram value ({exc})")
            failed = True
            continue
        n_icons, n_texts, n_edges = (sum(t[i] for t in totals) for i in range(3))
        provider_counts = {p: sum(t[3][p] for t in totals)
                           for p in ("aws", "azure_native", "google_native", "ibm_native", "embedded_svg")}
        declared = {p: 0 for p in ("aws", "azure", "google", "ibm")}
        if args.icon_inventory:
            try:
                with open(args.icon_inventory, encoding="utf-8") as source:
                    declared = inventory_counts(models, json.load(source))
            except (OSError, ValueError, TypeError) as exc:
                errors.append(f"[diagram] invalid icon inventory ({exc})")
        print(f"{path}: {len(models)} page(s), {n_icons} icons, {n_texts} labels, {n_edges} edges")
        print("  icon markup (heuristic): " + ", ".join(f"{p}={n}" for p, n in provider_counts.items()))
        recognized = {
            "aws": provider_counts["aws"] + declared["aws"],
            "azure": provider_counts["azure_native"] + declared["azure"],
            "google": provider_counts["google_native"] + declared["google"],
            "ibm": provider_counts["ibm_native"] + declared["ibm"],
        }
        if args.require_provider_icons and recognized[args.require_provider_icons] == 0:
            errors.append(f"[diagram] no recognized {args.require_provider_icons} provider icon markup found")
        if provider_counts["embedded_svg"]:
            warnings.append("[diagram] embedded SVGs are provider-neutral; provider enforcement requires --icon-inventory; verify provenance and glyph mapping manually")
        for w in warnings:
            print(f"  [WARN]  {w}")
        for e in errors:
            print(f"  [ERROR] {e}")
        print(f"  -> {len(errors)} errors, {len(warnings)} warnings")
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
