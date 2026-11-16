"""Regression checks using isolated, deliberately malformed component packages."""

import copy
import io
from pathlib import Path
import sys
import shutil
import uuid
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_components as validator


def workflow():
    def step(sid, needs):
        return {
            "id": sid, "uses": "skill/html-presentations", "needs": needs,
            "inputs": {"scope": "inputs.scope"},
            "outputs": {"result": {"description": "Evidence", "format": "markdown"}},
            "instructions": "Review only the supplied scope.",
            "completion": "The scoped evidence is reported.", "on_failure": "block_dependents",
        }
    return {
        "contract_version": "2.0", "kind": "workflow", "name": "review", "description": "Review scope.",
        "version": "0.1.0", "status": "draft", "dependencies": ["skill/html-presentations"],
        "when_to_use": ["Two assessments are required."], "when_not_to_use": ["One assessment suffices."],
        "inputs": {"scope": {"description": "Scope", "format": "text", "required": True}},
        "preconditions": [],
        "outputs": {"result": {"description": "Report", "format": "markdown",
                               "source": "steps.second.outputs.result"}},
        "steps": [step("first", []), step("second", ["first"])],
        "constraints": ["Read-only."], "failure_behavior": "Block dependents and retain evidence.",
        "quality_criteria": ["Evidence supports the result."], "validation": ["Review sources."],
    }


