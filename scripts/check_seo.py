#!/usr/bin/env python3
"""Check that the sitemap and localized canonical links agree."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "meta" and attrs.get("property") == "og:url":
            self.og_urls.append(attrs.get("content"))


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

        fallback = ORIGIN + page
        document = links(fallback)
        assert document.canonical == [variants["en-US"]], f"Wrong fallback canonical: {fallback}"
        assert document.og_urls == [variants["en-US"]], f"Wrong fallback og:url: {fallback}"
        assert document.alternates == variants, f"Wrong fallback hreflang group: {fallback}"

    print(f"Checked {len(urls)} sitemap URLs and {len(PAGES)} English fallback pages")


if __name__ == "__main__":
    main()
