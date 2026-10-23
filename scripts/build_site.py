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
SCENES = ('02-auto-refresh', '01-refresh-click', '04-find-stopped')
APP_STORE = 'https://apps.apple.com/app/id6502815806'
CHROME_STORE = 'https://chromewebstore.google.com/detail/auto-refresh-clicker/npnkajomnfmgoakdnjcafbnmcgfkgghc'
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"></path></svg>'


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
    destination = ROOT / 'images/safari-tasks'
    destination.mkdir(exist_ok=True)
    assets = []
    for locale in COPY:
        for scene in SCENES:
            source = directory / f'{locale}-{scene}-raw.png'
            name = f'{locale}-{scene}.png'
            shutil.copyfile(source, destination / name)
            contents = source.read_bytes()
            width, height = struct.unpack('>II', contents[16:24])
            assets.append({'file': 'images/safari-tasks/' + name, 'locale': locale,
                           'scene': scene, 'source': 'release/1.9.9/captures78/mac/' + source.name,
                           'sha256': hashlib.sha256(contents).hexdigest(), 'width': width, 'height': height})
    (destination / 'provenance.json').write_text(json.dumps({
        'app_version': '1.9.9', 'build': '78', 'surface': 'Safari on macOS',
        'example': 'Local demonstration page', 'transformation': 'None; byte-for-byte copy',
        'assets': assets}, ensure_ascii=False, indent=2) + '\n')


def stores(c):
    return f'''<div class="actions store-actions"><a class="button button-primary" href="{APP_STORE}" aria-label="{e(c['store'])}"><span>App Store</span>{ARROW}</a><a class="button button-secondary" href="{CHROME_STORE}" aria-label="{e(c['chrome'])}"><span>Chrome Web Store</span>{ARROW}</a></div>'''


def setup(c, guide=True):
    rows = ''.join(f'<li><span class="step-number" aria-hidden="true">0{i+1}</span><h3>{e(title)}</h3><p>{e(body)}</p></li>' for i, (title, body) in enumerate(c['steps']))
    link = f'<a class="text-link" href="help">{e(c["guide"])}{ARROW}</a>' if guide else ''
    return f'<section class="section setup-section" id="setup" aria-labelledby="setup-title"><div class="section-heading"><h2 id="setup-title">{e(c["setup"])}</h2><p>{e(c["setupIntro"])}</p></div><ol class="setup-grid">{rows}</ol>{link}</section>'


def tasks(c):
    rows = ''.join(f'<article><span class="feature-number" aria-hidden="true">0{i+1}</span><h3>{e(c["tabs"][i])}</h3><p>{e(body)}</p></article>' for i, body in enumerate(c['modes']))
    return f'<section class="section" id="tasks" aria-labelledby="tasks-title"><div class="section-heading"><h2 id="tasks-title">{e(c["tasks"])}</h2><p>{e(c["tasksIntro"])}</p></div><div class="feature-grid">{rows}</div></section>'


def faq(c, opened=False):
    items = ''.join(f'<details{" open" if opened else ""}><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>' for q, a in c['faq'])
    return f'<section class="section faq-section" id="faq" aria-labelledby="faq-title"><h2 id="faq-title">{e(c["faqTitle"])}</h2><div class="faq-list">{items}</div></section>'


def gallery(c, locale, prefix, assets):
    buttons, panels = [], []
    for index, (scene, label) in enumerate(zip(SCENES, c['tabs'])):
        active = index == 1
        buttons.append(f'<button type="button" id="task-tab-{index}" role="tab" aria-selected="{str(active).lower()}" aria-controls="task-panel-{index}" tabindex="{0 if active else -1}">{e(label)}</button>')
        file = f'images/safari-tasks/{locale}-{scene}.png'
        asset = assets[file]
        priority = ' fetchpriority="high"' if active else ''
        panels.append(f'<div id="task-panel-{index}" role="tabpanel" aria-labelledby="task-tab-{index}" tabindex="0"{"" if active else " hidden"}><figure><img src="{prefix}{file}" alt="{e(label + " — " + c["caption"])}" width="{asset["width"]}" height="{asset["height"]}" loading="{"eager" if active else "lazy"}" decoding="async"{priority}><figcaption><a href="{prefix}{file}" target="_blank" rel="noopener">{e(c["openImage"])}{ARROW}</a></figcaption></figure></div>')
    return f'<section class="viewer" aria-label="{e(c["previewLabel"])}" data-viewer><div class="viewer-toolbar"><span class="viewer-platform"><span class="live-dot" aria-hidden="true"></span>Safari <span aria-hidden="true">/</span> macOS</span><div class="task-tabs" role="tablist" aria-label="{e(c["previewLabel"])}">{"".join(buttons)}</div></div>{"".join(panels)}</section><p class="capture-caption">{e(c["caption"])}</p>'


