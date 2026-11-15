#!/usr/bin/env python3
"""Discover Apple competitors with source metadata; API order is not store rank."""
import argparse
from datetime import datetime, timezone
import json
import re
import sys
import urllib.parse
import urllib.request


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def normalize(item):
    return {
        'app_id': str(item['trackId']), 'name': item.get('trackName'),
        'developer': item.get('artistName'), 'store_url': item.get('trackViewUrl'),
        'category': item.get('primaryGenreName'), 'rating': item.get('averageUserRating'),
        'rating_count': item.get('userRatingCount'), 'price_label': item.get('formattedPrice'),
        'version': item.get('version'), 'updated_at': item.get('currentVersionReleaseDate'),
        'languages': item.get('languageCodesISO2A'), 'description': item.get('description'),
        'screenshot_urls': item.get('screenshotUrls', []),
    }


def research(terms, country='us', limit=6, target_id=None, fetcher=None):
    if not re.fullmatch(r'[a-zA-Z]{2}', country):
        raise ValueError('Country must be a two-letter storefront code')
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 20:
        raise ValueError('Limit must be between 1 and 20')
    if not isinstance(terms, list) or not terms or len(terms) > 5 or any(not isinstance(t, str) or not t.strip() for t in terms):
        raise ValueError('Supply one to five non-empty queries')
    if target_id is not None and not re.fullmatch(r'\d+', str(target_id)):
        raise ValueError('Target ID must be a numeric Apple app ID')
    fetcher = fetcher or fetch_json
    country = country.lower()
    target = None
    errors = []
    if target_id is not None:
        url = 'https://itunes.apple.com/lookup?' + urllib.parse.urlencode({'id': str(target_id), 'country': country})
        try:
            items = fetcher(url).get('results', [])
            item = next((i for i in items if str(i.get('trackId')) == str(target_id)), None)
            if item is None:
                errors.append({'stage': 'target_lookup', 'source_url': url, 'error': 'Target not found in this storefront'})
            else:
                target = normalize(item)
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            errors.append({'stage': 'target_lookup', 'source_url': url, 'error': str(exc)})
    queries = []
    for term in dict.fromkeys(t.strip() for t in terms):
        url = 'https://itunes.apple.com/search?' + urllib.parse.urlencode({'term': term, 'entity': 'software', 'country': country, 'limit': limit})
        query = {'query': term, 'source_url': url, 'target_api_result_order': None, 'candidates': []}
        try:
            items = fetcher(url).get('results', [])
            if not isinstance(items, list):
                raise ValueError('Search results must be an array')
            for order, item in enumerate(items, 1):
                if not isinstance(item, dict) or not item.get('trackId'):
                    continue
                if target_id is not None and str(item['trackId']) == str(target_id):
                    query['target_api_result_order'] = order
                    continue
                candidate = normalize(item)
                candidate['api_result_order'] = order
                candidate['same_developer_as_target'] = bool(target and target['developer'] and candidate['developer'] == target['developer'])
                words = set(re.findall(r'[^\W_]+', (candidate['name'] or '').casefold()))
                candidate['query_words_in_title'] = sorted(set(re.findall(r'[^\W_]+', term.casefold())) & words)
                query['candidates'].append(candidate)
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            errors.append({'stage': 'search', 'query': term, 'source_url': url, 'error': str(exc)})
        queries.append(query)
    return {
        'store': 'appstore', 'country': country,
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'ranking_status': 'not_measured',
        'limitations': [
            'API result order is discovery evidence, not verified App Store organic search rank.',
            'Missing from this sample does not mean an app is unranked.',
            'Ratings, descriptions and price labels do not establish ranking causality; review relevance manually.',
            'Private keywords, downloads, conversion and search volume are not supplied by this helper.',
        ],
        'target': target, 'queries': queries, 'errors': errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--term', action='append', required=True)
    parser.add_argument('--country', default='us')
    parser.add_argument('--limit', type=int, default=6)
    parser.add_argument('--target-id')
    args = parser.parse_args()
    try:
        report = research(args.term, args.country, args.limit, args.target_id)
    except (ValueError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report['errors'] else 0


if __name__ == '__main__':
    sys.exit(main())
