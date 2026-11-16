"""Attempt-record and renderer-boundary tests; all process launches are mocked."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

from _support import WorkspaceTestCase, load_script

renderer = load_script("render_diagram")


class RenderGuardTests(WorkspaceTestCase):
    def setUp(self):
        super().setUp()
        self.source = self.write("first.drawio", "<mxfile/>")
        self.second = self.write("second.drawio", "<mxfile/>")
        self.mermaid = self.write("diagram.mmd", "flowchart LR\nA --> B\n")
        self.cli = self.write("mermaid-cli.mjs", "// Discovery fixture; never executed.\n")
        self.record = self.workspace / "attempts.json"
        self.commands = []
        blocker = patch.object(renderer.subprocess, "run", side_effect=AssertionError("Unexpected real process launch"))
        blocker.start()
        self.addCleanup(blocker.stop)

    def fake_success(self, command):
        self.commands.append(command)
        output = Path(command[command.index("-o") + 1] if "-o" in command else command[-1])
        # Nonempty synthetic bytes test file handling, not rendered image validity.
        output.write_bytes(b"simulated preview")
        return {"code": 0, "stdout": "", "stderr": ""}

    def run_guard(self, **options):
        source = options.pop("input", self.source)
        defaults = {"tool": "drawio", "input": source, "output": source.with_suffix(".png"),
                    "attempt_record": self.record, "execute": self.fake_success}
        defaults.update(options)
        return renderer.render_once(**defaults)

    def test_drawio_success_uses_python_and_persists_receipt(self):
        result = self.run_guard()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(self.commands[0][:2], [sys.executable, "-B"])
        self.assertEqual(Path(self.commands[0][2]).name, "render_drawio.py")
        attempt = json.loads(self.record.read_text())["tools"]["drawio"][0]
        self.assertEqual(attempt["status"], "passed")
        self.assertTrue(attempt["started"] and attempt["finished"])
        self.assertFalse(self.record.with_name("attempts.json.lock").exists())

    def test_same_file_cannot_be_rendered_twice(self):
        self.run_guard()
        original = self.record.read_bytes()
        result = self.run_guard(output=self.workspace / "another.png")
        self.assertEqual(result["code"], 3)
        self.assertEqual(len(self.commands), 1)
        self.assertEqual(self.record.read_bytes(), original)

    def test_success_allows_another_file_with_same_renderer(self):
        self.run_guard()
        self.assertEqual(self.run_guard(input=self.second)["status"], "passed")
        self.assertEqual(len(self.commands), 2)

    def test_failure_blocks_other_files_but_not_another_renderer(self):
        execute = Mock(return_value={"code": 1, "stderr": "simulated failure"})
        self.assertEqual(self.run_guard(execute=execute)["status"], "failed")
        self.assertEqual(self.run_guard(input=self.second, execute=execute)["code"], 3)
        execute.assert_called_once()
        result = self.run_guard(tool="mermaid", input=self.mermaid, mermaid_cli=self.cli, node="fake-node")
        self.assertEqual(result["status"], "passed")
        self.assertEqual(self.commands[0][0], "fake-node")

    def test_zero_exit_requires_a_nonempty_preview(self):
        for empty in (False, True):
            with self.subTest(empty_file=empty):
                output = self.workspace / f"empty-{empty}.png"

                def execute(command):
                    if empty:
                        output.write_bytes(b"")
                    return {"code": 0}

                result = self.run_guard(output=output, attempt_record=self.workspace / f"record-{empty}.json", execute=execute)
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["code"], 1)
                self.assertIsNone(result["output"])

    def test_interrupted_attempt_and_active_lock_block_execution(self):
        self.record.write_text(json.dumps({"version": 1, "tools": {"drawio": [
            {"input": str(self.source), "status": "started"}]}}), encoding="utf-8")
        self.assertEqual(self.run_guard(input=self.second)["code"], 3)
        original = self.record.read_bytes()
        lock = self.write("attempts.json.lock", "active")
        self.assertEqual(self.run_guard()["code"], 3)
        self.assertTrue(lock.exists())
        self.assertEqual(self.record.read_bytes(), original)
        self.assertEqual(self.commands, [])

    def test_invalid_records_never_launch_or_overwrite_history(self):
        values = ["not JSON", "[]", '{"version": 2, "tools": {}}', '{"version": 1, "tools": []}',
                  '{"version": 1, "tools": {"drawio": {}}}',
                  '{"version": 1, "tools": {"drawio": [{"status": "unknown", "input": "x"}]}}']
        for index, value in enumerate(values):
            with self.subTest(value=value):
                path = self.write(f"invalid-{index}.json", value)
                with self.assertRaises(ValueError):
                    self.run_guard(attempt_record=path)
                self.assertEqual(path.read_text(), value)
                self.assertFalse(path.with_name(path.name + ".lock").exists())
        self.assertEqual(self.commands, [])

    def test_invalid_inputs_and_existing_preview_are_preserved(self):
        preview = self.write("existing.png", "keep this preview")
        cases = [{"tool": "unknown"}, {"input": self.workspace / "missing.drawio"},
                 {"input": self.mermaid}, {"output": self.workspace / "wrong.txt"},
                 {"attempt_record": self.source}, {"output": preview}]
        for options in cases:
            with self.subTest(options=options):
                with self.assertRaises(ValueError):
                    self.run_guard(**options)
        self.assertEqual(preview.read_text(), "keep this preview")
        self.assertEqual(self.source.read_text(), "<mxfile/>")
        self.assertEqual(self.commands, [])

    def test_mermaid_discovery_reads_manifest_without_launching_node(self):
        package = self.workspace / "node_modules/@mermaid-js/mermaid-cli"
        entry = self.write("node_modules/@mermaid-js/mermaid-cli/src/cli.js", "// Not executed.\n")
        for bin_value in ({"mmdc": "src/cli.js"}, "src/cli.js"):
            with self.subTest(bin_value=bin_value):
                (package / "package.json").write_text(json.dumps({"name": "@mermaid-js/mermaid-cli", "bin": bin_value}), encoding="utf-8")
                with patch.object(renderer.shutil, "which", return_value=None):
                    self.assertEqual(renderer.mermaid_entry(tooling_directory=self.workspace), entry.resolve())
        wrapper = self.write("mmdc.cmd", "not executed")
        with self.assertRaises(ValueError):
            renderer.mermaid_entry(wrapper)

    def test_missing_mermaid_runtime_records_failure_and_blocks_retry(self):
        with patch.object(renderer.shutil, "which", return_value=None):
            result = self.run_guard(tool="mermaid", input=self.mermaid, mermaid_cli=self.cli)
        self.assertEqual(result["status"], "failed")
        self.assertIn("Node.js", result["reason"])
        self.assertEqual(self.run_guard(tool="mermaid", input=self.mermaid, mermaid_cli=self.cli, node="fake-node")["code"], 3)
        self.assertEqual(self.commands, [])

    def test_discovery_and_launch_errors_are_persisted_before_retry(self):
        def execute(command):
            attempt = json.loads(self.record.read_text())["tools"]["drawio"][0]
            self.assertEqual(attempt["status"], "started")
            raise OSError("simulated unavailable renderer")

        self.assertEqual(self.run_guard(execute=execute)["status"], "failed")
        self.assertEqual(self.run_guard(input=self.second)["code"], 3)
        with patch.object(renderer, "mermaid_entry", side_effect=ValueError("CLI unavailable")):
            result = self.run_guard(tool="mermaid", input=self.mermaid)
        self.assertEqual(result["status"], "failed")
        history = json.loads(self.record.read_text())["tools"]
        self.assertEqual(history["drawio"][0]["status"], "failed")
        self.assertEqual(history["mermaid"][0]["status"], "failed")

    def test_execute_process_handles_timeout_os_error_and_nonzero_exit(self):
        command = ["fake-renderer", "input with spaces"]
        for error in (OSError("missing"), subprocess.TimeoutExpired(command, 100)):
            with self.subTest(error=error):
                with patch.object(renderer.subprocess, "run", side_effect=error):
                    self.assertEqual(renderer.execute_process(command)["code"], 1)
        completed = subprocess.CompletedProcess(command, 7, stdout="out", stderr="err")
        with patch.object(renderer.subprocess, "run", return_value=completed) as run:
            self.assertEqual(renderer.execute_process(command), {"code": 7, "stdout": "out", "stderr": "err"})
            self.assertFalse(run.call_args.kwargs["shell"])
            self.assertEqual(run.call_args.kwargs["timeout"], 100)

    def test_cli_reports_validation_and_blocked_status(self):
        options = ["--tool", "drawio", "--input", str(self.workspace / "missing.drawio"),
                   "--output", str(self.workspace / "preview.png"), "--attempt-record", str(self.record)]
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(renderer.main(options), 2)
            with patch.object(renderer, "render_once", return_value={"code": 3, "status": "not run"}):
                self.assertEqual(renderer.main(options), 3)


if __name__ == "__main__":
    unittest.main()
