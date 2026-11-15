from pathlib import Path
import sys
import unittest
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from competitor_lookup import research


class CompetitorLookupTests(unittest.TestCase):
    def fixture(self, url):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        if '/lookup?' in url:
            return {'results': [{'trackId': 1, 'trackName': 'Study Timer', 'artistName': 'Our Studio'}]}
        return {'results': [
            {'trackId': 2, 'trackName': 'Study Mock Test', 'artistName': 'Rival'},
            {'trackId': 1, 'trackName': 'Study Timer', 'artistName': 'Our Studio'},
            {'trackId': 3, 'trackName': 'Other Study App', 'artistName': 'Our Studio'},
        ]}

    def test_target_excluded_and_api_order_not_called_rank(self):
        report = research(['study'], target_id='1', fetcher=self.fixture)
        self.assertEqual(report['ranking_status'], 'not_measured')
        query = report['queries'][0]
        self.assertEqual(query['target_api_result_order'], 2)
        self.assertEqual([c['app_id'] for c in query['candidates']], ['2', '3'])
        self.assertEqual(query['candidates'][1]['api_result_order'], 3)
        self.assertNotIn('rank', query['candidates'][0])

    def test_missing_metrics_remain_unknown_and_siblings_flagged(self):
        candidates = research(['study'], target_id='1', fetcher=self.fixture)['queries'][0]['candidates']
        self.assertIsNone(candidates[0]['rating_count'])
        self.assertIsNone(candidates[0]['price_label'])
        self.assertFalse(candidates[0]['same_developer_as_target'])
        self.assertTrue(candidates[1]['same_developer_as_target'])

    def test_query_encoding_country_and_deduplication(self):
        urls = []
        def fetch(url):
            urls.append(url)
            return {'results': []}
        report = research(['study & timer', 'study & timer'], country='NP', fetcher=fetch)
        self.assertEqual(len(urls), 1)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(urls[0]).query)
        self.assertEqual(query['country'], ['np'])
        self.assertEqual(query['term'], ['study & timer'])
        self.assertIsNone(report['queries'][0]['target_api_result_order'])

    def test_invalid_inputs_do_not_make_network_calls(self):
        for kwargs in [{'terms': []}, {'terms': [' ']}, {'terms': ['x'] * 6}, {'terms': ['x'], 'country': 'nepal'}, {'terms': ['x'], 'limit': 0}, {'terms': ['x'], 'limit': True}, {'terms': ['x'], 'target_id': 'com.example'}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                research(**kwargs, fetcher=lambda url: self.fail('Unexpected network call'))

    def test_lookup_absence_is_explicit_without_losing_candidates(self):
        def fetch(url):
            return {'results': []} if '/lookup?' in url else self.fixture(url)
        report = research(['study'], target_id='1', fetcher=fetch)
        self.assertIsNone(report['target'])
        self.assertEqual(report['errors'][0]['stage'], 'target_lookup')
        self.assertEqual(len(report['queries'][0]['candidates']), 2)

    def test_network_failure_is_not_an_empty_success(self):
        def fetch(url):
            raise OSError('Simulated network failure')
        report = research(['study'], fetcher=fetch)
        self.assertEqual(report['errors'][0]['stage'], 'search')

    def test_title_overlap_is_observable_not_keyword_volume(self):
        candidate = research(['study mock'], fetcher=self.fixture)['queries'][0]['candidates'][0]
        self.assertEqual(candidate['query_words_in_title'], ['mock', 'study'])
        self.assertNotIn('search_volume', candidate)

    def test_invalid_response_is_recorded(self):
        report = research(['study'], fetcher=lambda url: {'results': None})
        self.assertTrue(report['errors'])


if __name__ == '__main__':
    unittest.main()
