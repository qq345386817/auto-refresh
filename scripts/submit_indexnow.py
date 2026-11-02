#!/usr/bin/env python3
"""Notify IndexNow about explicitly selected, deployed canonical URLs.

Defaults to a local preview. --submit verifies the hosted ownership file first.
No Bing account credential is required; the ownership file is intentionally public.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def prepare(urls):
    config = json.loads((ROOT / 'indexnow.json').read_text())
    host = config['host']
    if host != 'auto-rc.luopeike.com' or config['endpoint'] != 'https://api.indexnow.org/indexnow':
        raise ValueError('Unexpected host or IndexNow endpoint.')
    name = config['keyFile']
    if not re.fullmatch(r'[A-Za-z0-9-]{8,128}\.txt', name):
        raise ValueError('Invalid ownership filename.')
    key = (ROOT / name).read_text(encoding='utf-8').strip()
    if key != name[:-4] or not re.fullmatch(r'[A-Za-z0-9-]{8,128}', key):
        raise ValueError('Ownership filename and contents must match.')
    canonical = {node.text for node in ElementTree.parse(ROOT / 'sitemap.xml').getroot().findall('.//{*}loc')}
    selected = list(dict.fromkeys(urls))
    if not 1 <= len(selected) <= 10000:
        raise ValueError('Supply between 1 and 10,000 changed URLs.')
    for url in selected:
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.netloc != host or parsed.fragment or url not in canonical:
            raise ValueError('Submit only this site\'s canonical sitemap URLs: ' + url)
    return config['endpoint'], {
        'host': host, 'key': key, 'keyLocation': 'https://' + host + '/' + name,
        'urlList': selected,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', action='append', required=True, help='Changed canonical URL; repeat as needed.')
    parser.add_argument('--submit', action='store_true', help='Verify the live key and send the notification.')
    args = parser.parse_args()
    try:
        endpoint, payload = prepare(args.url)
        summary = {'endpoint': endpoint, 'keyLocation': payload['keyLocation'], 'urlCount': len(payload['urlList']), 'urls': payload['urlList']}
        if not args.submit:
            print(json.dumps(dict(summary, status='preview; no network request sent'), ensure_ascii=False, indent=2))
            return 0
        common = ['curl', '--silent', '--show-error', '--connect-timeout', '10', '--max-time', '45']
        hosted = subprocess.run(common + ['--fail', payload['keyLocation']], check=True, capture_output=True)
        if hosted.stdout.decode('utf-8').strip() != payload['key']:
            raise ValueError('Live ownership file does not match; deploy it before submitting.')
        response = subprocess.run(common + ['--output', '/dev/null', '--write-out', '%{http_code}',
                                           '--header', 'Content-Type: application/json; charset=utf-8',
                                           '--data-binary', '@-', endpoint],
                                  input=json.dumps(payload).encode('utf-8'), check=True, capture_output=True)
        code = int(response.stdout)
        states = {200: 'received by IndexNow; crawling and indexing are not guaranteed',
                  202: 'received; ownership key validation is pending'}
        if code not in states:
            raise ValueError('IndexNow returned HTTP ' + str(code) + '; notification not confirmed.')
        print(json.dumps(dict(summary, httpStatus=code, status=states[code]), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
