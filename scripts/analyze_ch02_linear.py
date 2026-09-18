"""Compare downloaded Spectre PSF against independently stated closed forms."""
from pathlib import Path
import os,json,csv
ROOT=Path(__file__).resolve().parent.parent
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/ch02-sim/mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from project_runtime import raw_output_dir
from virtuoso_bridge.spectre.psf import read_psf_ascii,result_file,vector,frequency_hz
OUT=ROOT/'output/simulations/ch02';(OUT/'assets').mkdir(exist_ok=True);(OUT/'csv').mkdir(exist_ok=True)

def raw(name,file):
 r=json.loads((OUT/'runs'/name/'result.json').read_text());assert r['ok'],r['errors']
 return read_psf_ascii(result_file(raw_output_dir(OUT/'runs'/name,r['metadata']),file))
def expected(t,s):
 p=t['params'];m=t['model']
 if m=='cs':return -p['gm']/(p['go']+1/p['rl']+s*p['cl'])
 if m=='miller':return (s*p['cf']-p['gm'])/(p['go']+s*p['cf']*(1+p['rs']*p['go']+p['rs']*p['gm']))
 if m=='degeneration':
  gm,go,rs=p['gm'],p['go'],p['rs'];ge=gm/(1+(gm+go)*rs);ro=1/go+(1+gm/go)*rs;return np.full_like(s,-ge/(1/ro+1/p['rl']))
 if m=='degen_zin':return 1/(s*p['cg'])+s*p['ls']+p['gm']*p['ls']/p['cg']
 if m=='diode_z':return 1/(p['gm']+p['go']+s*p['c'])
 if m=='diode_load':return -p['gm']/(p['go']+p['gml']+p['gol']+s*p['c'])
 if m=='inverter':
  gm=p['gmn']+p['gmp'];go=p['gon']+p['gop'];ci,cf,cl,rs=p['ci'],p['cf'],p['cl'],p['rs'];a1=(cl+cf)/go+rs*(ci+cf)+gm/go*rs*cf;a2=rs/go*(ci*cl+ci*cf+cf*cl);return -(gm/go)*(1-s*cf/gm)/(1+s*a1+s*s*a2)
 if m=='follower_dc':return p['gm']/(p['gm']+p['gmb']+p['go']+p['gb']+s*p['cl'])
 if m=='follower':
  gm,g,rs,cg,cd,c0=p['gm'],p['go']+p['gb'],p['rs'],p['cg'],p['cd'],p['c0'];d=gm+g+s*(cg+c0+rs*gm*cd+rs*g*(cd+cg))+s*s*rs*(c0*cd+c0*cg+cd*cg);return (1+s*rs*(cd+cg) if p['impedance'] else gm+s*cg)/d
 if m=='bjt_follower':
  gm,go,gs,gp=p['gm'],p['go'],1/p['rs'],p['gm']/p['beta'];y=gp+s*p['cpi'];n=gs+y+s*p['cmu'];return n/(n*(gm+y+go+s*p['cce'])-y*(gm+y))
 if m=='active_inductor':return (1+s*p['rs']*p['cg'])/(p['gm']+s*p['cg'])
 if m=='common_gate':
  q=1+p['gm']/p['go'];return np.full_like(s,q*p['rb']*p['rl']/(p['rl']+1/p['go']+q*p['rb']))
 if m=='cascode':
  gm1,gm2,go1,go2,cl,cf,rs,cm=[p[k] for k in ['gm1','gm2','go1','go2','cl','cf','rs','cm']];q=gm2+go2
  gl=1/(1/go1+1/go2+gm2/(go1*go2)) if p['top'] else 1/p['rb2'] if p['fold'] else 0
  if p['fold']:go1+=1/p['rb1']
  dx=go1+q
  if cf:return q*(s*cf-gm1)/(go1*go2+s*(cl*dx+cf*go2*(1+rs*(go1+gm1)))+s*s*cf*cl*(1+rs*(dx+gm1)))
  return -gm1*q/(go1*go2+gl*dx+s*(cl*dx+cm*(go2+gl))+s*s*cm*cl)
 if m=='two_stage':
  gm1,gm2,go1,go2,ci,cc,cl=[p[k] for k in ['gm1','gm2','go1','go2','ci','cc','cl']];d=go1*go2+s*(go1*(cl+cc)+go2*(ci+cc)+gm2*cc)+s*s*(ci*cl+ci*cc+cc*cl);return gm1*(gm2-s*cc)/d
 if m=='gainboost':
  gm1,gm2,go1,go2,cl,b0,wb=[p[k] for k in ['gm1','gm2','go1','go2','cl','b0','wb']];b=b0/(1+s/wb);return -gm1*(go2+gm2*(1+b))/(go1*go2+s*cl*(go1+go2+gm2*(1+b)))
 if m.startswith('bjt_degen'):
  gm,go,re,rpi,rb=p['gm'],p['go'],p['re'],p['beta']/p['gm'],p['rb']+p['rbext'];al=rpi/(rpi+rb);D=1/re+go+(gm+1/rpi)*al;ge=al*(gm/re-go/rpi)/D;ro=D/(go*(1/re+al/rpi));return np.full_like(s,ro if m.endswith('zout') else -ge/(1/ro+1/p['rl']))
 raise ValueError(m)

