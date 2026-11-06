#!/usr/bin/env python3
"""Export Draw.io diagrams through the installed diagrams.net Desktop CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

EXPORT_TIMEOUT_SECONDS = 90


def find_drawio() -> str | None:
    configured = os.environ.get("DRAWIO")
    if configured:
        return configured
    for command in ("drawio", "draw.io", "drawio.exe", "draw.io.exe"):
        found = shutil.which(command)
        if found:
            return found
    if sys.platform == "win32":
        for path in (
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "draw.io" / "draw.io.exe",
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "draw.io" / "draw.io.exe",
        ):
            if path.is_file():
                return str(path)
    if sys.platform == "darwin":
        for path in (
            Path("/Applications/draw.io.app/Contents/MacOS/draw.io"),
            Path.home() / "Applications/draw.io.app/Contents/MacOS/draw.io",
        ):
            if path.is_file():
                return str(path)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preview", "final", "svg", "pdf"))
    parser.add_argument("input", type=Path, help="source .drawio file")
    parser.add_argument("output", nargs="?", type=Path, help="destination; defaults beside the input")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"ERROR: Draw.io file not found: {args.input}", file=sys.stderr)
        return 2
    executable = find_drawio()
    if not executable:
        print("BLOCKED: diagrams.net Desktop CLI was not found; set DRAWIO to its executable path.", file=sys.stderr)
        return 3

    extension, options = {
        "preview": ("png", ["-x", "-f", "png", "-s", "2"]),
        "final": ("png", ["-x", "-f", "png", "-s", "4.17", "-b", "15"]),
        "svg": ("svg", ["-x", "-f", "svg", "-b", "15"]),
        "pdf": ("pdf", ["-x", "-f", "pdf", "--crop"]),
    }[args.mode]
    output = args.output or args.input.with_suffix(f".{extension}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [executable, *options, "-o", str(output), str(args.input)]
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=EXPORT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(
            f"BLOCKED: Draw.io export exceeded {EXPORT_TIMEOUT_SECONDS}s. "
            "Close any hung Draw.io export and retry one diagram at a time.",
            file=sys.stderr,
        )
        return 3
    except OSError as exc:
        print(f"ERROR: could not start diagrams.net Desktop: {exc}", file=sys.stderr)
        return 1
    if result.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print(f"ERROR: Draw.io export failed: {output}", file=sys.stderr)
        return 1
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
