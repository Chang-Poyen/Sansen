from project_runtime import node_executable, raw_output_dir
"""Offline artifact integrity, provenance and syntax checks; no browser session."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re,subprocess,shutil,hashlib
root=Path('output/derivations/ch02'); errors=[]
def check(ok,reason):
 if not ok:errors.append(reason)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.scripts={};self.current=None;self.text=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for a in ['src','href']:
   if a in attrs:self.links.append(attrs[a])
  if tag=='script':self.current=attrs.get('id','javascript');self.scripts[self.current]=''
 def handle_endtag(self,tag):
  if tag=='script':self.current=None
 def handle_data(self,data):
  if self.current is not None:self.scripts[self.current]+=data
  else:self.text.append(data)
def verify_links(p,base):
 for url in p.links:
  u=urlsplit(url)
  if not u.scheme and u.path:check((base/unquote(u.path)).is_file(),f'missing resource: {base}: {url}')
  check(not u.scheme.startswith('http'),'unexpected remote dependency/link: '+url)
mods=json.loads((root/'modules.json').read_text());coverage=json.loads((root/'coverage.json').read_text())
check(len(coverage)==72 and len({c['slide_id'] for c in coverage})==72,'72 unique source mappings')
check(sum(c['status'].startswith('context') for c in coverage)==6,'six context slides')
check(len(mods)==21 and sum(m['sfg'] for m in mods)==3,'20 derivations, one convention module, three SFGs')
by={c['slide_id']:c for c in json.loads(Path('output/extraction/catalog.json').read_text()) if c['chapter']==2}
for c in coverage:
 check(c['slide_id'] in by,'unknown source '+c['slide_id'])
 a=by[c['slide_id']]['slide_images'][0]
 check((c['pdf_page'],c['printed_page'])==(a['pdf_page'],a['printed_page']),'source page mismatch '+c['slide_id'])
 check(by[c['slide_id']].get('derivation',{}).get('module_id')==c['module_id'],'catalog mapping '+c['slide_id'])
for f in root.glob('*.html'):
 p=Page();s=f.read_text();p.feed(s);verify_links(p,f.parent)
 check('CH02MATHTOKEN' not in s and 'katex-error' not in s,'unrendered math '+f.name)
 check('$$' not in ''.join(p.text),'raw display delimiters '+f.name)
 for mid,m in [(m['id'],m) for m in mods if f.stem==m['id']]:
  check('class="katex' in s,'missing math rendering '+mid)
  check((root/(mid+'.md')).is_file(),'missing Markdown '+mid)
for css in [root/'assets/katex/katex.min.css']:
 for url in re.findall(r'url\(([^)]+)\)',css.read_text()):
  check((css.parent/url.strip('"\'')).exists(),'missing font '+url)
p=Page();p.feed(Path('output/extraction/index.html').read_text())
embedded=json.loads(p.scripts['derivations']);raw=json.loads(p.scripts['data'])
check(len(embedded)==21 and len(raw)==1468,'embedded payload counts')
for mid,m in embedded.items():
 fragment=Page();fragment.feed(m['html']);verify_links(fragment,Path('output/extraction'))
check('derivationPanel(c)' in p.scripts['javascript'],'catalog missing derivation integration')
check('value="derivation"' in Path('output/extraction/index.html').read_text(),'catalog missing derivation filter')
js=Path('tmp/ch02/catalog-inline.js');js.write_text(p.scripts['javascript'])
node=node_executable()
r=subprocess.run([node,'--check',str(js)],capture_output=True,text=True)
check(r.returncode==0,'catalog JS syntax: '+r.stderr)
for f in Path('scripts').glob('*ch02*.mjs'):
 r=subprocess.run([node,'--check',str(f)],capture_output=True,text=True);check(r.returncode==0,'build JS syntax '+str(f)+r.stderr)
for model in json.loads(Path('derivations/ch02/physical_sfg/models.json').read_text()):
 name=model['id'];edges=sum(len(c['terms']) for c in model['constraints'])
 dot=(root/f'assets/{name}-sfg.dot').read_text();svg=(root/f'assets/{name}-sfg.svg').read_text()
 check(dot.count(' -> ')==edges and svg.count('class="edge"')==edges,'SFG edge count '+name)
check(json.loads((root/'verification.json').read_text())['status']=='passed','algebra not passed')
check(json.loads((root/'render_verification.json').read_text())['status']=='passed','TeX not passed')
report=dict(status='failed' if errors else 'passed',errors=errors,slide_mappings=72,technical_slides=66,context_slides=6,
 standalone_html_pages=len(list(root.glob('*.html'))),source_provenance_checked=True,local_resources_checked=True,
 embedded_catalog_data_checked=True,javascript_syntax_checked=True,
 image_qa='Three SFGs and three scientific plots rasterized and visually inspected.',
 browser_qa='Not performed; static files and generated figure artifacts checked only.',
 source_markdown_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('derivations/ch02').glob('*.md')})
(root/'site_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='source_markdown_sha256'},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
