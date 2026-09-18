"""Choose dimensions from Spectre gm/Id data, then generate real MOS1 circuits."""
from pathlib import Path
import json,csv,math
import numpy as np
from project_runtime import raw_output_dir
from virtuoso_bridge.spectre.psf import read_psf_ascii,result_file,vector
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'output/simulations/ch02';NET=ROOT/'simulations/ch02/netlists'
r=json.loads((OUT/'runs/gmid_characterization/result.json').read_text());assert r['ok'];d=read_psf_ascii(result_file(raw_output_dir(OUT/'runs/gmid_characterization',r['metadata']),'characterize.dc'))
vov=np.array(vector(d,'VOV')).real;gm=np.array(vector(d,'MN:gm')).real;ids=np.abs(np.array(vector(d,'MN:ids')).real);ratio=gm/ids
# Workpoint is selected from simulated gm/Id, width from simulated current density.
target=10.;ix=int(np.argmin(abs(ratio-target)));gm_target=2*math.pi*100e6*3e-12
id_target=gm_target/target;width=20e-6*id_target/ids[ix];vg=.45+vov[ix]
selection=dict(model='Educational MOS1; not a foundry PDK',gm_over_Id_target_per_V=target,gm_over_Id_measured_per_V=float(ratio[ix]),lookup_VDS_V=1,lookup_L_m=2e-6,lookup_W_m=20e-6,selected_VOV_V=float(vov[ix]),selected_VGS_V=float(vg),gm_target_S=gm_target,Id_target_A=id_target,selected_W_m=width,selected_L_m=2e-6,width_method='W = Id_target / (Id_lookup / W_lookup); operating point selected from measured gm/Id.',book_W_m=188.4955592153876e-6,book_difference_reason='MOS1 includes (1+lambda*VDS)=1.1 in DC current; the textbook sizing approximation omits it.')
(OUT/'gmid_selection.json').write_text(json.dumps(selection,indent=2))
with (OUT/'csv/gmid_lookup.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['VOV_V','N_ids_A','N_gm_S','N_gds_S','N_gm_over_Id','P_abs_ids_A','P_gm_S','P_gm_over_Id'])
 pids=np.abs(np.array(vector(d,'MP:ids')).real);pgm=np.array(vector(d,'MP:gm')).real
 w.writerows(zip(vov,ids,gm,np.array(vector(d,'MN:gds')).real,ratio,pids,pgm,pgm/pids))
model=(ROOT/'simulations/ch02/educational_models.txt').read_text()
lines=['simulator lang=spectre','global 0',model,'opts options reltol=1e-7 vabstol=1e-10 iabstol=1e-15 gmin=1e-16','VDD (vdd 0) vsource dc=3'];moses=[];cases=[]
def v(n,node,dc,ac=False):lines.append(f'V_{n} ({node} 0) vsource dc={dc:.14g}'+(' mag=1' if ac else ''))
def m(n,d,g,s,b,typ='N_EDU'):
 lines.append(f'M_{n} ({d} {g} {s} {b}) {typ} w={width:.14g} l=2u');moses.append('M_'+n)
def load(o,current):lines.append(f'I_{o} (vdd {o}) isource dc={current:.14g}')
def cap(n,a,b,c):lines.append(f'C_{n} ({a} {b}) capacitor c={c:.14g}')
def resistor(n,a,b,r):lines.append(f'R_{n} ({a} {b}) resistor r={r:.14g}')
for name,rs,cf in [('mos_cs',0,0),('mos_miller',10000,.5e-12)]:
 v(name+'_in',name+'_in',vg,True);g=name+'_in'
 if rs:g=name+'_g';resistor(name+'_source',name+'_in',g,rs)
 m(name,name,g,'0','0');load(name,id_target);cap(name+'_load',name,'0',3e-12)
 if cf:cap(name+'_feedback',g,name,cf)
 cases.append(dict(id=name,module='03-miller' if cf else '02-single-pole',model='mos_cs',devices=['M_'+name],rs=rs,cf=cf,cl=3e-12))
# Grounded-bulk effect is disabled explicitly by the model gamma=0; source/bulk tied below.
name='mos_follower';v(name+'_in',name+'_in',1+vg,True);resistor(name+'_source',name+'_in',name+'_g',1e4);v(name+'_drain',name+'_d',2);m(name,name+'_d',name+'_g',name,name);lines.append(f'I_{name} ({name} 0) isource dc={id_target:.14g}');cap(name+'_load',name,'0',3e-12);cap(name+'_gate_drain',name+'_g',name+'_d',.2e-12);cases.append(dict(id=name,module='09-followers-hf',model=name,devices=['M_'+name],rs=1e4,cd_external=.2e-12,cl=3e-12))
name='mos_cascode';v(name+'_in',name+'_in',vg,True);v(name+'_bias',name+'_bias',1+vg);m(name+'_bottom',name+'_x',name+'_in','0','0');m(name+'_top',name,name+'_bias',name+'_x',name+'_x');load(name,id_target);cap(name+'_load',name,'0',3e-12);cap(name+'_middle',name+'_x','0',.1e-12);cases.append(dict(id=name,module='13-cascode',model=name,devices=['M_'+name+'_bottom','M_'+name+'_top'],cl=3e-12,cm_external=.1e-12))
name='mos_inverter';v(name+'_supply',name+'_supply',2*vg);v(name+'_in',name+'_in',vg,True);resistor(name+'_source',name+'_in',name+'_g',10000);m(name+'_n',name,name+'_g','0','0');m(name+'_p',name,name+'_g',name+'_supply',name+'_supply','P_EDU');cap(name+'_load',name,'0',3e-12);cap(name+'_feedback',name+'_g',name,.2e-12);cases.append(dict(id=name,module='07-inverter-ac',model=name,devices=['M_'+name+'_n','M_'+name+'_p'],rs=10000,cf=.2e-12,cl=3e-12))
name='mos_diode_load';v(name+'_supply',name+'_supply',2*vg);v(name+'_in',name+'_in',vg,True);m(name+'_n',name,name+'_in','0','0');m(name+'_p',name,name,name+'_supply',name+'_supply','P_EDU');cap(name+'_load',name,'0',3e-12);cases.append(dict(id=name,module='05-diode-loads',model=name,devices=['M_'+name+'_n','M_'+name+'_p'],cl=3e-12))
name='mos_degen';v(name+'_in',name+'_in',vg+.2,True);m(name,name,name+'_in',name+'_s',name+'_s');rs=.2/id_target;resistor(name+'_source',name+'_s','0',rs);resistor(name+'_load',name,'0',10000);load(name,id_target+1.2/10000);cap(name+'_load',name,'0',3e-12);cases.append(dict(id=name,module='04-degeneration',model=name,devices=['M_'+name],rs=rs,rl=10000,cl=3e-12))
lines+=['dcOp dc','ac ac start=1 stop=10G dec=60','save '+' '.join(c['id'] for c in cases),'save '+' '.join(n+':'+key for n in moses for key in ['gm','gds','ids','vgs','vds','vdsat','region','cgs','cgd','cgb','cbd','cbs']),'saveOptions options save=selected']
(NET/'mos_validation.scs').write_text('\n'.join(lines)+'\n');(ROOT/'simulations/ch02/mos_cases.json').write_text(json.dumps(cases,indent=2))
# Independent PZ decks retain one DUT so poles from other test circuits cannot leak in.
source=(NET/'linear_suite.scs').read_text();names=['miller','follower_cancel','follower_center','two_stage','gainboost_slow']
for name in names:
 start=source.index('// CASE '+name+':');end=source.find('// CASE ',start+4)
 if end<0:end=source.index('ac ac start=',start)
 block=source[start:end]
 deck='simulator lang=spectre\nglobal 0\nVin (vin 0) vsource dc=0 mag=1\n'+block+f'\npoles ({name} 0) pz iprobe=Vin docancel=no\nac ac start=1 stop=1T dec=10\nsave {name}\nsaveOptions options save=selected\n'
 (NET/('pz_'+name+'.scs')).write_text(deck)
print(json.dumps(selection,indent=2));print('Generated 7 MOS circuits and 5 independent PZ decks.')
