"""Read-only structural checks for the repository's canonical component profiles."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ModuleNotFoundError:
    yaml = None


NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
REFERENCE = re.compile(r"(skill|agent|workflow)/[a-z0-9]+(?:-[a-z0-9]+)*\Z")
COMMON = {"contract_version", "kind", "name", "description", "version", "status", "dependencies"}
PROCESS = {"when_to_use", "when_not_to_use", "inputs", "preconditions", "outputs",
           "steps", "constraints", "failure_behavior", "quality_criteria", "validation"}
STEP = {"id", "uses", "needs", "inputs", "outputs", "instructions", "completion", "on_failure"}


class Invalid(ValueError):
    """An actionable structural error, not an execution failure."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def mapping(value, label, allow_empty=False):
    require(isinstance(value, dict), f"{label}: expected a mapping")
    require(allow_empty or bool(value), f"{label}: must not be empty")
    require(all(isinstance(k, str) and NAME.fullmatch(k) for k in value),
            f"{label}: names must use lowercase kebab-case")


def fields(value, expected, label):
    require(isinstance(value, dict), f"{label}: expected a mapping")
    require(set(value) == expected,
            f"{label}: missing fields {sorted(expected - set(value))}; "
            f"unsupported fields {sorted(set(value) - expected)}")


def strings(value, label, allow_empty=False):
    require(isinstance(value, list) and (allow_empty or bool(value)),
            f"{label}: expected {'a possibly empty' if allow_empty else 'a nonempty'} list")
    require(all(text(item) for item in value), f"{label}: entries must be nonempty strings")


