"""Validate MOS AC against OP-derived small-signal parameters; strictly parse PZ."""
from pathlib import Path
import os,json,csv,re
ROOT=Path(__file__).resolve().parent.parent;os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/ch02-sim/mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from virtuoso_bridge.spectre.psf import scalar,vector,frequency_hz
from analyze_ch02_linear import raw,expected,plot,OUT
cases=json.loads((ROOT/'simulations/ch02/mos_cases.json').read_text());dc=raw('mos_validation','dcOp.dc');ac=raw('mos_validation','ac.ac');f=np.array(frequency_hz(ac));s=2j*np.pi*f;results=[]
ops={}
for c in cases:
 for n in c['devices']:
  ops[n]={k:scalar(dc,n+':'+k) for k in ['gm','gds','ids','vgs','vds','vdsat','region','cgs','cgd','cgb','cbd','cbs']}
  # These explicit educational assumptions must fail loudly if models change.
  assert all(abs(ops[n][k])<1e-25 for k in ['cgd','cgb','cbd','cbs']),f'{n}: new parasitics need a revised reference model'
  ops[n]['gm_over_Id']=ops[n]['gm']/abs(ops[n]['ids'])
  ops[n]['saturation_margin_V']=abs(ops[n]['vds'])-abs(ops[n]['vdsat'])
  ops[n]['saturation_passed']=ops[n]['region']==2 and ops[n]['saturation_margin_V']>0
 for t in [c]:
  pp=[ops[x] for x in t['devices']];a=pp[0];gm,go,cg=a['gm'],a['gds'],a['cgs'];m=t['model'];refnotes=''
  if m=='mos_cs' or m=='mos_inverter':
   gm=sum(x['gm'] for x in pp);go=sum(x['gds'] for x in pp);ci=sum(x['cgs'] for x in pp);cf=t['cf'];cl=t['cl'];rs=t['rs'];d1=(cl+cf)/go+rs*(ci+cf)+(gm/go)*rs*cf;d2=rs/go*(ci*cl+ci*cf+cf*cl);h=-(gm/go)*(1-s*cf/gm)/(1+s*d1+s*s*d2);refnotes='完整双节点模型 with measured gm, gds and Cgs; external CL and feedback C retained.'
  elif m=='mos_follower':
   cd=t['cd_external'];c0=t['cl'];rs=t['rs'];h=(gm+s*cg)/(gm+go+s*(cg+c0+rs*gm*cd+rs*go*(cd+cg))+s*s*rs*(c0*cd+c0*cg+cd*cg));refnotes='Follower full two-node model retains measured go and Cgs plus added gate-drain capacitor.'
  elif m=='mos_cascode':
   b=pp[1];q=b['gm']+b['gds'];dx=go+q;cm=b['cgs']+t['cm_external'];cl=t['cl'];h=-gm*q/(go*b['gds']+s*(cl*dx+cm*b['gds'])+s*s*cm*cl);refnotes='Cascode middle-node capacitance includes top transistor Cgs, not just the added capacitor.'
  elif m=='mos_diode_load':
   b=pp[1];h=-gm/(go+b['gm']+b['gds']+s*(t['cl']+b['cgs']));refnotes='Diode PMOS Cgs loads the output and its gm contributes to output conductance.'
  elif m=='mos_degen':
   gs=1/t['rs'];gl=1/t['rl'];cl=t['cl'];h=(-gm*gs+s*cg*go)/((gs+gm+go+s*cg)*(go+gl+s*cl)-go*(gm+go));refnotes='Source degeneration includes dynamic Cgs coupling; low-frequency textbook formula alone is insufficient at high frequency.'
  else:raise ValueError(m)
  y=np.array(vector(ac,t['id']));err=abs(y-h)/np.maximum(abs(h),1e-20);opok=all(x['saturation_passed'] for x in pp)
  r={**t,'passed':bool(max(err)<2e-5 and opok),'max_relative_complex_error':float(max(err)),'samples':len(f),'all_devices_saturated':opok,'dc_output_V':scalar(dc,t['id']),'low_frequency_gain':float(y[0].real),'reference_notes':refnotes,'asset':f"assets/{t['id']}.svg",'csv':f"csv/{t['id']}.csv"};results.append(r)
  plot({'id':t['id'],'units':'V/V','model':'no_approximation','level':'educational MOS1','params':{}},f,y,h)
  with (OUT/r['csv']).open('w') as fh:
   w=csv.writer(fh);w.writerow(['frequency_Hz','spectre_real','spectre_imag','derived_real','derived_imag','relative_error']);w.writerows(zip(f,y.real,y.imag,h.real,h.imag,err))
(OUT/'mos_operating_points.json').write_text(json.dumps(ops,indent=2));(OUT/'mos_results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'mos_tests':len(results),'passed':sum(x['passed'] for x in results),'max_relative_error':max(x['max_relative_complex_error'] for x in results),'devices':len(ops)},indent=2),flush=True)
# Plot normalized gm/Id lookup and selected point.
lookup=np.genfromtxt(OUT/'csv/gmid_lookup.csv',delimiter=',',names=True);sel=json.loads((OUT/'gmid_selection.json').read_text());fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained');ax.plot(lookup['VOV_V'],lookup['N_gm_over_Id'],label='Spectre NMOS 仿真');ax.plot(lookup['VOV_V'],lookup['P_gm_over_Id'],'--',label='Spectre PMOS 仿真');ax.scatter([sel['selected_VOV_V']],[sel['gm_over_Id_measured_per_V']],color='#aa3e4b',zorder=3,label='选定值 10 V⁻¹');ax.set(xlabel='过驱动电压（V）',ylabel='gm / |Id| (1/V)',title='MOS1 仿真 gm/Id 查表 | L=2 μm，VDS=1 V');ax.grid(alpha=.2);ax.legend();fig.savefig(OUT/'assets/gmid_lookup.svg');plt.close(fig)
if not all(x['passed'] for x in results):raise SystemExit(1)
