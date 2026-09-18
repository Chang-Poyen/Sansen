"""Independent KCL/SFG/algebra checks and numerical illustrations; not SPICE."""
import sys, json, math, os
from pathlib import Path
sys.path.insert(0,str(Path('tmp/ch02/python-deps').resolve()))
import sympy as S
import numpy as np
os.environ.setdefault('MPLCONFIGDIR',str(Path('tmp/ch02/mpl-cache').resolve()))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path('output/derivations/ch02')
assets=Path('derivations/ch02/assets')
out.mkdir(parents=True,exist_ok=True); assets.mkdir(parents=True,exist_ok=True)
from verify_physical_sfg import verify_models
physical_report=verify_models()
checks=[{'name': m['id']+' Physical/Causal SFG local constraints vs KCL', 'passed':m['passed'], 'residual':'0'} for m in physical_report['models']]
def eq(name,a,b=0):
    residual=S.factor(S.cancel(a-b))
    ok=residual==0
    checks.append({'name':name,'passed':bool(ok),'residual':str(residual)})
    if not ok: print('FAILED',name,residual,flush=True)

s,gm,gm1,gm2,go,go1,go2,Rs,RL,RB,CL,Ci,CF,Cg,Cd,C0,Cm,gb=S.symbols(
    's gm gm1 gm2 go go1 go2 Rs RL RB CL Ci CF Cg Cd C0 Cm gb', positive=True)
Gs=1/Rs
# Device differentiation and elementary stages
K,W,L,V,Vt,Id,VA=S.symbols('K W L V Vt Id VA', positive=True)
eq('MOS square-law derivative',S.diff(K*W/L*(V-Vt)**2,V),2*K*W/L*(V-Vt))
eq('CS KCL',-gm/(go+1/RL),-gm*(RL/(1+go*RL)))
eq('CL single-pole KCL',-gm/(go+s*CL),(-gm/go)/(1+s*CL/go))
# Miller
M=S.Matrix([[Gs+s*CF,-s*CF],[gm-s*CF,go+s*CF]])
H=(M.inv()*S.Matrix([Gs,0]))[1]
HM=(s*CF-gm)/(go+s*CF*(1+Rs*go+Rs*gm))
eq('Miller 2-node KCL vs closed form',H,HM)
eq('Miller RHP zero',S.factor(S.together(HM)).as_numer_denom()[0].subs(s,gm/CF))
eq('Miller high-frequency plateau',S.limit(HM,s,S.oo),1/(1+gm*Rs+go*Rs))
# Degeneration
Z=S.symbols('Z',positive=True)
vx=(gm*S.Symbol('vi')+go*S.Symbol('vo'))/(1/Z+gm+go)
idexpr=gm*(S.Symbol('vi')-vx)+go*(S.Symbol('vo')-vx)
eq('Source degeneration transconductance',S.diff(idexpr,S.Symbol('vi')),gm/(1+(gm+go)*Z))
eq('Source degeneration output resistance',1/S.diff(idexpr,S.Symbol('vo')),1/go+(1+gm/go)*Z)
Ls=S.symbols('Ls',positive=True)
eq('Inductive degeneration Zin',(1+s*Ls*(gm+s*Cg))/(s*Cg),1/(s*Cg)+s*Ls+gm*Ls/Cg)
g2m=S.symbols('g2m',positive=True)
Dx=gm1+go1+go2
hx=(gm1-g2m)/Dx
eq('MOS-resistor gm including lower-gate response',g2m+go2*hx,(gm1*go2+g2m*(gm1+go1))/Dx)
# Diode and inverter
vt=S.symbols('vt')
eq('Diode-connected test-source resistance',vt/(gm*vt+go*vt),1/(gm+go))
Gm,Go=S.symbols('Gm Go',positive=True)
MI=S.Matrix([[Gs+s*(Ci+CF),-s*CF],[Gm-s*CF,Go+s*(CL+CF)]])
Hi=(MI.inv()*S.Matrix([Gs,0]))[1]
a1=(CL+CF)/Go+Rs*(Ci+CF)+(Gm/Go)*Rs*CF
a2=Rs/Go*(Ci*CL+Ci*CF+CF*CL)
Hie=-(Gm/Go)*(1-s*CF/Gm)/(1+s*a1+s*s*a2)
eq('Inverter full two-node transfer',Hi,Hie)
eq('Inverter RHP zero uses total Gm',S.together(Hi).as_numer_denom()[0].subs(s,Gm/CF))
eq('Inverter input-only two poles',Hi.subs(CF,0),-(Gm/Go)/((1+s*Rs*Ci)*(1+s*CL/Go)))
# Follower
MF=S.Matrix([[Gs+s*(Cd+Cg),-s*Cg],[-gm-s*Cg,gm+go+gb+s*(Cg+C0)]])
C2=C0*Cd+C0*Cg+Cd*Cg
D=gm+go+gb+s*(Cg+C0+Rs*gm*Cd+Rs*(go+gb)*(Cd+Cg))+s*s*Rs*C2
Hf=(MF.inv()*S.Matrix([Gs,0]))[1]
Zf=(MF.inv()*S.Matrix([0,1]))[1]
eq('Follower full voltage transfer',Hf,(gm+s*Cg)/D)
eq('Follower full output impedance',Zf,(1+s*Rs*(Cd+Cg))/D)
D0=D.subs({go:0,gb:0}); gc=Cg/(Rs*(Cd+Cg))
eq('Follower voltage cancellation residual',D0.subs(s,-gm/Cg),C0*gm*(Rs*gm*(Cd+Cg)-Cg)/Cg**2)
eq('Follower impedance cancellation residual',D0.subs(s,-1/(Rs*(Cd+Cg))),
   Cg*(Rs*gm*(Cd+Cg)-Cg)/(Rs*(Cd+Cg)**2))