class SchemaTests(unittest.TestCase):
    def test_valid_workflow_and_ancestor_mapping(self):
        data = workflow()
        data["steps"][1]["inputs"]["previous"] = "steps.first.outputs.result"
        validator.check_metadata(data, "workflow", "review")
        validator.check_workflow(data)

    def test_invalid_workflow_cases(self):
        def set_step(data, key, value):
            data["steps"][1][key] = value

        cases = {
            "duplicate step": lambda d: set_step(d, "id", "first"),
            "missing predecessor": lambda d: set_step(d, "needs", ["absent"]),
            "duplicate predecessor": lambda d: set_step(d, "needs", ["first", "first"]),
            "cycle": lambda d: d["steps"][0].update(needs=["second"]),
            "self edge": lambda d: set_step(d, "needs", ["second"]),
            "unreachable output": lambda d: set_step(d, "inputs", {"scope": "steps.second.outputs.result"}),
            "undeclared input": lambda d: set_step(d, "inputs", {"scope": "inputs.absent"}),
            "unknown output": lambda d: set_step(d, "inputs", {"scope": "steps.first.outputs.absent"}),
            "nonstring source": lambda d: set_step(d, "inputs", {"scope": []}),
            "executable expression": lambda d: set_step(d, "inputs", {"scope": "${inputs.scope}"}),
            "undeclared uses": lambda d: set_step(d, "uses", "skill/absent"),
            "unsupported tool step": lambda d: set_step(d, "uses", "tool/read"),
            "implicit retries": lambda d: set_step(d, "on_failure", "retry"),
            "unused dependency": lambda d: d["dependencies"].append("agent/unused"),
            "missing final output": lambda d: d["outputs"]["result"].update(source="steps.absent.outputs.result"),
            "incompatible final format": lambda d: d["outputs"]["result"].update(format="json"),
            "nonboolean required": lambda d: d["inputs"]["scope"].update(required="true"),
            "malformed step": lambda d: d.update(steps=["invalid"]),
            "missing output metadata": lambda d: d["steps"][0]["outputs"].update(result=[]),
        }
        for label, mutate in cases.items():
            with self.subTest(label=label):
                data = copy.deepcopy(workflow())
                mutate(data)
                with self.assertRaises(validator.Invalid):
                    validator.check_workflow(data)

    def test_metadata_rejects_unsupported_fields_versions_and_types(self):
        cases = [{"contract_version": "1.0"}, {"version": 1}, {"status": "production"},
                 {"version": "01.0.0"}, {"dependencies": ["skill/x", "skill/x"]},
                 {"dependencies": ["tools/read"]}, {"owner": "team"}]
        for change in cases:
            with self.subTest(change=change):
                data = workflow()
                data.update(change)
                with self.assertRaises(validator.Invalid):
                    validator.check_metadata(data, "workflow", "review")

    def test_yaml_rejects_ambiguous_or_unsafe_documents(self):
        cases = ["name: x\nname: y", "name: &a x\nother: *a", "name: !!str x",
                 "? [a, b]\n: value", "name: [", "name: x\n---\nname: y", "- item"]
        for source in cases:
            with self.subTest(source=source):
                with self.assertRaises((validator.Invalid, validator.yaml.YAMLError)):
                    validator.load_yaml(source)

    def test_yaml_boolean_spellings(self):
        self.assertEqual(validator.load_yaml("enabled: yes\nother: true"), {"enabled": "yes", "other": True})

    def test_frontmatter_requires_closing_delimiter(self):
        with self.assertRaisesRegex(validator.Invalid, "Unterminated"):
            validator.frontmatter("---\nname: test")

    def test_graph_checks_missing_nodes_and_long_dags(self):
        validator.check_graph({str(i): [str(i - 1)] if i else [] for i in range(2000)})
        for graph in [{"a": ["missing"]}, {"a": ["b"], "b": ["a"]}, {"a": ["a"]}]:
            with self.assertRaises(validator.Invalid):
                validator.check_graph(graph)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        # Python 3.13's mode-0700 temporary directories can exclude restricted
        # Windows tokens. Inherit the workspace ACL instead; no sensitive data.
        test_directory = Path(__file__).resolve().parent
        self.root = test_directory / (".component-test-" + uuid.uuid4().hex)
        self.root.mkdir(mode=0o777)

        def cleanup():
            # Verify the absolute deletion boundary before recursive cleanup.
            if self.root.resolve().parent != test_directory:
                raise RuntimeError("Fixture cleanup escaped its test directory")
            shutil.rmtree(self.root)

        self.addCleanup(cleanup)
        self.skill = {"name": "html-presentations", "description": "Create presentations.",
                      "metadata": {"version": "1.0.0"}}
        self.write_skill("presentations", self.skill)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_skill(self, directory, data, body=""):
        self.write(f"skills/{directory}/SKILL.md",
                   "---\n" + validator.yaml.safe_dump(data) + "---\n" + body)
        self.write(f"skills/{directory}/examples/usage.md",
                   "[Espa\u00f1ol](#espa\u00f1ol) | [English](#english)\n"
                   "## Espa\u00f1ol\nPrompt.\n## English\nPrompt.\n")

    def report(self):
        return validator.validate_repository(self.root)

    def test_skill_name_differs_from_directory_and_templates_are_excluded(self):
        self.write("skills/presentations/templates/fake/SKILL.md", "not a skill")
        self.write("templates/example/SKILL.md", "not a skill")
        self.write("skills/.hidden/SKILL.md", "not a skill")
        report = self.report()
        self.assertEqual(report.errors, [])
        self.assertEqual(list(report.components), ["skill/html-presentations"])

    def test_valid_repository_with_workflow(self):
        self.write("workflows/review/workflow.yaml", validator.yaml.safe_dump(workflow()))
        self.assertEqual(self.report().errors, [])

    def test_validation_does_not_write_files(self):
        self.write("workflows/review/workflow.yaml", validator.yaml.safe_dump(workflow()))
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.report()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_workflow_template_is_checked_but_not_discovered(self):
        template = workflow()
        template["dependencies"] = ["skill/placeholder"]
        for step in template["steps"]:
            step["uses"] = "skill/placeholder"
        self.write("templates/workflow-template.yaml", validator.yaml.safe_dump(template))
        report = self.report()
        self.assertEqual(report.errors, [])
        self.assertEqual(len(report.components), 1)
        template["steps"][0]["on_failure"] = "retry"
        self.write("templates/workflow-template.yaml", validator.yaml.safe_dump(template))
        self.assertTrue(any("unsupported on_failure" in e for e in self.report().errors))

    def test_missing_and_duplicate_identities(self):
        self.write_skill("other", self.skill)
        self.assertTrue(any("Duplicate component" in e for e in self.report().errors))

    def test_missing_and_cyclic_required_components(self):
        agent = {"contract_version": "1.0", "kind": "agent", "name": "a", "description": "Review.",
                 "version": "0.1.0", "status": "draft", "dependencies": ["agent/b"]}
        self.write("agents/a/AGENT.md", "---\n" + validator.yaml.safe_dump(agent) + "---\n# Agent\n")
        self.assertTrue(any("missing dependency agent/b" in e for e in self.report().errors))
        agent.update(name="b", dependencies=["agent/a"])
        self.write("agents/b/AGENT.md", "---\n" + validator.yaml.safe_dump(agent) + "---\n# Agent\n")
        self.assertTrue(any("cycle" in e for e in self.report().errors))

    def test_usage_missing_or_wrong_order(self):
        guide = self.root / "skills/presentations/examples/usage.md"
        guide.unlink()
        self.assertTrue(any("Missing examples/usage.md" in e for e in self.report().errors))
        guide.write_text("## English\n## Espa\u00f1ol\n", encoding="utf-8")
        self.assertTrue(any("Spanish-first" in e for e in self.report().errors))

    def test_missing_navigation(self):
        self.write("skills/presentations/examples/usage.md", "## Espa\u00f1ol\n## English\n")
        self.assertTrue(any("navigation" in e for e in self.report().errors))

    def test_local_resources_and_external_package_links(self):
        self.write_skill("presentations", self.skill,
                         "[Missing](references/absent.md)\n[Authoring](../../README.md)\n"
                         "```md\n[Example](nonexistent.md)\n```\n")
        report = self.report()
        self.assertEqual(len(report.errors), 1)
        self.assertIn("Missing local resource", report.errors[0])
        self.assertEqual(len(report.warnings), 1)

    def test_template_payload_links_are_not_package_resources(self):
        self.write_skill("presentations", self.skill, "[Template](templates/output.md)")
        self.write("skills/presentations/templates/output.md", "[Output](../future-output.md)")
        report = self.report()
        self.assertEqual(report.errors + report.warnings, [])

    def test_legacy_workflow_is_an_error(self):
        self.write("workflows/old/WORKFLOW.md", "# Old workflow")
        self.assertTrue(any("legacy entry point" in e for e in self.report().errors))

    def test_invalid_file_does_not_hide_later_findings(self):
        self.write("agents/bad/AGENT.md", "---\nname: [\n---\n")
        self.write("workflows/review/workflow.yaml", "kind: workflow")
        self.assertEqual(len(self.report().errors), 2)

    def test_main_exit_codes(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(validator.main([str(self.root)]), 0)
            self.write("skills/presentations/SKILL.md", "not frontmatter")
            self.assertEqual(validator.main([str(self.root)]), 1)
            self.assertEqual(validator.main([str(self.root / "absent")]), 2)
            with patch.object(validator, "yaml", None):
                self.assertEqual(validator.main([str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
