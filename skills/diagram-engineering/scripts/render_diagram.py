#!/usr/bin/env python3
"""Guard Draw.io/Mermaid rendering with a persistent one-attempt task record.

Python 3.10+ and the standard library only. Mermaid CLI, when used, remains an
external installed tool with its own Node.js requirement. Nothing is installed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent


def execute_process(command):
    """Launch one process without a shell or visible Windows console."""
    try:
        result = subprocess.run(
            command, check=False, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=100, shell=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return {"code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"code": 1, "error": str(exc)}


def mermaid_entry(explicit=None, tooling_directory=None):
    """Read installed npm manifests without invoking Node, npm or a shell shim."""
    if explicit:
        path = Path(explicit).resolve()
        if not path.is_file() or path.suffix.lower() not in (".js", ".mjs", ".cjs"):
            raise ValueError("--mermaid-cli must name an existing CLI JavaScript entry, not a shell wrapper")
        return path

    start = Path(tooling_directory or Path.cwd()).resolve()
    folders = [start, *start.parents]
    installed_command = shutil.which("mmdc")
    if installed_command:
        location = Path(installed_command).resolve().parent
        folders.extend([location, *location.parents])
    checked = set()
    for folder in folders:
        for package in (folder / "node_modules" / "@mermaid-js" / "mermaid-cli",
                        folder / "@mermaid-js" / "mermaid-cli"):
            if package in checked:
                continue
            checked.add(package)
            manifest = package / "package.json"
            if not manifest.is_file():
                continue
            metadata = json.loads(manifest.read_text(encoding="utf-8-sig"))
            if metadata.get("name") != "@mermaid-js/mermaid-cli":
                continue
            executable = metadata.get("bin")
            if isinstance(executable, dict):
                executable = executable.get("mmdc")
            if not isinstance(executable, str) or not executable:
                raise ValueError("installed Mermaid CLI has no mmdc executable")
            return mermaid_entry(package / executable)
    raise ValueError("installed Mermaid CLI was not found; no renderer launched")


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def render_once(*, tool, input, output, attempt_record, mermaid_cli=None,
                tooling_directory=None, node=None, execute=execute_process):
    """Keep the version-1 JSON record compatible with earlier task receipts."""
    if tool not in ("drawio", "mermaid"):
        raise ValueError("--tool must be drawio or mermaid")
    source, preview, record_path = (Path(p).resolve() for p in (input, output, attempt_record))
    if not source.is_file():
        raise ValueError(f"input not found: {source}")
    if source.suffix.lower() != (".drawio" if tool == "drawio" else ".mmd"):
        raise ValueError("input extension does not match renderer")
    if preview.suffix.lower() not in (".png", ".svg", ".pdf"):
        raise ValueError("output must be PNG, SVG or PDF")
    if len({source, preview, record_path}) != 3:
        raise ValueError("input, preview and attempt record must use different paths")
    record_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = record_path.with_name(record_path.name + ".lock")
    try:
        lock = lock_path.open("x", encoding="utf-8")
    except FileExistsError:
        return {"code": 3, "status": "not run", "reason": "an attempt is active or its lock needs manual review; no renderer launched"}
    try:
        record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.exists() else {"version": 1, "tools": {}}
        if not isinstance(record, dict) or record.get("version") != 1 or not isinstance(record.get("tools"), dict):
            raise ValueError("invalid attempt record; no renderer launched")
        attempts = record["tools"].get(tool, [])
        if not isinstance(attempts, list) or any(
            not isinstance(a, dict) or a.get("status") not in ("started", "passed", "failed")
            or not isinstance(a.get("input"), str) for a in attempts
        ):
            raise ValueError("invalid attempt history; no renderer launched")
        if any(a["status"] != "passed" for a in attempts):
            return {"code": 3, "status": "not run", "reason": f"{tool} already failed or was interrupted in this task; no retry"}
        if any(Path(a["input"]).resolve() == source for a in attempts):
            return {"code": 3, "status": "not run", "reason": "this file already had its one rendering attempt"}
        if preview.exists():
            raise ValueError("preview destination already exists; choose a fresh output before attempting")
        attempt = {"input": str(source), "output": str(preview), "status": "started", "started": timestamp()}
        attempts.append(attempt)
        record["tools"][tool] = attempts

        def save():
            record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        save()  # Persist before discovery or launch; an interruption must not enable a retry.
        try:
            preview.parent.mkdir(parents=True, exist_ok=True)
            if tool == "drawio":
                mode = {".png": "preview", ".svg": "svg", ".pdf": "pdf"}[preview.suffix.lower()]
                command = [sys.executable, "-B", str(SCRIPT_DIRECTORY / "render_drawio.py"), mode, str(source), str(preview)]
            else:
                entry = mermaid_entry(mermaid_cli, tooling_directory)
                runtime = node or shutil.which("node")
                if not runtime:
                    raise ValueError("Mermaid CLI requires an existing Node.js runtime; no renderer launched")
                command = [str(runtime), str(entry), "-i", str(source), "-o", str(preview)]
            result = execute(command)
            valid_output = preview.is_file() and preview.stat().st_size > 0
            attempt["status"] = "passed" if result.get("code") == 0 and valid_output else "failed"
            attempt["command"], attempt["args"] = command[0], command[1:]
            attempt["detail"] = result.get("error") or result.get("stderr") or ("" if valid_output else "no nonempty preview produced")
            attempt["finished"] = timestamp()
            save()
            return {**result, "code": 0 if attempt["status"] == "passed" else 1,
                    "status": attempt["status"], "reason": attempt["detail"],
                    "output": str(preview) if attempt["status"] == "passed" else None}
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            attempt.update(status="failed", detail=str(exc), finished=timestamp())
            save()
            return {"code": 1, "status": "failed", "reason": str(exc), "output": None}
    finally:
        lock.close()
        lock_path.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=("drawio", "mermaid"))
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--attempt-record", required=True)
    parser.add_argument("--mermaid-cli", help="existing Mermaid CLI JavaScript entry; no .cmd wrapper")
    parser.add_argument("--tooling-directory", help="directory from which to locate installed Mermaid CLI")
    parser.add_argument("--node", help="existing Node.js executable, used only by external Mermaid CLI")
    options = parser.parse_args(argv)
    try:
        result = render_once(**vars(options))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result["code"]


if __name__ == "__main__":
    raise SystemExit(main())