ceff=C0+Cg*Cd/(Cg+Cd)
eq('Follower exact one-pole voltage at cancellation',Hf.subs({go:0,gb:0,gm:gc}),gc/(gc+s*ceff))
eq('Follower exact one-pole impedance at cancellation',Zf.subs({go:0,gb:0,gm:gc}),1/(gc+s*ceff))
x,k=S.symbols('x k',positive=True)
xp=(S.sqrt(k)+S.sqrt(k-1))**2; xm=(S.sqrt(k)-S.sqrt(k-1))**2
eq('Complex-region upper root',(xp+1)**2-4*k*xp)
eq('Complex-region lower root',(xm+1)**2-4*k*xm)
eq('Complex-region roots reciprocal',xp*xm,1)
# BJT high frequency matrix
gp,Cpi,Cmu,Cce=S.symbols('gp Cpi Cmu Cce',positive=True)
Y=gp+s*Cpi
MB=S.Matrix([[Gs+Y+s*Cmu,-Y],[-(gm+Y),gm+Y+go+s*Cce]])
Db=(Gs+Y+s*Cmu)*(gm+Y+go+s*Cce)-Y*(gm+Y)
eq('BJT output impedance matrix',(MB.inv()*S.Matrix([0,1]))[1],(Gs+Y+s*Cmu)/Db)
sz=-(Gs+gp)/(Cpi+Cmu)
eq('BJT output zero residual structure',Db.subs(s,sz),-(gp+sz*Cpi)*(gm+gp+sz*Cpi))
beta,tau,Cje=S.symbols('beta tau Cje',positive=True)
condition=gm*(Cpi+Cmu)+gp*Cmu-Gs*Cpi
eq('BJT diffusion-cap cancellation quadratic',
   condition.subs({Cpi:Cje+gm*tau,gp:gm/beta}),
   tau*gm**2+gm*(Cje+Cmu+Cmu/beta-Gs*tau)-Gs*Cje)