def footer(c, links):
    return f'<footer class="site-footer"><a class="footer-brand" href="./">Auto Refresh &amp; Clicker</a><nav aria-label="{e(c["guide"])}">{links}</nav><span>Safari · Chrome</span></footer>'


def build_page(path, locale, page, assets):
    document = path.read_text()
    c = COPY[locale]
    prefix = '' if path.parent == ROOT else '../'
    header = re.search(r'<header\b[\s\S]*?</header>', document).group()
    header = re.sub(r'aria-label="Primary"', f'aria-label="{e(c["guide"])}"', header)
    if page != 'index':
        header = header.replace(f'<a href="{page}">', f'<a href="{page}" aria-current="page">')
    links = re.search(r'<nav\b[^>]*>([\s\S]*?)</nav>', header).group(1)
    privacy_label = unescape(re.search(r'href="(?:en-US/)?privacy-policy"[^>]*>(.*?)</a>', header).group(1))
    help_label = unescape(re.search(r'href="(?:en-US/)?help"[^>]*>(.*?)</a>', header).group(1))
    if page == 'index':
        main = f'''<main id="main-content"><section class="hero" aria-labelledby="hero-title"><div><p class="eyebrow">{e(c['ctaText'])}</p><h1 id="hero-title">{e(c['hero'][0])}<br><span>{e(c['hero'][1])}</span></h1></div><div class="hero-copy"><p class="lead">{e(c['intro'])}</p>{stores(c)}<p class="hero-note">{e(c['promise'])}</p><a class="text-link" href="#tasks">{e(c['jump'])}{ARROW}</a></div></section>
          {gallery(c, locale, prefix, assets)}{tasks(c)}{setup(c)}<section class="section privacy-section"><h2>{e(c['privacyTitle'])}</h2><div><p>{e(c['privacyText'])}</p><p>{e(c['mobileNote'])}</p><a class="text-link" href="privacy-policy">{e(privacy_label)}{ARROW}</a></div></section>{faq(c)}<section class="section closing"><div><h2>{e(c['cta'])}</h2><p>{e(c['ctaText'])}</p></div><div>{stores(c)}<p class="capture-caption">{e(c['priceNote'])}</p></div></section></main>'''
    elif page == 'help':
        platforms = ''.join(f'<article><h3>{e(title)}</h3><p>{e(body)}</p></article>' for title, body in c['platforms'])
        main = f'<main id="main-content" class="content-page"><p class="eyebrow">Auto Refresh &amp; Clicker</p><h1>{e(help_label)}</h1><p class="lead small">{e(c["intro"])}</p>{setup(c, False)}<section class="section platform-guides" aria-label="{e(c["guide"])}">{platforms}</section>{tasks(c)}<aside class="platform-note"><p>{e(c["mobileNote"])}</p></aside>{faq(c, True)}<div class="section">{stores(c)}<p class="capture-caption">{e(c["priceNote"])}</p></div></main>'
    else:
        main = re.search(r'<main\b[\s\S]*?</main>', document).group()
        if 'id="main-content"' not in main:
            main = re.sub(r'<main\b', '<main id="main-content"', main, count=1)
    body = f'<body><a class="skip-link" href="#main-content">{e(c["skip"])}</a><div class="page"><div class="container{" narrow" if page != "index" else ""}">{header}{main}{footer(c, links)}</div></div>'
    if page == 'index':
        body += f'<script src="{prefix}script/site.js" defer></script>'
    body += '</body>'
    document = re.sub(r'<body>[\s\S]*?</body>', lambda _: body, document)
    document = re.sub(r'<meta name="theme-color"[^>]*>', '<meta name="theme-color" content="#ffffff">', document)
    if 'foundations.css' not in document:
        document = document.replace(f'<link rel="stylesheet" href="{prefix}style/site.css">', f'<link rel="stylesheet" href="{prefix}style/foundations.css">\n  <link rel="stylesheet" href="{prefix}style/site.css">')
    if page == 'index':
        for attribute in ('name="description"', 'property="og:description"'):
            document = re.sub(f'<meta {attribute} content="[^"]*">', f'<meta {attribute} content="{e(c["intro"])}">', document)
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
    assets = {asset['file']: asset for asset in manifest['assets']}
    for locale in COPY:
        for page in ('index', 'help', 'support', 'privacy-policy'):
            build_page(ROOT / locale / f'{page}.html', locale, page, assets)
    for page in ('index', 'help', 'support', 'privacy-policy'):
        build_page(ROOT / f'{page}.html', 'en-US', page, assets)
    print('Built 40 localized pages and 4 English fallbacks.')


if __name__ == '__main__':
    main()
