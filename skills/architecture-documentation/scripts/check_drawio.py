#!/usr/bin/env python3
"""Check Draw.io XML structure and flag common layout problems (stdlib only)."""

from __future__ import annotations

import argparse
import base64
import re
import sys
import zlib
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET


TEXT_STYLES = ("text;", "shape=none;", "shape=label;")
CONTAINER_STYLES = ("swimlane", "group", "container")


def parse_diagram(diagram: ET.Element) -> ET.Element:
    """Return an mxGraphModel from either plain or compressed Draw.io XML."""
    model = diagram.find("mxGraphModel")
    if model is not None:
        return model

    payload = (diagram.text or "").strip()
    if not payload:
        raise ValueError("diagram has neither an mxGraphModel nor compressed content")
    try:
        compressed = base64.b64decode(payload)
        decoded = zlib.decompress(compressed, -zlib.MAX_WBITS).decode("utf-8")
        decoded = unquote(decoded)
        root = ET.fromstring(decoded)
    except (ValueError, zlib.error, UnicodeDecodeError, ET.ParseError) as exc:
        raise ValueError(f"could not decode compressed diagram: {exc}") from exc
    if root.tag == "mxGraphModel":
        return root
    model = root.find("mxGraphModel")
    if model is None:
        raise ValueError("decoded diagram does not contain mxGraphModel")
    return model


def geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    geo = cell.find("mxGeometry")
    if geo is None or geo.get("as") == "relative":
        return None
    try:
        x = float(geo.get("x", "0"))
        y = float(geo.get("y", "0"))
        width = float(geo.get("width", "0"))
        height = float(geo.get("height", "0"))
    except ValueError:
        return None
    return x, y, width, height


def is_text_or_container(cell: ET.Element) -> bool:
    style = cell.get("style", "").lower()
    value = cell.get("value", "").strip()
    if any(token in style for token in TEXT_STYLES):
        return True
    if value and ("text" in style or "autosize=1" in style):
        return True
    return any(token in style for token in CONTAINER_STYLES)


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    """Return intersection area as a fraction of the smaller rectangle."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    iw = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    ih = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    smaller = min(max(0.0, aw * ah), max(0.0, bw * bh))
    return (iw * ih / smaller) if smaller else 0.0


def contained(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (
        ax <= bx and ay <= by and ax + aw >= bx + bw and ay + ah >= by + bh
    ) or (
        bx <= ax and by <= ay and bx + bw >= ax + aw and by + bh >= ay + ah
    )


def check_file(path: Path) -> tuple[int, int]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        print(f"ERROR {path}: invalid XML: {exc}")
        return 1, 0

    if root.tag != "mxfile":
        print(f"ERROR {path}: root element is <{root.tag}>, expected <mxfile>")
        return 1, 0

    diagrams = root.findall("diagram")
    if not diagrams:
        errors.append("mxfile contains no diagram pages")

    for page_number, diagram in enumerate(diagrams, start=1):
        page = diagram.get("name") or f"page {page_number}"
        try:
            model = parse_diagram(diagram)
        except ValueError as exc:
            errors.append(f"{page}: {exc}")
            continue

        graph_root = model.find("root")
        if graph_root is None:
            errors.append(f"{page}: mxGraphModel has no root")
            continue
        cells = list(graph_root.findall("mxCell"))
        ids: dict[str, ET.Element] = {}
        for cell in cells:
            cell_id = cell.get("id")
            if not cell_id:
                errors.append(f"{page}: cell without an id")
            elif cell_id in ids:
                errors.append(f"{page}: duplicate cell id {cell_id!r}")
            else:
                ids[cell_id] = cell

        for cell in cells:
            if cell.get("edge") != "1":
                continue
            cell_id = cell.get("id", "<missing id>")
            for endpoint in ("source", "target"):
                target_id = cell.get(endpoint)
                if not target_id:
                    errors.append(f"{page}: edge {cell_id} has no {endpoint}")
                elif target_id not in ids:
                    errors.append(f"{page}: edge {cell_id} references missing {endpoint} {target_id!r}")

        model_width = float(model.get("pageWidth", "0") or 0)
        model_height = float(model.get("pageHeight", "0") or 0)
        shapes: list[tuple[ET.Element, tuple[float, float, float, float]]] = []
        page_overflow: list[tuple[str, float, float, float, float]] = []
        for cell in cells:
            if cell.get("vertex") != "1":
                continue
            rect = geometry(cell)
            if rect is None:
                continue
            x, y, width, height = rect
            cell_id = cell.get("id", "<missing id>")
            if width <= 0 or height <= 0:
                errors.append(f"{page}: vertex {cell_id} has non-positive dimensions")
                continue
            if model_width and model_height and (x < 0 or y < 0 or x + width > model_width or y + height > model_height):
                page_overflow.append((cell_id, x, y, width, height))
            if not is_text_or_container(cell):
                shapes.append((cell, rect))

            style = cell.get("style", "")
            font_match = re.search(r"(?:^|;)fontSize=(\d+)(?:;|$)", style)
            if font_match and int(font_match.group(1)) < 10:
                warnings.append(f"{page}: vertex {cell_id} uses small font size {font_match.group(1)}")

        if page_overflow:
            right = max(item[1] + item[3] for item in page_overflow)
            bottom = max(item[2] + item[4] for item in page_overflow)
            left = min(item[1] for item in page_overflow)
            top = min(item[2] for item in page_overflow)
            warnings.append(
                f"{page}: {len(page_overflow)} vertex/vertices exceed the configured page "
                f"({model_width:g}x{model_height:g}); outlying geometry spans x={left:g}..{right:g}, y={top:g}..{bottom:g}"
            )

        for index, (left, left_rect) in enumerate(shapes):
            for right, right_rect in shapes[index + 1 :]:
                if left.get("parent") != right.get("parent"):
                    continue
                if contained(left_rect, right_rect):
                    continue
                ratio = overlaps(left_rect, right_rect)
                if ratio >= 0.15:
                    warnings.append(
                        f"{page}: likely shape overlap between {left.get('id')} and {right.get('id')} ({ratio:.0%})"
                    )

    for message in errors:
        print(f"ERROR {path}: {message}")
    for message in warnings:
        print(f"WARN  {path}: {message}")
    if not errors and not warnings:
        print(f"OK    {path}: {len(diagrams)} page(s), structure and layout heuristics passed")
    elif not errors:
        print(f"OK    {path}: structure passed; review {len(warnings)} layout warning(s)")
    return len(errors), len(warnings)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Draw.io XML and flag likely page-boundary, overlap, and small-font issues."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Draw.io files or folders to inspect")
    parser.add_argument(
        "--strict-layout",
        action="store_true",
        help="return a failing exit status when layout heuristics emit warnings",
    )
    args = parser.parse_args()

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.drawio")))
        elif path.is_file() and path.suffix.lower() == ".drawio":
            files.append(path)
        else:
            print(f"ERROR {path}: not a .drawio file or directory", file=sys.stderr)
            return 2
    files = list(dict.fromkeys(file.resolve() for file in files))
    if not files:
        print("ERROR: no .drawio files found", file=sys.stderr)
        return 2

    totals = [check_file(path) for path in files]
    errors = sum(item[0] for item in totals)
    warnings = sum(item[1] for item in totals)
    print(f"Summary: {len(files)} file(s), {errors} error(s), {warnings} layout warning(s)")
    return 1 if errors or (args.strict_layout and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
