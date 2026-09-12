import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("promptly", ROOT / "scripts/promptly.py")
promptly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promptly)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="promptly-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def test_committed_bundles_match_canonical_sources(self):
        self.assertEqual(promptly.build(check=True), [])

    def test_each_bundle_contains_exactly_one_unchanged_core(self):
        core = (ROOT / "core/prompt.md").read_text(encoding="utf-8").strip()
        for harness, entry in promptly.ENTRYPOINTS.items():
            body = promptly.render()[entry].decode()
            self.assertEqual(body.count(core), 1, harness)
            self.assertNotIn("{{CORE", body)

    def test_native_argument_forwarding_has_one_literal_slot(self):
        for harness in ("claude", "opencode"):
            content = promptly.render()[promptly.ENTRYPOINTS[harness]].decode()
            self.assertEqual(content.count("$ARGUMENTS"), 1)
            self.assertTrue(content.rstrip().endswith("$ARGUMENTS"))
            self.assertNotIn("!`", content)  # No shell preprocessing in shipped templates.
        for harness in ("codex", "generic"):
            content = promptly.render()[promptly.ENTRYPOINTS[harness]].decode()
            self.assertNotIn("$ARGUMENTS", content)

    def test_build_check_detects_drift_without_writing(self):
        shutil.copytree(ROOT / "core", self.base / "core")
        shutil.copytree(ROOT / "adapters", self.base / "adapters")
        promptly.build(self.base)
        entry = self.base / "bundles/codex/promptly/SKILL.md"
        entry.write_text("user edit", encoding="utf-8")
        stale = promptly.build(self.base, check=True)
        self.assertEqual(stale, ["codex/promptly/SKILL.md"])
        self.assertEqual(entry.read_text(), "user edit")

    def test_invalid_adapter_is_rejected(self):
        shutil.copytree(ROOT / "core", self.base / "core")
        shutil.copytree(ROOT / "adapters", self.base / "adapters")
        (self.base / "adapters/codex.md").write_text("Missing template slots")
        with self.assertRaisesRegex(ValueError, "Invalid adapter"):
            promptly.build(self.base)
        self.assertFalse((self.base / "bundles").exists())

    def test_install_with_spaces_and_unicode_and_reinstall(self):
        dest = self.base / "a space café" / "promptly"
        installed = promptly.install("codex", dest)
        self.assertEqual(len(installed), 2)
        self.assertTrue((dest / "SKILL.md").exists())
        self.assertTrue((dest / "agents/openai.yaml").exists())
        self.assertEqual(promptly.install("codex", dest), [])

    def test_every_harness_installs_only_expected_files(self):
        for harness in promptly.ENTRYPOINTS:
            dest = self.base / harness
            paths = promptly.install(harness, dest)
            self.assertEqual(len(paths), 2 if harness == "codex" else 1)
            self.assertTrue((dest / ("promptly.md" if harness == "opencode" else "SKILL.md")).exists())

    def test_dry_run_does_not_create_directories(self):
        dest = self.base / "uncreated" / "skill"
        self.assertEqual(len(promptly.install("codex", dest, dry_run=True)), 2)
        self.assertFalse(dest.exists())

    def test_conflict_preflight_leaves_all_files_untouched(self):
        dest = self.base / "skill"
        (dest / "agents").mkdir(parents=True)
        metadata = dest / "agents/openai.yaml"
        metadata.write_text("Existing unrelated metadata", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Existing file differs"):
            promptly.install("codex", dest)
        self.assertFalse((dest / "SKILL.md").exists())
        self.assertEqual(metadata.read_text(), "Existing unrelated metadata")

    def test_forced_updates_back_up_without_overwriting_old_backups(self):
        dest = self.base / "skill"
        dest.mkdir()
        entry = dest / "SKILL.md"
        entry.write_bytes(b"old skill")
        (dest / "SKILL.md.promptly-backup").write_bytes(b"older backup")
        (dest / "my-notes.md").write_bytes(b"keep")
        promptly.install("generic", dest, force=True)
        self.assertEqual((dest / "SKILL.md.promptly-backup").read_bytes(), b"older backup")
        self.assertEqual((dest / "SKILL.md.promptly-backup.1").read_bytes(), b"old skill")
        self.assertEqual((dest / "my-notes.md").read_bytes(), b"keep")

    def test_linked_installation_is_refused(self):
        target = self.base / "target"
        target.mkdir()
        linked = self.base / "linked"
        try:
            linked.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks is not permitted on this host")
        with self.assertRaisesRegex(ValueError, "Refusing linked"):
            promptly.install("generic", linked)
        self.assertEqual(list(target.iterdir()), [])

    def test_regular_file_cannot_be_replaced_by_directory(self):
        dest = self.base / "skill"
        (dest / "SKILL.md").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "Not a regular file"):
            promptly.install("generic", dest, force=True)

    def test_invalid_metadata_parent_does_not_partially_install(self):
        dest = self.base / "skill"
        dest.mkdir()
        (dest / "agents").write_bytes(b"not a directory")
        with self.assertRaisesRegex(ValueError, "Parent is not a directory"):
            promptly.install("codex", dest)
        self.assertFalse((dest / "SKILL.md").exists())

    def test_project_destinations(self):
        expected = {"codex": ".agents/skills/promptly", "generic": ".agents/skills/promptly",
                    "claude": ".claude/skills/promptly", "opencode": ".opencode/commands"}
        for harness, relative in expected.items():
            dest = promptly.destination(harness, "project", self.base, self.base, {})
            self.assertEqual(dest, self.base / relative)

    def test_user_destinations_and_xdg_config(self):
        home = self.base / "home"
        config = self.base / "custom-config"
        self.assertEqual(promptly.destination("codex", "user", self.base, home, {}),
                         home / ".agents/skills/promptly")
        self.assertEqual(promptly.destination("claude", "user", self.base, home, {}),
                         home / ".claude/skills/promptly")
        self.assertEqual(promptly.destination("opencode", "user", self.base, home,
                                             {"XDG_CONFIG_HOME": str(config)}),
                         config / "opencode/commands")
        with self.assertRaisesRegex(ValueError, "absolute"):
            promptly.destination("opencode", "user", self.base, home, {"XDG_CONFIG_HOME": "relative"})

    def test_cli_dry_run_and_errors(self):
        script = str(ROOT / "scripts/promptly.py")
        dest = self.base / "cli destination"
        result = subprocess.run([sys.executable, script, "install", "claude",
                                 "--destination", str(dest), "--dry-run"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Would write", result.stdout)
        self.assertFalse(dest.exists())
        result = subprocess.run([sys.executable, script, "install", "unknown"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


class EvaluationToolTests(unittest.TestCase):
    def test_cases_have_unique_ids_and_explicit_semantic_criteria(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text())
        self.assertGreaterEqual(len(cases), 15)
        self.assertLessEqual(len(cases), 25)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        for case in cases:
            self.assertTrue(case["must"] and case["must_not"])
            self.assertGreater(case["max_words"], 0)

    def test_blind_preparation_omits_grading_expectations(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate.py"),
                                 "prepare", "--preview"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        cases = json.loads(result.stdout)
        for case in cases:
            self.assertEqual(set(case), {"id", "input", "context"})
        self.assertIn("--show", cases[0]["input"])
        self.assertEqual(cases[17]["input"], "/promptly --compact --deep add trading")


if __name__ == "__main__":
    unittest.main()