def load_yaml(source):
    require(yaml is not None, "PyYAML is required; see validators/requirements.txt")

    class UniqueLoader(yaml.SafeLoader):
        pass

    # Restrict implicit booleans to YAML 1.2 spellings; do not coerce yes/no/on/off.
    UniqueLoader.yaml_implicit_resolvers = {
        key: [(tag, pattern) for tag, pattern in rules
              if tag != "tag:yaml.org,2002:bool"]
        for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    UniqueLoader.add_implicit_resolver("tag:yaml.org,2002:bool",
                                      re.compile(r"(?:true|True|TRUE|false|False|FALSE)\Z"), list("tTfF"))

    def unique_mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            require(isinstance(key, str), "YAML mapping keys must be strings")
            require(key not in result, f"Duplicate YAML key: {key}")
            result[key] = loader.construct_object(value_node)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    for event in yaml.parse(source):
        require(not isinstance(event, yaml.events.AliasEvent)
                and not getattr(event, "anchor", None) and not getattr(event, "tag", None),
                "YAML tags, anchors and aliases are unsupported")
    value = yaml.load(source, Loader=UniqueLoader)
    require(isinstance(value, dict), "Expected a single YAML mapping document")
    return value


def frontmatter(content):
    lines = content.splitlines()
    require(bool(lines) and lines[0] == "---", "Missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise Invalid("Unterminated YAML frontmatter") from exc
    return load_yaml("\n".join(lines[1:end]))


def check_metadata(data, kind, directory):
    require(text(data.get("name")) and NAME.fullmatch(data["name"]), "Invalid or missing name")
    require(text(data.get("description")), "Missing nonempty description")
    if kind == "skill":
        require("license" not in data, "Skill license fields require an adopted licensing policy")
        metadata = data.get("metadata", {})
        require(isinstance(metadata, dict), "Skill metadata must be a mapping")
        if "version" in metadata:
            require(isinstance(metadata["version"], str) and VERSION.fullmatch(metadata["version"]),
                    "Skill metadata.version must be a MAJOR.MINOR.PATCH string")
        return
    expected = COMMON | PROCESS if kind == "workflow" else COMMON
    fields(data, expected, kind)
    require(data["kind"] == kind, f"kind must be {kind}")
    require(data["contract_version"] == ("2.0" if kind == "workflow" else "1.0"),
            f"Unsupported {kind} contract_version")
    require(data["name"] == directory, "Declared name must match the package directory")
    require(isinstance(data["version"], str) and VERSION.fullmatch(data["version"]),
            "version must be a MAJOR.MINOR.PATCH string")
    require(data["status"] in ("draft", "ready", "deprecated"), "Invalid status")
    strings(data["dependencies"], "dependencies", allow_empty=True)
    require(all(REFERENCE.fullmatch(ref) for ref in data["dependencies"]),
            "Dependencies must use kind/name references")
    require(len(data["dependencies"]) == len(set(data["dependencies"])), "Duplicate dependencies")


def check_graph(graph):
    """Use an iterative traversal so long valid graphs do not exhaust recursion."""
    for node, predecessors in graph.items():
        for predecessor in predecessors:
            require(predecessor in graph, f"{node}: missing dependency {predecessor}")
    done = set()
    for node in graph:
        active = set()
        stack = [(node, False)]
        while stack:
            current, leaving = stack.pop()
            if leaving:
                active.remove(current)
                done.add(current)
            elif current not in done:
                require(current not in active, f"Dependency cycle at {current}")
                active.add(current)
                stack.append((current, True))
                stack.extend((item, False) for item in graph[current])


def check_workflow(data):
    for key in ("when_to_use", "when_not_to_use", "constraints", "quality_criteria", "validation"):
        strings(data[key], key)
    strings(data["preconditions"], "preconditions", allow_empty=True)
    require(text(data["failure_behavior"]), "failure_behavior must be nonempty text")
    mapping(data["inputs"], "inputs")
    for name, spec in data["inputs"].items():
        fields(spec, {"description", "format", "required"}, f"inputs.{name}")
        require(text(spec["description"]) and text(spec["format"]) and type(spec["required"]) is bool,
                f"inputs.{name}: require description, format and boolean required")
    require(isinstance(data["steps"], list) and bool(data["steps"]), "steps must be a nonempty list")
    steps = {}
    used = set()
    for step in data["steps"]:
        fields(step, STEP, "step")
        require(text(step["id"]) and NAME.fullmatch(step["id"]), "Invalid step ID")
        sid = step["id"]
        require(sid not in steps, f"Duplicate step ID: {sid}")
        strings(step["needs"], f"{sid}.needs", allow_empty=True)
        require(len(step["needs"]) == len(set(step["needs"])), f"{sid}: duplicate predecessors")
        require(text(step["uses"]) and REFERENCE.fullmatch(step["uses"])
                and step["uses"].split("/", 1)[0] in ("skill", "agent"), f"{sid}: invalid uses reference")
        require(step["uses"] in data["dependencies"], f"{sid}: uses is absent from dependencies")
        used.add(step["uses"])
        require(text(step["instructions"]) and text(step["completion"]), f"{sid}: missing scope or completion")
        require(step["on_failure"] == "block_dependents", f"{sid}: unsupported on_failure")
        mapping(step["inputs"], f"{sid}.inputs", allow_empty=True)
        mapping(step["outputs"], f"{sid}.outputs")
        for name, spec in step["outputs"].items():
            fields(spec, {"description", "format"}, f"{sid}.outputs.{name}")
            require(all(text(v) for v in spec.values()), f"{sid}.outputs.{name}: empty description or format")
        steps[sid] = step
    require(used == set(data["dependencies"]), "Workflow has unused required dependencies")
    graph = {sid: step["needs"] for sid, step in steps.items()}
    check_graph(graph)

    def source_output(source):
        require(text(source), "Source references must be nonempty strings")
        parts = source.split(".")
        require(len(parts) == 4 and parts[0] == "steps" and parts[2] == "outputs",
                f"Invalid step output source: {source}")
        require(parts[1] in steps and parts[3] in steps[parts[1]]["outputs"],
                f"Unknown step output: {source}")
        return parts[1], steps[parts[1]]["outputs"][parts[3]]

    for sid, step in steps.items():
        ancestors, pending = set(), list(step["needs"])
        while pending:
            predecessor = pending.pop()
            if predecessor not in ancestors:
                ancestors.add(predecessor)
                pending.extend(graph[predecessor])
        for source in step["inputs"].values():
            require(text(source), f"{sid}: source must be a string")
            if source.startswith("inputs."):
                require(source[7:] in data["inputs"], f"{sid}: unknown workflow input {source}")
            else:
                predecessor, _ = source_output(source)
                require(predecessor in ancestors, f"{sid}: source is not a reachable predecessor: {source}")
    mapping(data["outputs"], "outputs")
    for name, spec in data["outputs"].items():
        fields(spec, {"description", "format", "source"}, f"outputs.{name}")
        require(all(text(v) for v in spec.values()), f"outputs.{name}: fields must be nonempty strings")
        _, upstream = source_output(spec["source"])
        require(spec["format"] == upstream["format"], f"outputs.{name}: source format mismatch")


def prose(content):
    # Best-effort inline Markdown links only; fenced examples and inline code are excluded.
    return re.sub(r"`[^`\n]+`", "", re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*$", "", content))


@dataclass
class Report:
    components: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def validate_repository(root):
    require(yaml is not None, "PyYAML is required; see validators/requirements.txt")
    root = Path(root).resolve()
    report = Report()

    def issue(path, message, warning=False):
        label = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
        (report.warnings if warning else report.errors).append(f"{label}: {message}")

    def inspect_links(package):
        for path in sorted(package.rglob("*.md")):
            if not path.resolve().is_relative_to(package.resolve()):
                issue(path, "Resource resolves outside its package")
                continue
            if "templates" in path.relative_to(package).parts[:-1]:
                # Payload links may describe the generated artifact's future directory.
                # Links TO these templates are still checked from their callers.
                continue
            content = prose(path.read_text(encoding="utf-8-sig"))
            for target in re.findall(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", content):
                target = target.strip("<>")
                if urlsplit(target).scheme or target.startswith(("#", "//")) or "<" in target:
                    continue
                target_path = unquote(target.split("#", 1)[0])
                resolved = (path.parent / target_path).resolve()
                if not resolved.is_relative_to(package.resolve()):
                    issue(path, f"Link outside package needs portability review: {target}", warning=True)
                elif not resolved.is_file() and not resolved.is_dir():
                    issue(path, f"Missing local resource: {target}")

    require(root.is_dir() and (root / "skills").is_dir(), "Root must contain a skills/ directory")
    for kind, folder, entry in (("skill", "skills", "SKILL.md"), ("agent", "agents", "AGENT.md"),
                                ("workflow", "workflows", "workflow.yaml")):
        for path in sorted((root / folder).glob(f"*/{entry}")):
            if path.parent.name.startswith("."):
                continue
            try:
                require(path.resolve().is_relative_to(path.parent.absolute()), "Entry point escapes its package")
                content = path.read_text(encoding="utf-8-sig")
                data = load_yaml(content) if kind == "workflow" else frontmatter(content)
                check_metadata(data, kind, path.parent.name)
                if kind == "workflow":
                    check_workflow(data)
                if kind == "skill":
                    guide_path = path.parent / "examples" / "usage.md"
                    require(guide_path.is_file(), "Missing examples/usage.md")
                    require(guide_path.resolve().is_relative_to(path.parent.resolve()),
                            "Usage guide resolves outside its package")
                    guide = prose(guide_path.read_text(encoding="utf-8-sig"))
                    headings = re.findall(r"^## (.+?)\s*$", guide, re.M)
                    require(headings.count("Espa\u00f1ol") == headings.count("English") == 1
                            and headings.index("Espa\u00f1ol") < headings.index("English"),
                            "Usage guide needs one Spanish-first and one English section")
                    require("](#espa\u00f1ol)" in guide and "](#english)" in guide,
                            "Usage guide needs Markdown language navigation")
                ref = f"{kind}/{data['name']}"
                require(ref not in report.components, f"Duplicate component identity: {ref}")
                report.components[ref] = (path, data)
                inspect_links(path.parent)
            except (Invalid, OSError, UnicodeError, yaml.YAMLError) as exc:
                issue(path, str(exc))
    for path in sorted((root / "workflows").glob("*/WORKFLOW.md")):
        issue(path, "Unsupported legacy entry point; migrate to workflow.yaml profile 2.0")
    graph = {ref: data.get("dependencies", []) if not ref.startswith("skill/") else []
             for ref, (_, data) in report.components.items()}
    try:
        check_graph(graph)
    except Invalid as exc:
        issue(root, str(exc))
    template = root / "templates" / "workflow-template.yaml"
    if template.is_file():
        try:
            data = load_yaml(template.read_text(encoding="utf-8-sig"))
            check_metadata(data, "workflow", data.get("name"))
            check_workflow(data)
        except (Invalid, OSError, UnicodeError, yaml.YAMLError) as exc:
            issue(template, str(exc))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Repository root; defaults to this script's repository")
    args = parser.parse_args(argv)
    if yaml is None:
        print("ERROR: PyYAML is unavailable. Install validators/requirements.txt in your tooling environment.",
              file=sys.stderr)
        return 2
    try:
        report = validate_repository(args.root)
    except (Invalid, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for message in report.errors:
        print(f"ERROR: {message}")
    for message in report.warnings:
        print(f"WARNING: {message}")
    counts = {kind: sum(ref.startswith(kind + "/") for ref in report.components)
              for kind in ("skill", "agent", "workflow")}
    print(f"Checked {counts['skill']} Skills, {counts['agent']} agents, {counts['workflow']} workflows; "
          f"{len(report.errors)} errors, {len(report.warnings)} warnings.")
    print("Static checks only; semantic correctness, authority and execution evidence require review.")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
