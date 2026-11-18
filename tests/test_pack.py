import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint = load('aso_lint').lint_listing


class PackTests(unittest.TestCase):
    def test_example_has_no_issues(self):
        self.assertEqual(lint(json.loads((ROOT / 'examples/listing.json').read_text())), [])

    def test_all_limits_at_boundary_and_over(self):
        module = load('aso_lint')
        for field, (store, key) in module.FIELDS.items():
            maximum = module.LIMITS[store][key]
            with self.subTest(field=field):
                self.assertFalse(any(i['severity'] == 'CRITICAL' for i in lint({field: 'a' * maximum})))
                self.assertTrue(any(i['severity'] == 'CRITICAL' for i in lint({field: 'a' * (maximum + 1)})))

    def test_vitals_exact_threshold_is_flagged(self):
        for field, threshold in [('playCrashRatePct', 1.09), ('playAnrRatePct', 0.47)]:
            with self.subTest(field=field):
                issues = lint({'playTitle': 'Timer', field: threshold})
                self.assertTrue(any(i['severity'] == 'CRITICAL' for i in issues))

    def test_missing_metrics_are_unknown(self):
        self.assertEqual(len([i for i in lint({'playTitle': 'Timer'}) if 'unknown' in i['msg']]), 2)

    def test_invalid_data_rejected(self):
        for value in [[], {}, {'iosName': None}, {'iosName': 'Timer', 'playAnrRatePct': float('nan')}, {'iosName': 'Timer', 'playAnrRatePct': True}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                lint(value)

    def test_keyword_phrases_and_repeats(self):
        issues = lint({'iosName': 'Focus Timer', 'iosKeywords': 'focus session,notes,notes'})
        self.assertTrue(any('focus, notes' in i['msg'] for i in issues))

    def test_ios_only_does_not_require_play_title(self):
        self.assertEqual(lint({'iosName': 'Timer'}), [])

    def test_sample_size_changes_with_effect_size(self):
        calculate = load('ab_test_planner').calculate_sample_size
        small = calculate(28, 5, 1500)
        large = calculate(28, 20, 1500)
        self.assertGreater(small['perVariant'], large['perVariant'])
        self.assertEqual(small['totalVisitors'], 2 * small['perVariant'])

    def test_launch_date_and_offsets(self):
        timeline = load('launch_checklist').build_timeline('2026-12-01')
        self.assertEqual(timeline[0]['date'], '2026-11-17')
        self.assertEqual(timeline[-1]['date'], '2026-12-08')

    def test_manifests_and_skill_metadata(self):
        plugin = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(plugin['name'], market['plugins'][0]['name'])
        self.assertTrue((ROOT / market['plugins'][0]['source']).is_dir())
        for file in [ROOT / 'SKILL.md', *(ROOT / 'skills').glob('*/SKILL.md')]:
            text = file.read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'), str(file))
            frontmatter = text.split('---', 2)[1]
            self.assertIn('name:', frontmatter)
            self.assertIn('description:', frontmatter)

    def _assert_installer_behavior(self, shell_name, shell):
        for runtime in ['claude', 'codex']:
            with self.subTest(shell=shell_name, runtime=runtime), tempfile.TemporaryDirectory() as directory:
                if shell_name == 'bash':
                    command = [shell, str(ROOT / 'install.sh'), runtime, directory]
                else:
                    command = [shell, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ROOT / 'install.ps1'), '-Runtime', runtime, '-DestinationRoot', directory]
                first = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(first.returncode, 0, first.stderr)
                target = Path(directory) / ('aso' if runtime == 'claude' else 'claude-aso')
                for entry in ['SKILL.md', 'CLAUDE.md', 'AGENTS.md', 'LICENSE', 'skills', 'agents', 'data', 'scripts', 'templates', 'extensions', 'docs', 'examples']:
                    self.assertTrue((target / entry).exists(), entry)
                lint_command = [
                    sys.executable,
                    str(target / 'scripts/aso_lint.py'),
                    str(target / 'examples/listing.json'),
                ]
                usable = subprocess.run(lint_command, cwd=directory, capture_output=True, text=True)
                self.assertEqual(usable.returncode, 0, usable.stderr)

                sentinel = target / 'do-not-overwrite.txt'
                sentinel.write_text('custom installation', encoding='utf-8')
                second = subprocess.run(command, capture_output=True, text=True)
                self.assertNotEqual(second.returncode, 0)
                self.assertEqual(sentinel.read_text(encoding='utf-8'), 'custom installation')

    def test_bash_installers(self):
        bash = shutil.which('bash')
        if not bash:
            self.skipTest('Bash unavailable; skipping Bash installer behavior')
        self._assert_installer_behavior('bash', bash)

    def test_powershell_installers(self):
        powershell = shutil.which('pwsh') or shutil.which('powershell')
        if not powershell:
            self.skipTest('PowerShell unavailable; skipping PowerShell installer behavior')
        self._assert_installer_behavior('powershell', powershell)


if __name__ == '__main__':
    unittest.main()
