"""Build explicit-element Spectre decks. Reference formulas are evaluated separately."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parent.parent; out=ROOT/'simulations/ch02/netlists';out.mkdir(parents=True,exist_ok=True)
lines=['simulator lang=spectre','global 0','// Linearized circuits: each gm source, ro and capacitor is an explicit element.',
'// VCCS terminal/current sign was checked by a real Spectre smoke run.',
'opts options reltol=1e-7 vabstol=1e-10 iabstol=1e-15 gmin=1e-16',
'Vin (vin 0) vsource dc=0 mag=1'];tests=[];uid=0

def elem(kind,nodes,**kw):
 global uid
 uid+=1;lines.append(f'{kind.upper()}{uid} ({" ".join(nodes)}) {kind} '+ ' '.join(f'{k}={v:.14g}' for k,v in kw.items()))
def R(a,b,v):elem('resistor',[a,b],r=v)
def C(a,b,v):
 if v:elem('capacitor',[a,b],c=v)
def V(a,b,ip,im,gain):elem('vcvs',[a,b,ip,im],gain=gain)
def G(d,s,g,gs,gm):elem('vccs',[d,s,g,gs],gm=gm)
def mos(d,g,s,gm,go,cgs=0,cgd=0,cds=0):
 G(d,s,g,s,gm)
 if go:R(d,s,1/go)
 C(g,s,cgs);C(g,d,cgd);C(d,s,cds)
def inj(n):
 # isource with positive current flowing from node 0 to n.
 elem('isource',['0',n],dc=0,mag=1)
def add(name,module,model,params,units='V/V',variant='nominal'):
 tests.append(dict(id=name,module=module,model=model,params=params,output=name,units=units,variant=variant));lines.append(f'// CASE {name}: {model}');return name
# 01-02: intrinsic gain and capacitive load
for name,cl,rl,module in [('intrinsic',0,1e12,'01-intrinsic-gain'),('loaded_cs',3e-12,1e12,'02-single-pole')]:
 p=dict(gm=.002,go=2e-5,cl=cl,rl=rl);o=add(name,module,'cs',p);mos(o,'vin','0',p['gm'],p['go']);R(o,'0',rl);C(o,'0',cl)
# 03: same topology, intentional valid/invalid Miller approximation conditions
for name,rs in [('miller',1e4),('miller_low_rs',10),('miller_high_rs',1e6)]:
 p=dict(gm=.002,go=2e-5,rs=rs,cf=.5e-12);o=add(name,'03-miller','miller',p,variant='source_resistance_sweep');g=name+'_g';R('vin',g,rs);mos(o,g,'0',p['gm'],p['go']);C(g,o,p['cf'])
# 04: source resistor degeneration and shorted-output input impedance with inductive degeneration
p=dict(gm=.002,go=2e-5,rs=1000,rl=10000);o=add('degeneration','04-degeneration','degeneration',p);sn=o+'_s';mos(o,'vin',sn,p['gm'],p['go']);R(sn,'0',p['rs']);R(o,'0',p['rl'])
p=dict(gm=.002,cg=1e-12,ls=10e-9);o=add('degeneration_zin','04-degeneration','degen_zin',p,'ohm');sn=o+'_s';inj(o);mos('0',o,sn,p['gm'],0,cgs=p['cg']);elem('inductor',[sn,'0'],l=p['ls'])
# 05: diode connected impedance and gain with a diode-connected load
p=dict(gm=.001,go=1e-5,c=1e-12);o=add('diode_z','05-diode-loads','diode_z',p,'ohm');inj(o);mos(o,o,'0',p['gm'],p['go']);C(o,'0',p['c'])
p=dict(gm=.002,go=2e-5,gml=.001,gol=1e-5,c=1e-12);o=add('diode_load','05-diode-loads','diode_load',p);mos(o,'vin','0',p['gm'],p['go']);mos(o,o,'0',p['gml'],p['gol']);C(o,'0',p['c'])
# 06-07: the two devices both drive the output; their gm and go add.
for name,ci,cf,rs,module in [('inverter_dc',0,0,1,'06-inverter-dc'),('inverter_ac',1e-12,.2e-12,1e4,'07-inverter-ac')]:
 p=dict(gmn=.002,gmp=.002,gon=2e-5,gop=2e-5,ci=ci,cf=cf,cl=3e-12,rs=rs);o=add(name,module,'inverter',p);g=o+'_g';R('vin',g,rs);mos(o,g,'0',p['gmn'],p['gon']);mos(o,g,'0',p['gmp'],p['gop']);C(g,'0',ci);C(g,o,cf);C(o,'0',p['cl'])
# 08: finite bias conductance + grounded-bulk transconductance
p=dict(gm=.002,gmb=.0004,go=2e-5,gb=1e-5,cl=3e-12);o=add('follower_dc','08-followers-dc','follower_dc',p);mos('0','vin',o,p['gm'],p['go']);G('0',o,'0',o,p['gmb']);R(o,'0',1/p['gb']);C(o,'0',p['cl'])
# 09 + 11: high-frequency source follower, separate voltage- and output-impedance tests.
for name,gm in [('cancel',1e-12/(1e4*1.2e-12)),('book',4e-12/(1e4*1.2e-12)),('center',.002)]:
 for impedance in [False,True]:
  p=dict(gm=gm,go=0,gb=0,rs=1e4,cg=1e-12,cd=.2e-12,c0=3e-12,impedance=impedance);o=add('follower_'+name+('_z' if impedance else ''),'09-followers-hf','follower',p,'ohm' if impedance else 'V/V',name);g=o+'_g';R('0' if impedance else 'vin',g,p['rs']);mos('0',g,o,gm,0,cgs=p['cg'],cgd=p['cd'],cds=p['c0']);
  if impedance:inj(o)
# 10: 混合 π 型 BJT with finite beta and explicitly fixed Cpi at the chosen bias
p=dict(gm=.002,go=1e-5,beta=100,rs=1e4,cpi=1.4e-12,cmu=.2e-12,cce=1e-12);o=add('bjt_follower_z','10-emitter-hf','bjt_follower',p,'ohm');b=o+'_b';R(b,'0',p['rs']);mos('0',b,o,p['gm'],p['go'],cgs=p['cpi'],cgd=p['cmu'],cds=p['cce']);R(b,o,p['beta']/p['gm']);inj(o)
p=dict(gm=.002,rs=1e4,cg=1e-12);o=add('active_inductor','11-active-inductors','active_inductor',p,'ohm');g=o+'_g';R(g,'0',p['rs']);mos('0',g,o,p['gm'],0,cgs=p['cg']);inj(o)
# 12: common gate current input and finite bias/load impedances
p=dict(gm=.002,go=2e-5,rb=1e5,rl=1e6);o=add('common_gate','12-common-gate','common_gate',p,'ohm');sn=o+'_s';inj(sn);R(sn,'0',p['rb']);R(o,'0',p['rl']);mos(o,'0',sn,p['gm'],p['go'])
# 13-16: cascodes, middle-node parasitics, telescopic opposite branch and folded bias branch
for name,rs,cf,cm,top,fold,module in [('cascode',1,0,0,0,0,'13-cascode'),('cascode_miller',1e4,.5e-12,0,0,0,'14-cascode-miller'),('cascode_cm_small',1,0,1e-12,0,0,'15-cascode-middle-cap'),('cascode_cm_large',1,0,1e-9,0,0,'15-cascode-middle-cap'),('telescopic',1,0,0,1,0,'16-telescopic-folded'),('folded',1,0,0,0,1,'16-telescopic-folded')]:
 p=dict(gm1=.002,gm2=.002,go1=2e-5,go2=2e-5,cl=3e-12,rs=rs,cf=cf,cm=cm,top=top,fold=fold,rb1=5e4,rb2=5e6);o=add(name,module,'cascode',p);x=o+'_x';g=o+'_g';R('vin',g,rs);mos(x,g,'0',p['gm1'],p['go1']);mos(o,'0',x,p['gm2'],p['go2']);C(o,'0',p['cl']);C(g,x,cf);C(x,'0',cm)
 if top:
  # PMOS branch linearized around its bias: same passive output resistance.
  y=o+'_y';mos(y,'0','0',.002,2e-5);mos(o,'0',y,.002,2e-5)
 if fold:R(x,'0',p['rb1']);R(o,'0',p['rb2'])
# 17: physical two-stage Miller compensation.
p=dict(gm1=.002,gm2=.004,go1=2e-5,go2=2e-5,ci=1e-12,cc=3e-12,cl=5e-12);o=add('two_stage','17-cascade','two_stage',p);x=o+'_x';mos(x,'vin','0',p['gm1'],p['go1']);mos(o,x,'0',p['gm2'],p['go2']);C(x,'0',p['ci']);C(x,o,p['cc']);C(o,'0',p['cl'])
# 18: auxiliary amplifier implemented as a VCVS followed by actual R/C.
for name,wb in [('gainboost_slow',2*math.pi*1e3),('gainboost_fast',2*math.pi*1e6)]:
 p=dict(gm1=.002,gm2=.002,go1=2e-5,go2=2e-5,cl=3e-12,b0=20,wb=wb);o=add(name,'18-gain-boosting','gainboost',p);x=o+'_x';a=o+'_a';a0=o+'_a0';mos(x,'vin','0',p['gm1'],p['go1']);mos(o,a,x,p['gm2'],p['go2']);C(o,'0',p['cl']);V(a0,'0',x,'0',-p['b0']);R(a0,a,1000);C(a,'0',1/(1000*wb))
# 20: finite-beta BJT input/output tests with emitter degeneration and base resistance
for name,typ in [('bjt_degen_gain','bjt_degen_gain'),('bjt_degen_zout','bjt_degen_zout')]:
 p=dict(gm=.002,go=2e-5,beta=100,rb=500,rbext=1000,re=1000,rl=10000);o=add(name,'20-port-summary',typ,p,'ohm' if typ.endswith('zout') else 'V/V');b=o+'_b';sn=o+'_e';R('0' if typ.endswith('zout') else 'vin',b,p['rb']+p['rbext']);R(b,sn,p['beta']/p['gm']);R(sn,'0',p['re']);mos(o,b,sn,p['gm'],p['go'])
 if typ.endswith('zout'):inj(o)
 else:R(o,'0',p['rl'])
lines+=['ac ac start=1 stop=1T dec=60','dcOp dc','save vin '+' '.join(t['output'] for t in tests),'saveOptions options save=selected']
(out/'linear_suite.scs').write_text('\n'.join(lines)+'\n')
(ROOT/'simulations/ch02/linear_cases.json').write_text(json.dumps(tests,indent=2))
# gm/Id characterization: normalized widths, sweep overdrive using native Spectre DC.
model='''// EDUCATIONAL MOS1 only: chosen textbook-like constants, not a foundry PDK.
// MOS terminal order: D G S B.
model N_EDU mos1 type=n vto=0.45 kp=100u lambda=0.1 gamma=0 phi=0.7 tox=10n cgso=0 cgdo=0 cbd=0 cbs=0
model P_EDU mos1 type=p vto=-0.45 kp=100u lambda=0.1 gamma=0 phi=0.7 tox=10n cgso=0 cgdo=0 cbd=0 cbs=0'''
(ROOT/'simulations/ch02/educational_models.txt').write_text(model+'\n')
(out/'gmid_characterization.scs').write_text('''simulator lang=spectre
global 0
parameters VOV=0.2
'''+model+'''
opts options reltol=1e-7 vabstol=1e-10 iabstol=1e-15 gmin=1e-16
VGN (gn 0) vsource dc=0.45+VOV
VDN (dn 0) vsource dc=1
MN (dn gn 0 0) N_EDU w=20u l=2u
VSP (sp 0) vsource dc=2
VGP (gp 0) vsource dc=1.55-VOV
VDP (dp 0) vsource dc=1
MP (dp gp sp sp) P_EDU w=20u l=2u
characterize dc param=VOV start=0.05 stop=0.60 step=0.005
save MN:ids MN:gm MN:gds MN:cgs MN:cgd MN:vdsat MN:region MP:ids MP:gm MP:gds MP:cgs MP:cgd MP:vdsat MP:region
saveOptions options save=selected
''')
# Closed-loop doublet and no-doublet transient: integrator and RC element implementations.
tran=['simulator lang=spectre','global 0','opts options reltol=1e-7 vabstol=1e-10 iabstol=1e-15 gmin=1e-16','VSTEP (vin 0) vsource type=pulse val0=0 val1=1 delay=1u rise=1n fall=1n width=2m period=4m'];old=lines;lines=tran
u=2*math.pi*1e6
for name,p,z in [('tail',2*math.pi*12e3,2*math.pi*2e3),('overshoot',2*math.pi*2e3,2*math.pi*12e3)]:
 e=name+'_e';lp=name+'_lp';V(e,'0','vin',name,1);R(e,lp,1);C(lp,'0',1/p);C(name,'0',1);G(name,'0',e,'0',-u);G(name,'0',lp,'0',-u*(z/p-1))
C('baseline','0',1);G('baseline','0','vin','baseline',-u)
lines+=['tran tran stop=601u maxstep=100n errpreset=conservative','save vin tail overshoot baseline','saveOptions options save=selected']
(out/'doublet_transient.scs').write_text('\n'.join(lines)+'\n')
print(f'Generated {len(tests)} independent linear tests, gm/Id characterization and transient decks.')
