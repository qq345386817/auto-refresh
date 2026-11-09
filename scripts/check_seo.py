#!/usr/bin/env python3
"""Check that the sitemap and localized canonical links agree."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://auto-rc.luopeike.com"
LOCALES = (
    "ar-SA", "de-DE", "en-US", "es-ES", "fr-FR",
    "ja", "ko", "pt-PT", "zh-Hans", "zh-Hant",
)
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


def main():
    sitemap = ElementTree.parse(ROOT / "sitemap.xml").getroot()
    urls = [node.text for node in sitemap.findall(".//{*}loc")]
    expected = {ORIGIN + f"/{locale}{page}" for locale in LOCALES for page in PAGES}
    assert len(urls) == len(expected) and set(urls) == expected, "Sitemap URLs differ from localized canonical pages"

    for page in PAGES:
        variants = {locale: ORIGIN + f"/{locale}{page}" for locale in LOCALES}
        variants["x-default"] = variants["en-US"]
        for locale in LOCALES:
            url = variants[locale]
            document = links(url)
            assert document.canonical == [url], f"Wrong canonical: {url}"
            assert document.og_urls == [url], f"Wrong og:url: {url}"
            assert document.alternates == variants, f"Wrong hreflang group: {url}"
            check_language_links(document, url, variants, locale)

        fallback = ORIGIN + page
        document = links(fallback)
        assert document.canonical == [variants["en-US"]], f"Wrong fallback canonical: {fallback}"
        assert document.og_urls == [variants["en-US"]], f"Wrong fallback og:url: {fallback}"
        assert document.alternates == variants, f"Wrong fallback hreflang group: {fallback}"
        check_language_links(document, fallback, variants, 'en-US')

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