# Active inductance
Za=(1+s*Rs*Cg)/(gm+s*Cg)
Leff=Cg/gm*(Rs-1/gm)
eq('Active inductor exact decomposition',Za,1/gm+s*Leff/(1+s*Cg/gm))
eq('Active inductor low-frequency L',S.diff(Za,s).subs(s,0),Leff)
# Common gate
MCG=S.Matrix([[1/RB+gm+go,-go],[-gm-go,1/RL+go]])
sol=MCG.inv()*S.Matrix([1,0]); Q=1+gm/go
AR=Q*RB*RL/(RL+1/go+Q*RB)
Rin=RB*(RL+1/go)/(RL+1/go+Q*RB)
eq('Common-gate transresistance',sol[1],AR)
eq('Common-gate input resistance',sol[0],Rin)
eq('Common-gate open output limit',S.limit(AR,RL,S.oo),Q*RB)
# Cascode
Q2=gm2+go2; Dxx=go1+Q2
MC=S.Matrix([[Dxx,-go2],[-Q2,go2+1/RL+s*CL]])
hc=(MC.inv()*S.Matrix([-gm1,0]))[1]
eq('Cascode transfer',hc,-gm1*Q2/(go1*go2+Dxx/RL+s*Dxx*CL))
eq('Cascode intrinsic Rout',Dxx/(go1*go2),1/go1+1/go2+gm2/(go1*go2))
# Cascode gate-x Miller cap
MM=S.Matrix([[Gs+s*CF,-s*CF,0],[gm1-s*CF,Dxx+s*CF,-go2],[0,-Q2,go2+s*CL]])
hm=(MM.inv()*S.Matrix([Gs,0,0]))[2]
d0=go1*go2
d1=CL*Dxx+CF*go2*(1+Rs*(go1+gm1))
d2=CF*CL*(1+Rs*(Dxx+gm1))
eq('Cascode Miller 3-node quadratic',hm,Q2*(s*CF-gm1)/(d0+s*d1+s*s*d2))
# Grounded middle cap
MMID=S.Matrix([[Dxx+s*Cm,-go2],[-Q2,go2+s*CL]])
hmiddle=(MMID.inv()*S.Matrix([-gm1,0]))[1]
eq('Cascode middle-cap quadratic',hmiddle,-gm1*Q2/(go1*go2+s*(CL*Dxx+Cm*go2)+s*s*Cm*CL))
# Two-stage compensated cascade
MCC=S.Matrix([[go1+s*(Ci+CF),-s*CF],[gm2-s*CF,go2+s*(CL+CF)]])
hcc=(MCC.inv()*S.Matrix([-gm1,0]))[1]
Dcc=go1*go2+s*(go1*(CL+CF)+go2*(Ci+CF)+gm2*CF)+s*s*(Ci*CL+Ci*CF+CF*CL)
eq('Miller-compensated cascade transfer',hcc,gm1*(gm2-s*CF)/Dcc)
# Gain boosting and explicit SFG
B,B0,wb=S.symbols('B B0 wb',positive=True)
MBST=S.Matrix([[Dxx,-gm2,-go2],[B,1,0],[-Q2,gm2,go2+s*CL]])
hb=(MBST.inv()*S.Matrix([-gm1,0,0]))[2]
hbe=-gm1*(go2+gm2*(1+B))/(go1*go2+s*CL*(go1+go2+gm2*(1+B)))
eq('Gain boost KCL',hb,hbe)
hbd=hbe.subs(B,B0/(1+s/wb))
db=go1*go2*(1+s/wb)+s*CL*(Dxx*(1+s/wb)+gm2*B0)
eq('Gain boost auxiliary-pole quadratic',hbd,-gm1*(Q2*(1+s/wb)+gm2*B0)/db)
zboost=(MBST.inv()*S.Matrix([0,0,1]))[2]
eq('Gain boost output test-source resistance',zboost.subs(s,0),1/go1+1/go2+gm2*(1+B)/(go1*go2))
eq('Gain boost DC gain',hbd.subs(s,0),-gm1/go1*(1+gm2/go2*(1+B0)))
wz=wb*(1+gm2*B0/Q2)
eq('Gain boost exact zero cancellation condition',
   db.subs(s,-wz).subs(wb,(go2/CL)/(1+gm2*B0/Q2)),0)
# Doublet exact step residual
p,z,u=S.symbols('p z u',positive=True)
lf,ls=S.symbols('lf ls',positive=True)
As=(p-ls)/(lf-ls); Af=(lf-p)/(lf-ls)
eq('Doublet residue initial-value normalization',As+Af,1)
eq('Doublet partial fractions',Af/(s+lf)+As/(s+ls),(s+p)/((s+lf)*(s+ls)))
Acl=u/s*(s+z)/(s+p)
eq('Doublet unity-feedback transfer',Acl/(1+Acl),u*(s+z)/(s*s+(p+u)*s+u*z))
# BJT CB counterpart
MCB=S.Matrix([[1/RB+gp+gm+go,-go],[-gm-go,1/RL+go]])
bsol=MCB.inv()*S.Matrix([1,0])
Rstar=1/(1/RB+gp)
eq('BJT common-base RB parallel rpi',bsol[1],AR.subs(RB,Rstar))

