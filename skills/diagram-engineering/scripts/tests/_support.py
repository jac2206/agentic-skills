"""Local, disposable fixtures; inherit workspace permissions on Windows."""

import importlib.util
from pathlib import Path
import shutil
import sys
import unittest
import uuid


def load_script(name):
    path = Path(__file__).resolve().parents[1] / (name + ".py")
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("diagram_test_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self):
        self.test_directory = Path(__file__).resolve().parent
        self.workspace = self.test_directory / (".diagram-test-" + uuid.uuid4().hex)
        self.workspace.mkdir(mode=0o777)
        self.addCleanup(self.cleanup_workspace)

    def cleanup_workspace(self):
        if self.workspace.resolve().parent != self.test_directory:
            raise RuntimeError("Fixture cleanup escaped its test directory")
        shutil.rmtree(self.workspace)

    def write(self, name, content):
        path = self.workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path
