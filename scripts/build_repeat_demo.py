#!/usr/bin/env python3
"""Build localized, functional orders pages used by Safari preview recordings."""
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'preview_demo'
copy = json.loads((DEST / 'repeat-copy.json').read_text())
digest = hashlib.sha256((DEST / 'repeat-demo.css').read_bytes() + (DEST / 'repeat-demo.js').read_bytes()).hexdigest()[:12]
refresh = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 6v5h-5M4 18v-5h5"/><path d="M6.1 6.1A8 8 0 0 1 20 11M4 13a8 8 0 0 0 13.9 4.9"/></svg>'
search = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>'
for locale, c in copy.items():
    e = escape
    options = ''.join(f'<option value="{key}"{" selected" if key == locale else ""}>{name}</option>' for key, name in [('en-US','English'),('zh-Hans','简体中文'),('zh-Hant','繁體中文'),('ja','日本語'),('ko','한국어'),('de-DE','Deutsch'),('fr-FR','Français'),('es-ES','Español'),('pt-PT','Português'),('ar-SA','العربية')])
    data = json.dumps(c, ensure_ascii=False).replace('<', '\\u003c')
    page = f'''<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar-SA' else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{e(c['title'])} · Luma Studio</title><link rel="icon" href="../favicon/favicon.ico"><link rel="stylesheet" href="./repeat-demo.css?v={digest}"></head>
<body><header class="topbar"><a class="brand" href="./repeat-{locale.lower()}.html"><span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="m12 3 8 4.5v9L12 21l-8-4.5v-9Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9M8 5.2l8 4.6"/></svg></span>Luma Studio</a><span class="demo-note">{e(c['demo'])}</span><select id="language" aria-label="{e(c['language'])}">{options}</select></header>
<main><div class="page-heading"><div><h1>{e(c['title'])}</h1><p>{e(c['subtitle'])}</p></div></div>
<section class="metrics" aria-label="{e(c['title'])}"><div><span>{e(c['toShip'])}</span><strong id="pendingCount">—</strong><i class="metric-line amber" aria-hidden="true"></i></div><div><span>{e(c['today'])}</span><strong id="shippedCount">—</strong><i class="metric-line green" aria-hidden="true"></i></div><div><span>{e(c['inView'])}</span><strong id="matchingCount">—</strong><i class="metric-line blue" aria-hidden="true"></i></div></section>
<section id="orders" class="orders-panel" aria-label="{e(c['title'])}"><div class="panel-toolbar"><div class="filters" role="group" aria-label="{e(c['status'])}"><button type="button" data-status="all" aria-pressed="true">{e(c['all'])}</button><button type="button" data-status="pending" aria-pressed="false">{e(c['pending'])}<span id="pendingBadge" class="filter-count" aria-hidden="true"></span></button><button type="button" data-status="shipped" aria-pressed="false">{e(c['shipped'])}</button></div><div class="search-refresh"><label class="search-field">{search}<span class="sr-only">{e(c['search'])}</span><input id="orderSearch" type="search" aria-label="{e(c['search'])}" placeholder="{e(c['placeholder'])}" autocomplete="off" enterkeyhint="search"></label><button id="refreshOrders" class="refresh-button" type="button" aria-label="{e(c['refresh'])}" title="{e(c['refresh'])}">{refresh}</button></div></div>
<div class="sync-row"><p id="syncStatus" role="status" aria-live="polite">{e(c['updated'])}</p><button id="clearFilters" type="button" hidden>{e(c['reset'])}</button></div>
<div class="table-wrap"><table><thead><tr><th scope="col">{e(c['order'])}</th><th scope="col">{e(c['product'])}</th><th scope="col">{e(c['status'])}</th><th scope="col">{e(c['time'])}</th></tr></thead><tbody id="orderRows"></tbody></table></div>
<footer class="table-footer"><p id="showing" role="status" aria-live="polite"></p><div><button id="loadMore" type="button">{e(c['more'])}</button></div></footer></section></main>
<script type="application/json" id="demoCopy">{data}</script><script src="./repeat-demo.js?v={digest}" defer></script></body></html>'''
    (DEST / f'repeat-{locale.lower()}.html').write_text(page)
print('Built ten localized orders demos; existing news previews are unchanged.')