# Independent numerical nodal solves at random complex frequencies.
rng=np.random.default_rng(20260915)
numeric=[]
for name,mat,rhs,ix,expr,syms in [
 ('Miller',M,S.Matrix([Gs,0]),1,HM,[gm,go,Rs,CF]),
 ('Inverter',MI,S.Matrix([Gs,0]),1,Hie,[Gm,Go,Rs,Ci,CF,CL]),
 ('Follower',MF,S.Matrix([Gs,0]),1,(gm+s*Cg)/D,[gm,go,gb,Rs,Cg,Cd,C0]),
 ('Cascode',MC,S.Matrix([-gm1,0]),1,-gm1*Q2/(go1*go2+Dxx/RL+s*Dxx*CL),[gm1,gm2,go1,go2,RL,CL]),
]:
    maxerr=0
    for _ in range(30):
        vals={}
        for v in syms:
            n=str(v)
            vals[v]=float(10**rng.uniform(-13,-10) if n.startswith('C') else
                          10**rng.uniform(2,6) if n.startswith('R') else
                          10**rng.uniform(-4,-2) if n.startswith('gm') or n=='Gm' else
                          10**rng.uniform(-8,-4))
        vals[s]=1j*2*np.pi*10**rng.uniform(2,10)
        mn=np.array(mat.subs(vals).evalf(),dtype=complex)
        bn=np.array(rhs.subs(vals).evalf(),dtype=complex).ravel()
        nodal=np.linalg.solve(mn,bn)[ix]
        analytic=complex(expr.subs(vals).evalf())
        err=abs(nodal-analytic)/max(abs(nodal),abs(analytic),1e-20)
        maxerr=max(maxerr,float(err))
    numeric.append({'model':name,'samples':30,'max_relative_error':maxerr,'passed':maxerr<1e-8})

# Reproducible illustrative values, not PDK device data
from project_runtime import plot_font_families
plt.rcParams.update({'font.family':plot_font_families(),'font.size':11,'axes.spines.top':False,
                     'axes.spines.right':False,'svg.fonttype':'path'})
def style(ax):
    ax.grid(True,which='both',alpha=.18)
fig,axs=plt.subplots(2,1,figsize=(9.2,6.7),sharex=True,layout='constrained')
freq=np.logspace(3,10,1400); ss=2j*np.pi*freq
mg,ro,rs,cf=2e-3,50e3,10e3,.5e-12
full=(ss*cf-mg)/(1/ro+ss*cf*(1+rs/ro+rs*mg))
ap=-(mg*ro)/(1+ss*cf*mg*rs*ro)
axs[0].semilogx(freq,20*np.log10(abs(full)),label='完整双节点模型',color='#16666e')
axs[0].semilogx(freq,20*np.log10(abs(ap)),'--',label='米勒单极点近似',color='#bd6c28')
axs[1].semilogx(freq,np.unwrap(np.angle(full/(-mg*ro)))*180/np.pi,color='#16666e')
axs[1].semilogx(freq,np.unwrap(np.angle(ap/(-mg*ro)))*180/np.pi,'--',color='#bd6c28')
for ax in axs: style(ax);ax.axvline(mg/(2*np.pi*cf),color='#a43244',ls=':',alpha=.8)
axs[0].set_ylabel('幅度（dB）');axs[0].legend();axs[1].set_ylabel('相对低频相位（°）');axs[1].set_xlabel('频率（Hz）')
fig.suptitle('米勒反馈：右半平面零点引起的相位变化')
fig.savefig(assets/'miller-comparison.svg');fig.savefig('tmp/ch02/miller-comparison.png',dpi=140);plt.close(fig)

rs,cg,cd,c0=1e4,1e-12,.2e-12,3e-12
gcancel=cg/(rs*(cg+cd));gbook=(cg+c0)/(rs*(cg+cd))
gcenter=(cg+c0)/(rs*cd)
rr=c0*cg/(cd*(c0+cg)); kk=1+rr
glo=gcenter*(math.sqrt(kk)-math.sqrt(kk-1))**2
ghi=gcenter*(math.sqrt(kk)+math.sqrt(kk-1))**2
freq=np.logspace(3,9,1400);ss=2j*np.pi*freq
fig,axs=plt.subplots(2,1,figsize=(9.2,6.8),sharex=True,layout='constrained')
for g,label,col in [(gcancel,'精确极零相消','#16666e'),
                    (gbook,'幻灯片 0243 的估算（C_DS = C0）','#bd6c28'),
                    (gcenter,'复极点区间中心','#a43244')]:
    den=g+ss*(cg+c0+rs*g*cd)+ss*ss*rs*(c0*cd+c0*cg+cd*cg)
    hh=(g+ss*cg)/den; zz=(1+ss*rs*(cd+cg))/den
    axs[0].semilogx(freq,20*np.log10(abs(hh)),label=label,color=col)
    axs[1].loglog(freq,abs(zz),color=col)
