from project_runtime import node_executable, raw_output_dir
"""Validate simulation provenance, numeric acceptance, and offline links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,hashlib,subprocess,shutil
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'output/simulations/ch02';errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def read(n):return json.loads((OUT/n).read_text())
report=read('verification.json');check(report['status']=='passed','simulation report failed')
rows=[*read('linear_results.json'),*read('mos_results.json'),*read('pz_results.json'),*read('transient_results.json')]
check(len(rows)==47 and all(r['passed'] for r in rows),'47 numeric acceptance checks')
check(len({r['module'] for r in rows})==20,'20 representative groups')
check(all(r['all_devices_saturated'] for r in read('mos_results.json')),'MOS saturation')
for entry in report['runs']:
 deck=ROOT/entry['deck'];check(hashlib.sha256(deck.read_bytes()).hexdigest()==entry['deck_sha256'],'changed run source '+entry['name'])
 copy=OUT/'netlists'/deck.name;check(copy.read_bytes()==deck.read_bytes(),'web netlist differs from executed source '+entry['name'])
 log=(OUT/entry['spectre_log']).read_text(errors='replace');check('spectre completes with 0 errors, 0 warnings' in log,'unclean simulator log '+entry['name'])
 run=json.loads((OUT/entry['metadata']).read_text());raw=raw_output_dir((OUT/entry['metadata']).parent,run['metadata']);check(raw.is_dir() and any(raw.glob('*.*')),'missing raw PSF '+entry['name']);check(run['metadata']['returncode']==0 and run['ok'],'bad execution contract '+entry['name'])
for name,digest in report['theory_source_hashes'].items():check(hashlib.sha256((ROOT/'derivations/ch02'/name).read_bytes()).hexdigest()==digest,'changed derivation '+name)
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  self.links += [a[k] for k in ['href','src'] if k in a]
p=P();text=(OUT/'index.html').read_text();p.feed(text)
for link in p.links:
 u=urlsplit(link)
 check(not u.scheme.startswith('http'),'unexpected external web dependency '+link)
 if not u.scheme and u.path:check((OUT/unquote(u.path)).is_file(),'missing web resource '+link)
 if not u.path and u.fragment:check(u.fragment in p.ids,'missing module anchor '+link)
check('SIMMATHTOKEN' not in text and 'katex-error' not in text,'unrendered math')
for r in read('linear_results.json')+read('mos_results.json'):
 for key in ['csv','asset']:check((OUT/r[key]).is_file(),r['id']+' missing '+key)
check(not (OUT/'bridge.env').exists(),'connection config should not be in web output')
mods=read('module_summary.json');derived=json.loads((ROOT/'output/derivations/ch02/modules_data.json').read_text());catalog=json.loads((ROOT/'output/extraction/catalog.json').read_text())
for mid in mods:check('Spectre 仿真结果' in derived[mid]['html'],'missing derivation integration '+mid)
mapped=[c for c in catalog if c['chapter']==2 and c.get('simulation')]
check(len(mapped)==66,'66 technical slides linked to group representative simulations')
for c in mapped:check(c['simulation_status']=='derivation_group_representative_models_verified','overstated or missing per-slide status '+c['slide_id'])
node=node_executable()
for f in ['scripts/build_ch02_sim.mjs','scripts/build_ch02.mjs']:
 r=subprocess.run([node,'--check',str(ROOT/f)],capture_output=True,text=True);check(r.returncode==0,'JS syntax '+f+r.stderr)
result={'status':'failed' if errors else 'passed','errors':errors,'numeric_checks':47,'representative_groups':20,'technical_slides_linked_to_group_report':len(mapped),'executed_netlist_hashes_checked':True,'raw_psf_present':True,'simulator_logs_clean':True,'web_assets_and_module_anchors_checked':True,'math_rendering_checked':True,'browser_qa':False,'visual_qa':'Inspected representative AC overlays, MOS plot, gm/Id lookup, PZ map and transient figure.'}
(OUT/'artifact_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
