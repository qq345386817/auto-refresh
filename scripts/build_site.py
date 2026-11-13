#!/usr/bin/env python3
"""Build plain-HTML localized pages; optionally import original Safari captures."""
import argparse
import hashlib
import json
import re
import shutil
import struct
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY = json.loads((ROOT / 'scripts/site-copy.json').read_text())
HELP = json.loads((ROOT / 'scripts/help-copy.json').read_text())
SCENES = ('02-auto-refresh', '01-refresh-click', '04-repeat-click')
GUIDE_IDS = ('auto-refresh', 'refresh-click', 'repeat-click')
APP_STORE = 'https://apps.apple.com/app/id6502815806'
CHROME_STORE = 'https://chromewebstore.google.com/detail/auto-refresh-clicker/npnkajomnfmgoakdnjcafbnmcgfkgghc'
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"></path></svg>'
LANGUAGES = (
    ('en-US', 'English'), ('zh-Hans', '简体中文'), ('zh-Hant', '繁體中文'),
    ('ja', '日本語'), ('ko', '한국어'), ('de-DE', 'Deutsch'),
    ('fr-FR', 'Français'), ('es-ES', 'Español'), ('pt-PT', 'Português'),
    ('ar-SA', 'العربية'),
)


def e(text):
    return escape(text, quote=True)


def sync_tokens(path):
    tokens = json.loads(path.read_text())
    lines = ['/* Generated from the Auto Refresh & Clicker design system. */']
    for theme in tokens['color']['themes']:
        declarations = []
        for token in tokens['color']['tokens']:
            value = token['value']
            if isinstance(value, dict):
                value = value.get(theme['id'], value.get('light'))
            declarations.append(f"  --{token['name']}: {value};")
        rule = ':root {\n' + '\n'.join(declarations) + '\n}'
        lines.append(rule if theme['id'] == 'light' else '@media (prefers-color-scheme: dark) {\n' + rule + '\n}')
    declarations = [f"  --font-sans: {tokens['type']['families']['sans']};"]
    for family in ('spacing', 'radius'):
        declarations += [f"  --{t['name']}: {t['value']};" for t in tokens[family]['tokens']]
    lines.append(':root {\n' + '\n'.join(declarations) + '\n}')
    (ROOT / 'style/foundations.css').write_text('\n'.join(lines) + '\n')


def import_captures(directory):
    directory = directory.resolve()
    destination = ROOT / 'images/safari-tasks'
    destination.mkdir(exist_ok=True)
    assets = []
    builds = set()
    for locale in COPY:
        for scene in SCENES:
            source = directory / f'{locale}-{scene}.png'
            proof = json.loads((directory / f'{locale}-{scene}.json').read_text())
            assert proof['version'] == '1.10.0' and proof['build'] == '80' and proof['family'] == 'mac', 'Final Mac release capture required'
            assert proof.get('demo_story_revision') == 'news-orders-v1', 'Use the current news and orders scenes'
            assert proof.get('visual_reviewed') and proof.get('language_reviewed'), 'Review the original capture before publishing it'
            assert proof['locale'] == locale and proof['scene'] == scene
            contents = source.read_bytes()
            assert hashlib.sha256(contents).hexdigest() == proof['sha256'], 'Capture checksum mismatch'
            builds.add(proof['build'])
            name = f'{locale}-{scene}-v{proof["version"]}-b{proof["build"]}.png'
            shutil.copyfile(source, destination / name)
            width, height = struct.unpack('>II', contents[16:24])
            assets.append({'file': 'images/safari-tasks/' + name, 'locale': locale,
                           'scene': scene, 'source': str(source.relative_to(ROOT.parent)),
                           'build': proof['build'], 'sha256': hashlib.sha256(contents).hexdigest(), 'width': width, 'height': height})
    (destination / 'provenance.json').write_text(json.dumps({
        'app_version': '1.10.0', 'builds': sorted(builds), 'surface': 'Safari on Mac',
        'example': 'Local demonstration page', 'transformation': 'None; byte-for-byte copy',
        'assets': assets}, ensure_ascii=False, indent=2) + '\n')


def stores(c):
    return f'''<div class="actions store-actions"><a class="button button-primary" href="{APP_STORE}" aria-label="{e(c['store'])}"><span>App Store</span>{ARROW}</a><a class="button button-secondary" href="{CHROME_STORE}" aria-label="{e(c['chrome'])}"><span>Chrome Web Store</span>{ARROW}</a></div>'''


