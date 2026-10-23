# Auto Refresh & Clicker Website

Static website for Auto Refresh & Clicker. The landing pages offer the Safari app for iPhone, iPad, and Mac and the Chrome extension for desktop, with localized popup previews and links to both stores.

The landing pages show original Safari for Mac 1.9.9 (78) captures, with three selectable tasks in each language. The captions identify the Safari platform and local demonstration page; they do not imply that the Chrome store has the same version. Source paths, dimensions, and SHA-256 values are in `images/safari-tasks/provenance.json`. The image viewer preserves the complete browser capture and offers a full-size image link on small screens.

Download links have localized accessible names and explicit App Store / Chrome Web Store destinations. Prices are left to the stores.

## Design and content

The shared design system is in `../website-design-system/` and the editable design draft is in `../website-design/`. The system preserves the product blue, system typography, and original icon, and adds website semantic colors and layout rules. `style/foundations.css` is generated from that system; `style/site.css` owns responsive layout. No frontend framework or build dependencies are needed.

Localized copy lives in `scripts/site-copy.json`. To regenerate the 40 localized pages and four default pages:

```sh
python3 scripts/build_site.py
python3 scripts/check_seo.py
```

From the parent app project, sync the design-system values and import original release captures when required:

```sh
python3 auto-refresh/scripts/build_site.py --tokens website-design-system/tokens.json --import-captures release/1.9.9/captures78/mac
```

Ordinary builds reuse the selected images already present in the website. Old `images/popup-previews/` files remain for compatibility but are no longer used by the landing pages. The generator preserves canonical links, hreflang groups, original privacy-policy content, and support contact information. The localized help pages describe the current Safari workflow and provide separate setup directions for iPhone/iPad, Mac, and desktop Chrome.

Tabs support click, arrow keys (including RTL), Home and End. Without JavaScript, the default product image remains visible. Pages respect system appearance and reduced motion, and include a keyboard skip link. Keep temporary screenshots, logs, and QA scripts outside this repository. Publishing is a separate step; generating these files does not deploy the site.

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