axs[0].set_ylabel('电压增益（dB）');axs[0].legend(fontsize=9)
axs[1].set_ylabel('输出阻抗（Ω）');axs[1].set_xlabel('频率（Hz）')
for ax in axs:style(ax)
fig.suptitle('跟随器：精确极零相消与渐近估算')
fig.savefig(assets/'follower-comparison.svg');fig.savefig('tmp/ch02/follower-comparison.png',dpi=140);plt.close(fig)

u=2*np.pi*1e6; pn=2*np.pi*12e3; zn=2*np.pi*2e3
lam=np.sort(np.roots([1,pn+u,u*zn])*-1);lsn,lfn=lam
asn=(pn-lsn)/(lfn-lsn); afn=1-asn
t=np.linspace(0,600e-6,3000)
err=afn*np.exp(-lfn*t)+asn*np.exp(-lsn*t)
fig,axs=plt.subplots(2,1,figsize=(9.2,6.8),layout='constrained')
axs[0].plot(t*1e6,1-np.exp(-u*t),label='无极零对',color='#16666e')
axs[0].plot(t*1e6,1-err,label='单位反馈下的精确极零对模型',color='#a43244')
axs[0].set_xlim(0,10);axs[0].set_ylabel('归一化阶跃响应');axs[0].legend(fontsize=9)
axs[1].semilogy(t*1e6,np.maximum(np.exp(-u*t),1e-12),color='#16666e')
axs[1].semilogy(t*1e6,abs(err),color='#a43244')
axs[1].axhline(.001,ls='--',color='#bd6c28',label='0.1% 误差限')
axs[1].set_ylim(1e-6,1);axs[1].set_xlabel('时间（μs）');axs[1].set_ylabel('建立误差绝对值');axs[1].legend()
for ax in axs:style(ax)
fig.suptitle('微小的慢模态留数可能主导高精度建立过程')
fig.savefig(assets/'settling-comparison.svg');fig.savefig('tmp/ch02/settling-comparison.png',dpi=140);plt.close(fig)
settle=float(t[np.where(abs(err)>.001)[0][-1]+1])
nums={'exercise_029':{'gm_S':2*np.pi*100e6*3e-12,'Id_A':2*np.pi*100e6*3e-12*.2/2,
                       'W_over_L':2*np.pi*100e6*3e-12*.2/2/(50e-6*.2**2),
                       'chosen_L_um':2,'FOM_MHz_pF_per_mA':100*3/(2*np.pi*100e6*3e-12*.2/2*1000)},
      'follower_illustration':{'Rs_ohm':rs,'Cgs_F':cg,'Cgd_F':cd,'C0_F':c0,'g_cancel_S':gcancel,
                              'g_slide_0243_estimate_S':gbook,'g_complex_center_S':gcenter,
                              'g_complex_lower_S':glo,'g_complex_upper_S':ghi},
      'miller_illustration':{'gm_S':mg,'ro_ohm':ro,'Rs_ohm':1e4,'Cf_F':cf},
      'doublet_illustration':{'GBW_Hz':1e6,'open_pole_Hz':12e3,'open_zero_Hz':2e3,
                              'slow_residue':float(asn),'fast_residue':float(afn),
                              'lambda_s_rad_s':float(lsn),'lambda_f_rad_s':float(lfn),
                              'settling_0_1pct_s':settle,'no_doublet_settling_0_1pct_s':math.log(1000)/u}}
report={'status':'passed' if all(x['passed'] for x in checks+numeric) else 'failed',
        'scope':'Algebra and numerical nodal-model verification only; no SPICE or PDK validation.',
        'symbolic_checks':checks,'numerical_nodal_checks':numeric,'illustration_parameters':nums,
        'source_discrepancies':'See discrepancies.json; checks do not certify discrepant textbook formulas.'}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'status':report['status'],'symbolic_checks':len(checks),'numerical_nodal_checks':numeric,
                  'illustration_parameters':nums},ensure_ascii=False,indent=2),flush=True)
if report['status']!='passed':raise SystemExit(1)