def setup(c, guide=True):
    rows = ''.join(f'<li><span class="step-number" aria-hidden="true">0{i+1}</span><h3>{e(title)}</h3><p>{e(body)}</p></li>' for i, (title, body) in enumerate(c['steps']))
    link = f'<a class="text-link" href="help">{e(c["guide"])}{ARROW}</a>' if guide else ''
    return f'<section class="section setup-section" id="setup" aria-labelledby="setup-title"><div class="section-heading"><h2 id="setup-title">{e(c["setup"])}</h2><p>{e(c["setupIntro"])}</p></div><ol class="setup-grid">{rows}</ol>{link}</section>'


def tasks(c, h):
    rows = ''.join(f'<article><span class="feature-number" aria-hidden="true">0{i+1}</span><h3>{e(c["tabs"][i])}</h3><p>{e(body)}</p><a class="text-link" href="help#{GUIDE_IDS[i]}">{e(h["links"][i])}{ARROW}</a></article>' for i, body in enumerate(c['modes']))
    return f'<section class="section" id="tasks" aria-labelledby="tasks-title"><div class="section-heading"><h2 id="tasks-title">{e(c["tasks"])}</h2><p>{e(c["tasksIntro"])}</p></div><div class="feature-grid">{rows}</div></section>'


def faq(c, opened=False):
    items = ''.join(f'<details{" open" if opened else ""}><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>' for q, a in c['faq'])
    return f'<section class="section faq-section" id="faq" aria-labelledby="faq-title"><h2 id="faq-title">{e(c["faqTitle"])}</h2><div class="faq-list">{items}</div></section>'


def help_page(c, h):
    sections = [('enable', h['enable'])] + list(zip(GUIDE_IDS, c['tabs'])) + [
        ('troubleshooting', h['troubleshooting']), ('contact', h['contactTitle'])]
    contents = ''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor, label in sections)
    platforms = ''.join(f'<article><h3>{e(title)}</h3><p>{e(body)}</p></article>' for title, body in c['platforms'])
    tutorials = []
    for i, guide in enumerate(h['guides']):
        steps = ''.join(f'<li>{e(step)}</li>' for step in guide['steps'])
        tutorials.append(f'<section class="section tutorial" id="{GUIDE_IDS[i]}" aria-labelledby="{GUIDE_IDS[i]}-title"><h2 id="{GUIDE_IDS[i]}-title">{e(c["tabs"][i])}</h2><p class="tutorial-intro">{e(guide["intro"])}</p><ol class="tutorial-steps">{steps}</ol><aside class="platform-note"><p>{e(guide["note"])}</p></aside></section>')
    issues = ''.join(f'<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>' for q, a in h['issues'])
    return (f'<main id="main-content" class="content-page help-page"><p class="eyebrow">Auto Refresh &amp; Clicker</p>'
            f'<h1>{e(h["title"])}</h1><p class="lead small">{e(h["intro"])}</p><p class="release-note">{e(c["releaseStatus"])}</p>'
            f'<nav class="help-contents" aria-label="{e(h["toc"])}"><h2>{e(h["toc"])}</h2>{contents}</nav>'
            f'<section class="section" id="enable" aria-labelledby="enable-title"><h2 id="enable-title">{e(h["enable"])}</h2><div class="platform-guides">{platforms}</div></section>'
            + ''.join(tutorials)
            + f'<section class="section" id="troubleshooting" aria-labelledby="troubleshooting-title"><h2 id="troubleshooting-title">{e(h["troubleshooting"])}</h2><div class="faq-list">{issues}</div></section>'
            f'<section class="section help-contact" id="contact" aria-labelledby="contact-title"><h2 id="contact-title">{e(h["contactTitle"])}</h2><p>{e(h["contactBody"])}</p><a class="text-link" href="support">{e(h["contactLink"])}{ARROW}</a></section></main>')


