import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_report import build_report, markdown
from listing_diff import compare
from review_summary import summarize


class WorkflowTests(unittest.TestCase):
    def test_partial_report_exposes_missing_evidence(self):
        report = build_report({'iosName': 'Timer'})
        self.assertEqual(report['status'], 'no_findings_in_supplied_fields')
        self.assertIn('iosKeywords', report['missing_fields'])
        self.assertEqual(report['budgets'][0]['remaining'], 25)

    def test_report_marks_critical_and_formats_actual_budget(self):
        report = build_report({'iosName': 'x' * 31})
        self.assertEqual(report['status'], 'critical_findings')
        self.assertIn('31 / 30', markdown(report))

    def test_report_does_not_mutate_input(self):
        listing = {'iosName': 'Timer'}
        build_report(listing)
        self.assertEqual(listing, {'iosName': 'Timer'})

    def test_comparison_identifies_budget_regression(self):
        report = compare({'iosName': 'Timer'}, {'iosName': 'x' * 31})
        self.assertEqual(report['changes'][0]['after_count'], 31)
        self.assertEqual(len(report['introduced_findings']), 1)

    def test_comparison_identifies_resolved_finding_and_removed_field(self):
        report = compare({'iosName': 'x' * 31, 'iosKeywords': 'study'}, {'iosName': 'Timer'})
        self.assertEqual(len(report['resolved_findings']), 1)
        removed = next(row for row in report['changes'] if row['field'] == 'iosKeywords')
        self.assertEqual(removed['change'], 'removed')
        self.assertIsNone(removed['after_count'])

    def test_unchanged_listing_has_no_changes(self):
        self.assertEqual(compare({'iosName': 'Timer'}, {'iosName': 'Timer'})['changes'], [])

    def test_csv_summary_aggregates_sample_without_review_text(self):
        report = summarize(ROOT / 'examples/reviews.csv')
        self.assertEqual(report['total_reviews'], 3)
        self.assertEqual(report['average_rating'], 3.667)
        self.assertEqual(report['low_rating_count'], 1)
        self.assertNotIn('screen locked', json.dumps(report))

    def test_csv_handles_bom_quotes_and_empty_export(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'reviews.csv'
            path.write_text('\ufeffrating,body\n5,"Useful, clear"\n', encoding='utf-8')
            self.assertEqual(summarize(path)['average_rating'], 5)
            path.write_text('rating,body\n', encoding='utf-8')
            self.assertIsNone(summarize(path)['average_rating'])

    def test_bad_csv_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'reviews.csv'
            for content in ['body\ntext\n', 'rating,body\n6,text\n', 'rating,body\n2.5,text\n', 'rating,body\n5\n', 'rating,body\n5,"unclosed\n']:
                path.write_text(content, encoding='utf-8')
                with self.subTest(content=content), self.assertRaises((ValueError, csv.Error)):
                    summarize(path)

    def test_command_routes_resolve_to_bundled_files(self):
        routes = json.loads((ROOT / 'data/commands.json').read_text())
        self.assertEqual(len({r['command'] for r in routes}), len(routes))
        for route in routes:
            self.assertTrue((ROOT / route['skill']).is_file())
            if route['agent']:
                self.assertTrue((ROOT / route['agent']).is_file())

    def test_report_cli_works_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/audit_report.py'), str(ROOT / 'examples/listing.json'), '--format', 'json'], cwd=directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['findings'], [])

    def test_cli_invalid_input_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('[]', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/audit_report.py'), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('JSON object', json.loads(result.stderr)['error'])


if __name__ == '__main__':
    unittest.main()
