"""Check primitive physical graphs against independently assembled nodal equations.
No overall transfer function is used to construct or check the graphs.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tmp/ch02/python-deps'))
import sympy as S
import numpy as np

def verify_models():
 spec=ROOT/'derivations/ch02/physical_sfg/models.json'
 models=json.loads(spec.read_text());reports=[];rng=np.random.default_rng(2642026)
 for m in models:
  nodes={n['id']:n for n in m['nodes']};cons=m['constraints'];inputs=m['inputs'];unknown=[n for n in nodes if n not in inputs]
  assert len(nodes)==len(m['nodes']) and len(cons)==len(unknown)
  assert set(c['target'] for c in cons)==set(unknown) and len({c['target'] for c in cons})==len(cons)
  assert len({c['law'] for c in cons})==len(cons) and len({c['id'] for c in cons})==len(cons)
  symbols={p:S.Symbol(p) for p in m['parameter_units']};symbols['s']=S.Symbol('s');v=symbols
  allowed={'1','-1'}|{p for p,u in m['parameter_units'].items() if u[2]==0}|{'s*'+p for p,u in m['parameter_units'].items() if u[2]==1}
  allowed|={'-'+p for p in allowed if not p.startswith('-')}
  A=S.eye(len(unknown));B=S.zeros(len(unknown),len(inputs));edges=[]
  for c in cons:
   row=unknown.index(c['target']);assert len({t['source'] for t in c['terms']})==len(c['terms'])
   for t in c['terms']:
    source=t['source'];gain=t['gain'];assert source in nodes and gain in allowed,(m['id'],c['id'],gain)
    g=S.sympify(gain,locals=symbols)
    unit=np.array([1,0,0] if nodes[source]['kind']=='voltage' else [0,1,0])
    if gain not in ['1','-1']:
     unit+=m['parameter_units'][gain.lstrip('-').split('*')[-1]]
     if gain.startswith('s*'):unit+=[0,0,-1]
    assert list(unit)==([1,0,0] if nodes[c['target']]['kind']=='voltage' else [0,1,0]),(c,t,'unit mismatch')
    if source in inputs:B[row,inputs.index(source)]+=g
    else:A[row,unknown.index(source)]-=g
    edges.append(dict(id=f'E{len(edges)+1:02d}',source=source,target=c['target'],gain=gain,constraint=c['id'],law=c['law']))
  assert edges==json.loads((spec.parent/f"{m['id']}-edges.json").read_text())
  s=v['s']
  if m['id']=='miller':
   gm,ro,Rs,CF=[v[x] for x in ['gm','ro','Rs','CF']];keep=['vg','vo']
   N=S.Matrix([[1/Rs+s*CF,-s*CF],[gm-s*CF,1/ro+s*CF]]);U=S.Matrix([[1/Rs],[0]]);T=S.diag(Rs,ro)
  elif m['id']=='follower':
   gm,ro,Rs,Cg,Cd,CL,CDS,GB=[v[x] for x in ['gm','ro','Rs','Cg','Cd','CL','CDS','GB']];keep=['vg','vo']
   N=S.Matrix([[1/Rs+s*(Cg+Cd),-s*Cg],[-gm-s*Cg,gm+1/ro+GB+s*(Cg+CL+CDS)]]);U=S.Matrix([[1/Rs,0],[0,1]]);T=S.diag(Rs,ro)
  else:
   gm1,gm2,BA,ro1,ro2,RA,CL,CA=[v[x] for x in ['gm1','gm2','BA','ro1','ro2','RA','CL','CA']];keep=['vx','va','vo']
   N=S.Matrix([[1/ro1+gm2+1/ro2,-gm2,-1/ro2],[BA/RA,1/RA+s*CA,0],[-gm2-1/ro2,gm2,1/ro2+s*CL]])
   U=S.Matrix([[-gm1],[0],[0]]);T=S.Matrix([[ro1,0,ro1],[0,RA,0],[0,0,ro2]])
  ki=[unknown.index(n) for n in keep];ii=[i for i,n in enumerate(unknown) if n not in keep]
  # Eliminate only branch auxiliaries for verification of KCL, never produce a reduced SFG.
  internal=A.extract(ii,ii).inv()
  reduced=A.extract(ki,ki)-A.extract(ki,ii)*internal*A.extract(ii,ki)
  rhs=B.extract(ki,range(len(inputs)))-A.extract(ki,ii)*internal*B.extract(ii,range(len(inputs)))
  residuals=list(reduced-T*N)+list(rhs-T*U)
  assert all(S.cancel(x)==0 for x in residuals),(m['id'],'physical/nodal symbolic mismatch')
  assert S.simplify(T.det())!=0
  ps=list(symbols);fn=[S.lambdify([symbols[p] for p in ps],x,'numpy') for x in [A,B,N,U]]
  max_error=0.;max_residual=0.;trials=0
  for j in range(30):
   values={p:(2j*np.pi*10**rng.uniform(2,9) if p=='s' else 10**rng.uniform(0,2) if p=='BA' else 10**rng.uniform(-13,-11) if units[2]==1 else 10**rng.uniform(3,5) if units[0]==1 else 10**rng.uniform(-5,-2)) for p,units in {**m['parameter_units'],'s':[0,0,-1]}.items()}
   av,bv,nv,uv=[np.asarray(f(*[values[p] for p in ps]),dtype=complex) for f in fn]
   for port in range(len(inputs)):
    inp=np.zeros(len(inputs),complex);inp[port]=1 if nodes[inputs[port]]['kind']=='voltage' else 1e-6
    graph=np.linalg.solve(av,bv@inp);nodal=np.linalg.solve(nv,uv@inp)
    err=np.max(abs(graph[ki]-nodal)/np.maximum(abs(nodal),1e-15));max_error=max(max_error,float(err))
    residual=abs(av@graph-bv@inp)/(abs(av)@abs(graph)+abs(bv@inp)+1e-30);max_residual=max(max_residual,float(max(residual)));trials+=1
  assert max_error<1e-8 and max_residual<1e-10,(m['id'],max_error,max_residual)
  reports.append(dict(id=m['id'],passed=True,nodes=len(nodes),voltage_nodes=sum(n['kind']=='voltage' for n in nodes.values()),current_nodes=sum(n['kind']=='current' for n in nodes.values()),independent_constraints=len(cons),edges=len(edges),unique_constraint_per_target=True,primitive_edge_units_checked=True,symbolic_nodal_equivalence=True,numerical_port_comparisons=trials,max_relative_voltage_error=max_error,max_normalized_equation_residual=max_residual))
 report=dict(status='passed',construction='Local physical constraints only; no overall transfer function or reduced algebraic SFG.',models=reports,spec_sha256=hashlib.sha256(spec.read_bytes()).hexdigest())
 out=ROOT/'output/derivations/ch02/physical_sfg_verification.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report
if __name__=='__main__':print(json.dumps(verify_models(),ensure_ascii=False,indent=2))