def gallery(c, locale, prefix, assets):
    buttons, panels = [], []
    for index, (scene, label) in enumerate(zip(SCENES, c['tabs'])):
        active = index == 1
        buttons.append(f'<button type="button" id="task-tab-{index}" role="tab" aria-selected="{str(active).lower()}" aria-controls="task-panel-{index}" tabindex="{0 if active else -1}">{e(label)}</button>')
        asset = assets[(locale, scene)]
        file = asset['file']
        priority = ' fetchpriority="high"' if active else ''
        panels.append(f'<div id="task-panel-{index}" role="tabpanel" aria-labelledby="task-tab-{index}" tabindex="0"{"" if active else " hidden"}><figure><img src="{prefix}{file}" alt="{e(label + " — " + c["caption"])}" width="{asset["width"]}" height="{asset["height"]}" loading="{"eager" if active else "lazy"}" decoding="async"{priority}><figcaption><a href="{prefix}{file}" target="_blank" rel="noopener">{e(c["openImage"])}{ARROW}</a></figcaption></figure></div>')
    return f'<section class="viewer" aria-label="{e(c["previewLabel"])}" data-viewer><div class="viewer-toolbar"><span class="viewer-platform"><span class="live-dot" aria-hidden="true"></span>Safari <span aria-hidden="true">/</span> Mac</span><div class="task-tabs" role="tablist" aria-label="{e(c["previewLabel"])}">{"".join(buttons)}</div></div>{"".join(panels)}</section><p class="capture-caption">{e(c["caption"])}</p>'


def footer(c, links):
    return f'<footer class="site-footer"><a class="footer-brand" href="./">Auto Refresh &amp; Clicker</a><nav aria-label="{e(c["guide"])}">{links}</nav><span>Safari · Chrome</span></footer>'


def language_switch(locale, page, label):
    suffix = '/' if page == 'index' else f'/{page}'
    current = dict(LANGUAGES)[locale]
    items = []
    for code, name in LANGUAGES:
        current_attribute = ' aria-current="page"' if code == locale else ''
        items.append(f'<a href="/{code}{suffix}" hreflang="{code}" lang="{code}" dir="auto"{current_attribute}>{e(name)}</a>')
    links = ''.join(items)
    chevron = '<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>'
    return (f'<details class="language-switch"><summary aria-label="{e(label + ": " + current)}">'
            f'<span lang="{locale}" dir="auto">{e(current)}</span>{chevron}</summary>'
            f'<nav class="language-options" aria-label="{e(label)}">{links}</nav></details>')


def build_not_found():
    links = ''.join(f'<a href="/{code}/" lang="{code}" hreflang="{code}" dir="auto">{e(name)}</a>'
                    for code, name in LANGUAGES)
    styles = ''.join(
        f'<link rel="stylesheet" href="/style/{name}?v={hashlib.sha256((ROOT / "style" / name).read_bytes()).hexdigest()[:12]}">'
        for name in ('foundations.css', 'site.css')
    )
    document = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page not found — Auto Refresh &amp; Clicker</title><meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#ffffff">{styles}<link rel="icon" href="/favicon/favicon.ico"></head>
