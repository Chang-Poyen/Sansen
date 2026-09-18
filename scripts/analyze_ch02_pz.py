"""PZ values are in Hz in Spectre PSF, while polynomial roots use rad/s."""
from pathlib import Path
import os,json,re,itertools
ROOT=Path(__file__).resolve().parent.parent;os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/ch02-sim/mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze_ch02_linear import raw,OUT
cases={x['id']:x for x in json.loads((ROOT/'simulations/ch02/linear_cases.json').read_text())}
def parse_complex(value):
 if isinstance(value,complex):return value
 if isinstance(value,str):
  m=re.fullmatch(r'\(\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)\s*\)',value)
  if m:return complex(float(m[1]),float(m[2]))
 raise ValueError('Unexpected PZ complex encoding: '+repr(value))
def roots(name):
 p=cases[name]['params'];model=cases[name]['model']
 if model=='miller':
  return [-p['go']/(p['cf']*(1+p['rs']*p['go']+p['rs']*p['gm']))],[p['gm']/p['cf']]
 if model=='follower':
  gm,rs,cg,cd,c0=[p[x] for x in ['gm','rs','cg','cd','c0']];return np.roots([rs*(c0*cd+c0*cg+cd*cg),cg+c0+rs*gm*cd,gm]),[-gm/cg]
 if model=='two_stage':
  gm1,gm2,go1,go2,ci,cc,cl=[p[x] for x in ['gm1','gm2','go1','go2','ci','cc','cl']];return np.roots([ci*cl+ci*cc+cc*cl,go1*(cl+cc)+go2*(ci+cc)+gm2*cc,go1*go2]),[gm2/cc]
 if model=='gainboost':
  gm2,go1,go2,cl,b0,wb=[p[x] for x in ['gm2','go1','go2','cl','b0','wb']];dx=go1+go2+gm2;q=go2+gm2;return np.roots([cl*dx/wb,go1*go2/wb+cl*(dx+gm2*b0),go1*go2]),[-wb*(1+gm2*b0/q)]
 raise ValueError(model)
def compare(observed,expected):
 assert len(observed)==len(expected),(observed,expected)
 return min(max(abs(a-b)/max(abs(b),1e-30) for a,b in zip(order,expected)) for order in itertools.permutations(observed))
records=[];fig,axs=plt.subplots(2,3,figsize=(12,7),layout='constrained')
for i,name in enumerate(['miller','follower_cancel','follower_center','two_stage','gainboost_slow']):
 data=raw('pz_'+name,'poles.pz');pol=np.array([parse_complex(v) for k,v in data.items() if k.endswith(':pole')]);zer=np.array([parse_complex(v) for k,v in data.items() if k.endswith(':zero')]);ep,ez=roots(name);ep=np.array(ep,dtype=complex)/(2*np.pi);ez=np.array(ez,dtype=complex)/(2*np.pi);pe=compare(pol,ep);ze=compare(zer,ez)
 enc=lambda a:[[float(v.real),float(v.imag)] for v in a]
 records.append(dict(id=name,module=cases[name]['module'],passed=bool(max(pe,ze)<2e-5),unit='Hz (complex s divided by 2*pi)',spectre_poles=enc(pol),derived_poles=enc(ep),spectre_zeros=enc(zer),derived_zeros=enc(ez),max_relative_pole_error=pe,max_relative_zero_error=ze,docancel=False))
 ax=axs.ravel()[i];ax.scatter(pol.real/1e6,pol.imag/1e6,marker='x',s=65,label='Spectre 极点',color='#aa3e4b');ax.scatter(zer.real/1e6,zer.imag/1e6,marker='o',facecolors='none',s=110,label='Spectre 零点',edgecolors='#16666e');ax.axvline(0,color='#becac6',lw=.8);ax.axhline(0,color='#becac6',lw=.8);ax.set(title=name,xlabel='实部 Re(s/2π)（MHz）',ylabel='虚部 Im(s/2π)（MHz）');ax.grid(alpha=.2);ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4));ax.legend(fontsize=7)
axs.ravel()[-1].axis('off');axs.ravel()[-1].text(.02,.8,'极点与零点坐标来自 Spectre PZ\n\n已禁用自动极零相消。\nx/o 重叠表示极零相消。\n\n正实零点位于右半平面。',va='top',fontsize=11);fig.suptitle('Spectre 极点与零点分析');fig.savefig(OUT/'assets/pole_zero.svg');fig.savefig(ROOT/'tmp/ch02-sim/pole_zero.png',dpi=130);plt.close(fig)
(OUT/'pz_results.json').write_text(json.dumps(records,indent=2));print(json.dumps({'tests':len(records),'passed':sum(x['passed'] for x in records),'max_relative_error':max(max(x['max_relative_pole_error'],x['max_relative_zero_error']) for x in records)},indent=2))
if not all(x['passed'] for x in records):raise SystemExit(1)
