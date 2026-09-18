"""Package existing web artifacts for Cloudflare Pages, using only static hosting."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'dist/pages'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(v for k, v in attrs if k in ('href', 'src') and v)


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for section in ('extraction', 'derivations', 'simulations'):
        shutil.copytree(ROOT / 'output' / section, DEST / section,
                        ignore=shutil.ignore_patterns('.DS_Store', '__pycache__'))

    # The original 49 MiB PDF remains local; slide images are available online.
    catalog = DEST / 'extraction/index.html'
    html = catalog.read_text()
    old = '<a href="${pdf}" target="_blank">原 PDF 页面</a>'
    if html.count(old) != 1:
        raise ValueError('Catalog PDF link changed; update the deployment adapter.')
    html = html.replace(old, '<span class="caption">原 PDF 保留于本地；来源页码见上方</span>')
    html = html.replace('本地离线数据；无外部字体、服务或上传。',
                        'Sansen 在线数据库 · 图片与字体随网站提供。')
    catalog.write_text(html)
    (DEST / '_redirects').write_text('/ /extraction/ 302\n')
    (DEST / '404.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>找不到页面 · Sansen</title>
<body style="font:18px system-ui;max-width:700px;margin:15vh auto;padding:24px;color:#173f42">
<h1>找不到这个页面</h1><p>请回到数据库搜索幻灯片，或打开第二章的推导与仿真。</p>
<p><a href="/extraction/">教材数据库</a> · <a href="/derivations/ch02/">公式推导</a> ·
<a href="/simulations/ch02/">Spectre 仿真</a></p></body></html>''')
    (DEST / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n')

    errors = []
    references = 0

    def check_link(base, url):
        nonlocal references
        u = urlsplit(url)
        if u.scheme or u.netloc or not u.path:
            return
        references += 1
        target = (DEST / unquote(u.path).lstrip('/') if u.path.startswith('/')
                  else base / unquote(u.path)).resolve()
        if not target.is_relative_to(DEST) or not (target.is_file() or (target / 'index.html').is_file()):
            errors.append(f'{base.relative_to(DEST)}: {url}')

    for page in DEST.rglob('*.html'):
        parsed = Links()
        parsed.feed(page.read_text())
        for url in parsed.links:
            check_link(page.parent, url)
    for css in DEST.rglob('*.css'):
        for url in re.findall(r'url\(([^)]+)\)', css.read_text()):
            check_link(css.parent, url.strip('\"\''))
    cases = json.loads((DEST / 'extraction/catalog.json').read_text())
    for case in cases:
        for slide in case['slide_images']:
            check_link(DEST / 'extraction', slide['path'])
        for formula in case['formula_candidates']:
            check_link(DEST / 'extraction', formula['context_crop'])
        for ext in ('json', 'md'):
            check_link(DEST / 'extraction', f"cases/{case['case_id']}.{ext}")
        for key in ('html', 'markdown'):
            if case.get('derivation', {}).get(key):
                check_link(DEST / 'extraction', case['derivation'][key])

    files = [p for p in DEST.rglob('*') if p.is_file()]
    errors.extend(str(p.relative_to(DEST)) for p in files if p.stat().st_size > 25 * 1024**2)
    if len(files) > 20000:
        errors.append('Exceeded Pages Free file count')
    if any(p.name in ('_worker.js', '_routes.json') or 'functions' in p.relative_to(DEST).parts for p in files):
        errors.append('Server-side code is forbidden in this static deployment')
    report = dict(status='failed' if errors else 'passed', files=len(files),
                  total_bytes=sum(p.stat().st_size for p in files),
                  max_file_bytes=max(p.stat().st_size for p in files),
                  local_references_checked=references, slides=len(cases),
                  static_only=True, original_pdf_included=False, errors=errors)
    (ROOT / 'dist/pages-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