<body><div class="page"><div class="container narrow"><header class="topbar">
<a class="brand" href="/en-US/"><img src="/images/app-icon.png" alt="" width="38" height="38"><span>Auto Refresh &amp; Clicker</span></a>
</header><main class="content-page"><p class="eyebrow">404</p><h1>Page not found</h1>
<p>This link may be out of date. Choose your language to return to the homepage.</p>
<nav class="not-found-languages" aria-label="Languages">{links}</nav></main></div></div></body></html>
'''
    (ROOT / '404.html').write_text(document)


def build_page(path, locale, page, assets):
    document = path.read_text()
    c = COPY[locale]
    h = HELP[locale]
    prefix = '' if path.parent == ROOT else '../'
    header = re.search(r'<header\b[\s\S]*?</header>', document).group()
    header = re.sub(r'aria-label="Primary"', f'aria-label="{e(c["guide"])}"', header)
    switch_pattern = r'<(?:label|details)\b[^>]*class="language-switch"[^>]*>[\s\S]*?</(?:label|details)>'
    switch = re.search(switch_pattern, header)
    assert switch, f'Missing language navigation: {path}'
    label = unescape(re.search(r'<(?:select|nav)\b[^>]*aria-label="([^"]+)"', switch.group()).group(1))
    header = re.sub(switch_pattern, lambda _: language_switch(locale, page, label), header)
    if page != 'index':
        header = header.replace(f'<a href="{page}">', f'<a href="{page}" aria-current="page">')
    links = re.search(r'<nav\b[^>]*>([\s\S]*?)</nav>', header).group(1)
    privacy_label = unescape(re.search(r'href="(?:en-US/)?privacy-policy"[^>]*>(.*?)</a>', header).group(1))
    if page == 'index':
        main = f'''<main id="main-content"><section class="hero" aria-labelledby="hero-title"><div><p class="eyebrow">{e(c['ctaText'])}</p><h1 id="hero-title">{e(c['hero'][0])}<br><span>{e(c['hero'][1])}</span></h1></div><div class="hero-copy"><p class="lead">{e(c['intro'])}</p>{stores(c)}<p class="hero-note">{e(c['promise'])}</p><p class="release-note">{e(c['releaseStatus'])}</p><a class="text-link" href="#tasks">{e(c['jump'])}{ARROW}</a></div></section>
          {gallery(c, locale, prefix, assets)}{tasks(c, h)}{setup(c)}<section class="section privacy-section"><h2>{e(c['privacyTitle'])}</h2><div><p>{e(c['privacyText'])}</p><p>{e(c['mobileNote'])}</p><a class="text-link" href="privacy-policy">{e(privacy_label)}{ARROW}</a></div></section>{faq(c)}<section class="section closing"><div><h2>{e(c['cta'])}</h2><p>{e(c['ctaText'])}</p></div><div>{stores(c)}<p class="capture-caption">{e(c['priceNote'])}</p></div></section></main>'''
    elif page == 'help':
        main = help_page(c, h)
    else:
        main = re.search(r'<main\b[\s\S]*?</main>', document).group()
        if 'id="main-content"' not in main:
            main = re.sub(r'<main\b', '<main id="main-content"', main, count=1)
        if page == 'support':
            # Keep the existing contact links and purchase guidance. Replace the
            # old supplemental cards, some of which described the removed mode.
            pattern = r'<section class="section support-list">([\s\S]*?)</section>'
            section = re.search(pattern, main)
            articles = re.findall(r'<article>[\s\S]*?</article>', section[1])[:4]
            articles.append(f'<article><h2>{e(h["contactTitle"])}</h2><p>{e(h["contactBody"])}</p><a class="text-link" href="help#troubleshooting">{e(h["troubleshooting"])}{ARROW}</a></article>')
            main = re.sub(pattern, lambda _: '<section class="section support-list">' + ''.join(articles) + '</section>', main)
    body = f'<body><a class="skip-link" href="#main-content">{e(c["skip"])}</a><div class="page"><div class="container{" narrow" if page != "index" else ""}">{header}{main}{footer(c, links)}</div></div>'
    if page == 'index':
        body += f'<script src="{prefix}script/site.js" defer></script>'
    body += '</body>'
    document = re.sub(r'<body>[\s\S]*?</body>', lambda _: body, document)
    document = re.sub(r'<meta name="theme-color"[^>]*>', '<meta name="theme-color" content="#ffffff">', document)
    if 'foundations.css' not in document:
        document = document.replace(f'<link rel="stylesheet" href="{prefix}style/site.css">', f'<link rel="stylesheet" href="{prefix}style/foundations.css">\n  <link rel="stylesheet" href="{prefix}style/site.css">')
    for stylesheet in ('foundations.css', 'site.css'):
        digest = hashlib.sha256((ROOT / 'style' / stylesheet).read_bytes()).hexdigest()[:12]
        document = re.sub(r'(href="(?:\.\./)?style/' + re.escape(stylesheet) + r')(?:\?[^\"]*)?"',
                          lambda match: match[1] + '?v=' + digest + '"', document)
    descriptions = {'index': c['intro'], 'help': h['description'],
                    'support': h['supportDescription'], 'privacy-policy': h['privacyDescription']}
    for attribute in ('name="description"', 'property="og:description"'):
        document = re.sub(f'<meta {attribute} content="[^"]*">', lambda _: f'<meta {attribute} content="{e(descriptions[page])}">', document)
    if page == 'help':
        title = e(h['title'] + ' · Auto Refresh & Clicker')
        document = re.sub(r'<title>[\s\S]*?</title>', lambda _: f'<title>{title}</title>', document)
        document = re.sub(r'<meta property="og:title" content="[^"]*">', lambda _: f'<meta property="og:title" content="{title}">', document)
    path.write_text(document)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tokens', type=Path)
    parser.add_argument('--import-captures', type=Path)
    args = parser.parse_args()
    if args.tokens:
        sync_tokens(args.tokens)
    if args.import_captures:
        import_captures(args.import_captures)
    manifest = json.loads((ROOT / 'images/safari-tasks/provenance.json').read_text())
    assets = {(asset['locale'], asset['scene']): asset for asset in manifest['assets']}
    for locale in COPY:
        for page in ('index', 'help', 'support', 'privacy-policy'):
            build_page(ROOT / locale / f'{page}.html', locale, page, assets)
    for page in ('index', 'help', 'support', 'privacy-policy'):
        build_page(ROOT / f'{page}.html', 'en-US', page, assets)
    build_not_found()
    print('Built 40 localized pages, 4 English fallbacks, and a 404 page.')


if __name__ == '__main__':
    main()
