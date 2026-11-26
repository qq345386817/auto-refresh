#!/usr/bin/env python3
"""Check that the sitemap and localized canonical links agree."""

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree
from build_site import LANGUAGES


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://auto-rc.luopeike.com"
LOCALES = tuple(code for code, _ in LANGUAGES)
PAGES = ("/", "/help", "/support", "/privacy-policy")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.alternates = {}
        self.og_urls = []
        self.anchor_hrefs = []
        self.language_links = []
        self.in_language_switch = False
        self.robots = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "meta" and attrs.get("property") == "og:url":
            self.og_urls.append(attrs.get("content"))
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots = attrs.get("content", "")
        if tag == "details" and attrs.get("class") == "language-switch":
            self.in_language_switch = True
        if tag == "a" and attrs.get("href"):
            self.anchor_hrefs.append(attrs["href"])
            if self.in_language_switch:
                self.language_links.append(attrs)

    def handle_endtag(self, tag):
        if tag == "details":
            self.in_language_switch = False


def page_file(url):
    parsed = urlparse(url)
    assert parsed.scheme == "https" and parsed.netloc == urlparse(ORIGIN).netloc
    path = parsed.path.lstrip("/")
    if parsed.path.endswith("/"):
        return ROOT / path / "index.html"
    return ROOT / f"{path}.html"


def links(url):
    parser = Links()
    parser.feed(page_file(url).read_text(encoding="utf-8"))
    return parser


def check_language_links(document, url, variants, locale):
    expected = {code: target for code, target in variants.items() if code != 'x-default'}
    actual = {link.get('hreflang'): urljoin(url, link['href']) for link in document.language_links}
    assert len(document.language_links) == len(expected) and actual == expected, f'Noncrawlable language menu: {url}'
    selected = [link for link in document.language_links if link.get('aria-current') == 'page']
    assert len(selected) == 1 and selected[0]['hreflang'] == locale, f'Wrong current language: {url}'


def check_internal_page_links(document, url, expected, fallbacks):
    for href in document.anchor_hrefs:
        if href.startswith(("mailto:", "#")):
            continue
        target = urljoin(url, href).split("#")[0]
        if urlparse(target).netloc != urlparse(ORIGIN).netloc:
            continue
        assert not target.endswith(".html"), f"Non-clean .html internal link on {url}: {href}"
        assert target not in fallbacks, f"Non-canonical fallback link on {url}: {href} -> {target}"
        if "/images/" not in urlparse(target).path:
            assert target in expected, f"Unexpected internal page link on {url}: {href} -> {target}"


def main():
    sitemap = ElementTree.parse(ROOT / "sitemap.xml").getroot()
    url_nodes = sitemap.findall(".//{*}url")
    urls = [node.findtext("{*}loc") for node in url_nodes]
    lastmods = [node.findtext("{*}lastmod") for node in url_nodes]
    expected = {ORIGIN + f"/{locale}{page}" for locale in LOCALES for page in PAGES}
    fallbacks = {ORIGIN + page for page in PAGES}
    assert len(urls) == len(expected) and set(urls) == expected, "Sitemap URLs differ from localized canonical pages"
    assert all(m is None or re.fullmatch(r"\d{4}-\d{2}-\d{2}", m) for m in lastmods), "Invalid sitemap lastmod format"

    for page in PAGES:
        variants = {locale: ORIGIN + f"/{locale}{page}" for locale in LOCALES}
        variants["x-default"] = variants["en-US"]
        for locale in LOCALES:
            url = variants[locale]
            document = links(url)
            assert 'noindex' not in document.robots.lower(), f'Canonical page blocks indexing: {url}'
            assert document.canonical == [url], f"Wrong canonical: {url}"
            assert document.og_urls == [url], f"Wrong og:url: {url}"
            assert document.alternates == variants, f"Wrong hreflang group: {url}"
            check_language_links(document, url, variants, locale)
            check_internal_page_links(document, url, expected, fallbacks)

        fallback = ORIGIN + page
        document = links(fallback)
        assert document.canonical == [variants["en-US"]], f"Wrong fallback canonical: {fallback}"
        assert document.og_urls == [variants["en-US"]], f"Wrong fallback og:url: {fallback}"
        assert document.alternates == variants, f"Wrong fallback hreflang group: {fallback}"
        check_language_links(document, fallback, variants, 'en-US')
        check_internal_page_links(document, fallback, expected, fallbacks)

    for legacy in ("help_win.html", "how_to_use.html"):
        assert not (ROOT / legacy).exists(), f"Legacy file {legacy} shadows _redirects on Cloudflare Pages"
    redirects_text = (ROOT / "_redirects").read_text(encoding="utf-8")
    for line in redirects_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        source, target, status = line.split()
        assert not target.endswith(".html"), f"Redirect target must not end with .html: {line}"
    for legacy_path in ("/help_win", "/help_win.html", "/how_to_use", "/how_to_use.html"):
        assert f"{legacy_path} /en-US/help 301" in redirects_text, f"Missing 301 redirect for {legacy_path}"

    reachable = {ORIGIN + '/en-US/'}
    pending = list(reachable)
    while pending:
        url = pending.pop()
        for href in links(url).anchor_hrefs:
            target = urljoin(url, href).split('#')[0]
            if target in expected and target not in reachable:
                reachable.add(target)
                pending.append(target)
    assert reachable == expected, 'Canonical pages are disconnected from HTML navigation'

    not_found = Links()
    not_found.feed((ROOT / '404.html').read_text(encoding='utf-8'))
    assert 'noindex' in not_found.robots and not not_found.canonical, '404 must not advertise a canonical content page'
    assert {ORIGIN + f'/{locale}/' for locale in LOCALES} <= {
        urljoin(ORIGIN, href) for href in not_found.anchor_hrefs
    }, '404 must offer working language homepage links'

    print(f"Checked {len(urls)} sitemap URLs, {len(PAGES)} English fallbacks, crawlable language navigation and 404 page")


if __name__ == "__main__":
    main()
