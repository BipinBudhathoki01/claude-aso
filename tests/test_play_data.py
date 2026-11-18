import io
import json
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from play_listing_performance import markdown as performance_markdown, summarize as summarize_performance
from play_vitals import fetch_vitals


class PlayListingPerformanceTests(unittest.TestCase):
    def write_csv(self, content):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'performance.csv'
        path.write_text(content, encoding='utf-8')
        return path

    def test_legacy_export_calculates_visitor_weighted_rate(self):
        report = summarize_performance(ROOT / 'examples/play-listing-performance.csv')
        self.assertEqual(report['metric'], 'store_listing_conversion_rate')
        self.assertEqual(report['summary']['visitors'], 330)
        self.assertEqual(report['summary']['visitor_weighted_rate_percent'], 13.7576)
        self.assertEqual(report['summary']['daily_visitor_change'], 10)

    def test_parses_quoted_visitor_thousands_separator(self):
        path = self.write_csv('Date,Store listing visitors,Click-through rate\n2026-01-01,"1,200",0.1\n')
        self.assertEqual(summarize_performance(path)['summary']['visitors'], 1200)

    def test_new_ctr_export_accepts_percent_values_and_segment_rows(self):
        path = self.write_csv('Date,Store listing visitors,Click-through rate,Country\n2026-01-01,100,12.5%,US\n2026-01-01,80,0.2,GB\n')
        report = summarize_performance(path)
        self.assertEqual(report['metric'], 'click_through_rate')
        self.assertIsNone(report['summary'])
        self.assertEqual([row['rate_percent'] for row in report['rows']], [20.0, 12.5])
        self.assertIn('omitted', report['notes'][-1])

    def test_invalid_columns_rates_and_dates_have_clear_errors(self):
        for content, expected in [
            ('Date,Visitors\n2026-01-01,10\n', 'needs Date'),
            ('Date,Store listing visitors,Click-through rate\n2026-01-01,10,101\n', 'between 0 and 100'),
            ('Date,Store listing visitors,Click-through rate\n2026/01/01,10,0.2\n', 'YYYY-MM-DD'),
        ]:
            with self.subTest(expected=expected), self.assertRaisesRegex(ValueError, expected):
                summarize_performance(self.write_csv(content))

    def test_markdown_escapes_segment_text(self):
        report = summarize_performance(self.write_csv('Date,Store listing visitors,Click-through rate,Country\n2026-01-01,10,0.1,US | <test>\n'))
        output = performance_markdown(report)
        self.assertIn(r'US \| &lt;test&gt;', output)

    def test_omits_aggregate_when_dimension_changes_over_time(self):
        path = self.write_csv('Date,Store listing visitors,Click-through rate,Country\n2026-01-01,10,0.1,US\n2026-01-02,20,0.2,GB\n')
        report = summarize_performance(path)
        self.assertIsNone(report['summary'])
        self.assertIn('dimensions that vary over time', report['notes'][-1])


class PlayVitalsTests(unittest.TestCase):
    def test_queries_real_reporting_endpoints_with_oauth_header(self):
        calls = []

        def opener(request, timeout):
            self.assertIsInstance(request, Request)
            self.assertEqual(request.get_header('Authorization'), 'Bearer test-token')
            self.assertEqual(timeout, 30)
            calls.append((request.full_url, json.loads(request.data)))
            metric = 'crashRate' if 'crashRateMetricSet' in request.full_url else 'anrRate'
            return io.BytesIO(json.dumps({'rows': [{'metrics': [{'metric': metric, 'decimalValue': '0.4'}]}]}).encode())

        report = fetch_vitals('test-token', 'com.example.app', date(2026, 1, 1), date(2026, 1, 7), opener)
        self.assertEqual(len(calls), 2)
        self.assertIn('crashRateMetricSet:query', calls[0][0])
        self.assertIn('anrRateMetricSet:query', calls[1][0])
        self.assertEqual(calls[0][1]['metrics'], ['crashRate', 'distinctUsers'])
        self.assertEqual(calls[0][1]['timelineSpec']['startTime']['timeZone'], 'America/Los_Angeles')
        self.assertEqual(report['crash_rate_rows'][0]['metrics'][0]['decimalValue'], '0.4')
        self.assertIn('does not include store-listing visitors', report['scope'])

    def test_invalid_package_and_date_range_are_rejected_without_network(self):
        def no_network(*args, **kwargs):
            self.fail('invalid inputs must not make network calls')

        with self.assertRaisesRegex(ValueError, 'Package name'):
            fetch_vitals('token', 'not a package', date(2026, 1, 1), date(2026, 1, 2), no_network)
        with self.assertRaisesRegex(ValueError, 'End date'):
            fetch_vitals('token', 'com.example.app', date(2026, 1, 2), date(2026, 1, 1), no_network)


if __name__ == '__main__':
    unittest.main()
