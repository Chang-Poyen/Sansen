"""Run saved decks via the installed bridge; preserve raw PSF and run metadata."""
from pathlib import Path
import os,json,argparse,hashlib,time
ROOT=Path(__file__).resolve().parent.parent
os.environ['LC_ALL']='C'
if os.environ.get('SANSEN_BRIDGE_BIN'):
 os.environ['PATH']=os.environ['SANSEN_BRIDGE_BIN']+os.pathsep+os.environ['PATH']
from virtuoso_bridge.env import set_runtime_env_file
from virtuoso_bridge.spectre.runner import SpectreSimulator
ap=argparse.ArgumentParser();ap.add_argument('--env-file',type=Path,default=ROOT/'simulations/ch02/bridge.env');ap.add_argument('decks',nargs='+');args=ap.parse_args()
set_runtime_env_file(args.env_file)
for name in args.decks:
 deck=ROOT/'simulations/ch02/netlists'/f'{name}.scs'
 out=ROOT/'output/simulations/ch02/runs'/name
 out.mkdir(parents=True,exist_ok=True)
 sim=SpectreSimulator.from_env(work_dir=out,timeout=180,keep_remote_files=True,spectre_args=['+lqtimeout','30'])
 started=time.time();r=sim.run_simulation(deck,{})
 report={'deck':str(deck.relative_to(ROOT)),'sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'ok':r.ok,'errors':r.errors,'metadata':r.metadata,'wall_s':time.time()-started}
 (out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str))
 print(json.dumps({'deck':name,'ok':r.ok,'errors':r.errors,'keys':list(r.data)[:30],'metadata':r.metadata},default=str),flush=True)
 if not r.ok:raise SystemExit(1)