def approximation(t,s):
 p=t['params'];m=t['model']
 if m=='miller':
  a=p['gm']/p['go'];return -a/(1+s*p['rs']*a*p['cf']),'米勒主极点近似'
 if m=='cs':return -p['gm']/p['go']/(1+s*p['cl']/p['go']),'忽略外部负载'
 if m=='degeneration':return np.full_like(s,-p['rl']/p['rs']),'深度负反馈；忽略有限输出电阻'
 if m=='active_inductor':return 1/p['gm']+s*p['rs']*p['cg']/p['gm'],'低频串联 R+L 近似'
 if m=='cascode' and not p['cf'] and not p['cm'] and not p['top'] and not p['fold']:
  a=p['gm1']*p['gm2']/(p['go1']*p['go2']);return -a/(1+s*p['cl']*p['gm2']/(p['go1']*p['go2'])),'高本征增益近似'
 return None,None

from project_runtime import plot_font_families
plt.rcParams.update({'font.family':plot_font_families(),'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'path'})
def plot(t,f,y,h):
 fig,axs=plt.subplots(2,1,figsize=(9,6),sharex=True,layout='constrained');phase=np.unwrap(np.angle(h))*180/np.pi;yp=np.unwrap(np.angle(y))*180/np.pi
 axs[0].semilogx(f,20*np.log10(abs(h)),color='#155f65',label='完整模型推导');axs[0].semilogx(f[::24],20*np.log10(abs(y[::24])),'.',color='#aa3e4b',label='Spectre 仿真采样点')
 axs[1].semilogx(f,phase,color='#155f65');axs[1].semilogx(f[::24],yp[::24],'.',color='#aa3e4b')
 ap,label=approximation(t,2j*np.pi*f)
 if ap is not None:axs[0].semilogx(f,20*np.log10(abs(ap)),'--',color='#b77825',label=label)
 axs[0].set_ylabel('阻抗幅度（dBΩ）' if t['units']=='ohm' else '幅度（dB）');axs[1].set_ylabel('相位（°）');axs[1].set_xlabel('频率（Hz）');axs[0].legend(fontsize=8)
 for ax in axs:ax.grid(True,which='both',alpha=.2)
 fig.suptitle(t['id']+' | Spectre 仿真与理论推导对比');fig.savefig(OUT/'assets'/f"{t['id']}.svg")
 if t['id'] in ['miller','follower_center','two_stage']:fig.savefig(ROOT/'tmp/ch02-sim'/f"{t['id']}.png",dpi=120)
 plt.close(fig)

if __name__=='__main__':
 tests=json.loads((ROOT/'simulations/ch02/linear_cases.json').read_text());d=raw('linear_suite','ac.ac');f=np.array(frequency_hz(d));s=2j*np.pi*f;results=[]
 for t in tests:
  y=np.array(vector(d,t['output']));h=expected(t,s);err=abs(y-h)/np.maximum(abs(h),1e-20);ap,label=approximation(t,s);r={**t,'passed':bool(np.max(err)<2e-5),'max_relative_complex_error':float(max(err)),'samples':len(f),'frequency_Hz':[float(f[0]),float(f[-1])],'low_frequency_value_real':float(y[0].real),'asset':f"assets/{t['id']}.svg",'csv':f"csv/{t['id']}.csv"}
  if ap is not None:
   # Keep approximation error separate from complete-model verification.
   mask=f<=1e6;r['approximation']={'name':label,'max_relative_error_up_to_1MHz':float(np.max(abs(y[mask]-ap[mask])/np.maximum(abs(y[mask]),1e-20)))}
  results.append(r);plot(t,f,y,h)
  with (OUT/r['csv']).open('w') as fh:
   w=csv.writer(fh);w.writerow(['frequency_Hz','spectre_real','spectre_imag','derived_real','derived_imag','relative_error']);w.writerows(zip(f,y.real,y.imag,h.real,h.imag,err))
 (OUT/'linear_results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'tests':len(results),'passed':sum(x['passed'] for x in results),'failures':[(x['id'],x['max_relative_complex_error']) for x in results if not x['passed']],'max_relative_error':max(x['max_relative_complex_error'] for x in results)},indent=2),flush=True)
 # Transient: account for the source's 1 ns linear rising edge by averaging the ideal step.
 tr=raw('doublet_transient','tran.tran.tran');tt=np.array(vector(tr,'time')).real;delay=1e-6;rise=1e-9;elapsed=tt-delay;u=2*np.pi*1e6;res=[];fig,axs=plt.subplots(2,1,figsize=(9,6.5),layout='constrained')
 for name,p,z in [('baseline',None,None),('tail',2*np.pi*12e3,2*np.pi*2e3),('overshoot',2*np.pi*2e3,2*np.pi*12e3)]:
  y=np.array(vector(tr,name)).real
  if p is None:rates=[u];weights=[1.]
  else:
   ls,lf=np.sort(-np.roots([1,p+u,u*z]));rates=[ls,lf];weights=[(p-ls)/(lf-ls),(lf-p)/(lf-ls)]
  ideal=np.zeros_like(tt);ramp=(elapsed>0)&(elapsed<rise);after=elapsed>=rise
  # convolution with a boxcar: y_ramp(t)=(1/tr)*integral_0^tr step(t-a) da
  ideal[ramp]=elapsed[ramp]/rise
  for rate,weight in zip(rates,weights):ideal[ramp]-=weight*(-np.expm1(-rate*elapsed[ramp]))/(rate*rise)
  ideal[after]=1
  for rate,weight in zip(rates,weights):ideal[after]-=weight*np.exp(-rate*(elapsed[after]-rise))*(-np.expm1(-rate*rise))/(rate*rise)
  err=float(np.max(abs(y-ideal)));valid=elapsed>=rise;bad=np.where(valid&(abs(1-y)>.001))[0];settle=float(tt[bad[-1]+1]-delay) if len(bad) and bad[-1]+1<len(tt) else None
  res.append({'id':name,'module':'19-doublet-settling','passed':err<2e-5,'max_absolute_error':err,'samples':len(tt),'settling_0_1pct_s':settle,'rates_rad_s':[float(x) for x in rates],'weights':[float(x) for x in weights]})
  axs[0].plot(elapsed*1e6,y,label={'baseline':'基准响应','tail':'慢尾响应','overshoot':'过冲'}[name]);axs[0].plot(elapsed[::60]*1e6,ideal[::60],'.',color='#233e3d',ms=2)
  axs[1].semilogy(elapsed[valid]*1e6,abs(1-y[valid]),label={'baseline':'基准响应','tail':'慢尾响应','overshoot':'过冲'}[name])
  with (OUT/'csv'/f'transient_{name}.csv').open('w') as fh:
   w=csv.writer(fh);w.writerow(['time_s','spectre','derived_finite_rise_step','absolute_error']);w.writerows(zip(tt,y,ideal,abs(y-ideal)))
 axs[0].plot([],[],'.',color='#233e3d',label='有限上升时间的理论响应',ms=4)
 axs[0].set_xlim(0,10);axs[0].set_ylabel('阶跃响应');axs[0].set_xlabel('阶跃开始后的时间（μs）');axs[1].set_xlim(0,600);axs[1].set_ylim(1e-7,1);axs[1].set_xlabel('阶跃开始后的时间（μs）');axs[1].set_ylabel('建立误差绝对值');axs[1].axhline(.001,color='#b77825',ls='--')
 for ax in axs:ax.grid(True,alpha=.2);ax.legend(fontsize=8)
 fig.suptitle('Spectre 瞬态分析：极零对引起的慢尾响应与过冲');fig.savefig(OUT/'assets/doublet_transient.svg');fig.savefig(ROOT/'tmp/ch02-sim/doublet_transient.png',dpi=120);plt.close(fig)
 (OUT/'transient_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
 if not all(x['passed'] for x in results+res):raise SystemExit(1)
