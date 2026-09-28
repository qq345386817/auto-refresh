# Auto Refresh & Clicker Website

Static website for Auto Refresh & Clicker. The landing pages offer the Safari app for iPhone, iPad, and Mac and the Chrome extension for desktop, with localized popup previews and links to both stores.

The popup previews use the 1.9.7 extension UI. Deploy the updated landing pages with the Chrome Web Store 1.9.7 release so the website matches the version users install.

The Chrome download buttons use Google's [Chrome Web Store badge](https://developer.chrome.com/docs/webstore/branding/) from `images/chrome-web-store-badge.png`, sized to match the App Store badge. The localized `aria-label` on each link names the destination for screen readers.

## URLs

| Language | Home | Help | Support | Privacy |
| --- | --- | --- | --- | --- |
| Default | https://auto-rc.luopeike.com/ | https://auto-rc.luopeike.com/help | https://auto-rc.luopeike.com/support | https://auto-rc.luopeike.com/privacy-policy |
| English | https://auto-rc.luopeike.com/en-US/ | https://auto-rc.luopeike.com/en-US/help | https://auto-rc.luopeike.com/en-US/support | https://auto-rc.luopeike.com/en-US/privacy-policy |
| 简体中文 | https://auto-rc.luopeike.com/zh-Hans/ | https://auto-rc.luopeike.com/zh-Hans/help | https://auto-rc.luopeike.com/zh-Hans/support | https://auto-rc.luopeike.com/zh-Hans/privacy-policy |
| 繁體中文 | https://auto-rc.luopeike.com/zh-Hant/ | https://auto-rc.luopeike.com/zh-Hant/help | https://auto-rc.luopeike.com/zh-Hant/support | https://auto-rc.luopeike.com/zh-Hant/privacy-policy |
| 日本語 | https://auto-rc.luopeike.com/ja/ | https://auto-rc.luopeike.com/ja/help | https://auto-rc.luopeike.com/ja/support | https://auto-rc.luopeike.com/ja/privacy-policy |
| 한국어 | https://auto-rc.luopeike.com/ko/ | https://auto-rc.luopeike.com/ko/help | https://auto-rc.luopeike.com/ko/support | https://auto-rc.luopeike.com/ko/privacy-policy |
| Deutsch | https://auto-rc.luopeike.com/de-DE/ | https://auto-rc.luopeike.com/de-DE/help | https://auto-rc.luopeike.com/de-DE/support | https://auto-rc.luopeike.com/de-DE/privacy-policy |
| Français | https://auto-rc.luopeike.com/fr-FR/ | https://auto-rc.luopeike.com/fr-FR/help | https://auto-rc.luopeike.com/fr-FR/support | https://auto-rc.luopeike.com/fr-FR/privacy-policy |
| Español | https://auto-rc.luopeike.com/es-ES/ | https://auto-rc.luopeike.com/es-ES/help | https://auto-rc.luopeike.com/es-ES/support | https://auto-rc.luopeike.com/es-ES/privacy-policy |
| Português | https://auto-rc.luopeike.com/pt-PT/ | https://auto-rc.luopeike.com/pt-PT/help | https://auto-rc.luopeike.com/pt-PT/support | https://auto-rc.luopeike.com/pt-PT/privacy-policy |
| العربية | https://auto-rc.luopeike.com/ar-SA/ | https://auto-rc.luopeike.com/ar-SA/help | https://auto-rc.luopeike.com/ar-SA/support | https://auto-rc.luopeike.com/ar-SA/privacy-policy |

Sitemap: https://auto-rc.luopeike.com/sitemap.xml

The ten localized URL sets are the canonical search pages. The four unprefixed
English pages remain available as fallbacks and point to their `/en-US/`
counterparts as canonical URLs. The sitemap lists only the 40 localized pages;
`hreflang="x-default"` also points to the English pages. Run
`python3 scripts/check_seo.py` before deploying SEO changes.

## Search Pages

Localized landing pages are available under:

```text
/<locale>/
```

Localized help, support, and privacy pages are available under:

```text
/<locale>/help
/<locale>/support
/<locale>/privacy-policy
```

Examples:

- https://auto-rc.luopeike.com/en-US/
- https://auto-rc.luopeike.com/zh-Hans/
- https://auto-rc.luopeike.com/ja/help
- https://auto-rc.luopeike.com/de-DE/support
- https://auto-rc.luopeike.com/fr-FR/privacy-policy

Utility pages used for screenshot previews are excluded from indexing with `robots.txt` and page-level `noindex` tags.
