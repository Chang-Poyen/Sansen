"""Render physical constraints to auditable A–F Markdown and DOT; no transfer reduction."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'derivations/ch02'
MODELS=json.loads((SRC/'physical_sfg/models.json').read_text())
TEX={'vi':'v_i','vg':'v_g','vo':'v_o','vx':'v_x','va':'v_a','vF':'v_F','vR':'v_R','vR2':'v_{R2}','vgs':'v_{gs}','vgs2':'v_{gs2}',
     'im':'i_m','iF':'i_F','iR':'i_R','io':'i_o','it':'i_t','iG':'i_G','iD':'i_D','iB':'i_B','iL':'i_L','iDS':'i_{DS}',
     'im1':'i_{m1}','im2':'i_{m2}','io1':'i_{o1}','io2':'i_{o2}','imA':'i_{mA}','iCA':'i_{CA}','iRA':'i_{RA}',
     'va0':'v_{a0}','vRA':'v_{RA}','BA':'B_A','gm':'g_m','gm1':'g_{m1}','gm2':'g_{m2}','gmA':'g_{mA}','ro':'r_o','ro1':'r_{o1}','ro2':'r_{o2}','Rs':'R_S',
     'RA':'R_A','CF':'C_F','Cg':'C_{GS}','Cd':'C_{GD}','CL':'C_L','CDS':'C_{DS}','CA':'C_A','GB':'G_B','s':'s'}
def tex(x):return '-'+tex(x[1:]) if x.startswith('-') else ' '.join(TEX.get(t,t) for t in x.split('*'))
def equation(c):
 parts=[]
 for t in c['terms']:
  g=t['gain'];negative=g.startswith('-');mag=g.lstrip('-')
  term=('' if mag=='1' else tex(mag)+' ')+tex(t['source'])
  parts.append((' - ' if negative else ' + ')+term)
 return tex(c['target'])+' = '+''.join(parts).lstrip(' +')
def edge_rows(m):
 rows=[]
 for c in m['constraints']:
  for t in c['terms']:rows.append(dict(id=f'E{len(rows)+1:02d}',source=t['source'],target=c['target'],gain=t['gain'],constraint=c['id'],law=c['law']))
 return rows
for m in MODELS:
 nodes=m['nodes'];edges=edge_rows(m)
 (SRC/'physical_sfg'/f"{m['id']}-edges.json").write_text(json.dumps(edges,ensure_ascii=False,indent=2)+'\n')
 md=[f"# {m['title']}",'','## A. 选取的 SFG 节点及选择理由','',m['assumptions'],'',
     '所有量为工作点附近的小信号，电容采用零初始条件的拉普拉斯关系。按局部器件关系选择因果方向，不预先求整体传递函数，也不消元为最少节点图。',
     '', '| 节点 | 类型 | 选择理由 |','|---|---|---|']
 for n in nodes:md.append(f"| ${tex(n['id'])}$（`{n['id']}`） | {'电压 / V' if n['kind']=='voltage' else '电流 / A'} | {n['reason']} |")
 md+=['','## B. 独立约束','','每行是一个独立局部约束，整理为 $y=\\sum_k a_kx_k$。右侧的每一项生成一条边；一行分成多条边不等于重复使用约束。','','| 约束 | 物理来源 | 定向方程 |','|---|---|---|']
 for c in m['constraints']:md.append(f"| {c['id']} | {c['law']} | ${equation(c)}$ |")
 md+=['','电阻只使用 $v=Ri$ 这一方向，不再同时添加 $i=v/R$；同一电容的支路电流可以出现在两端节点的 KCL 中，但其本构关系只建一次。',
      '本图保留有限输出电阻以采用“电流 → 电压”的电阻方向。若另取输出电导严格为零的理想模型，应重新分配约束方向，不能直接在图上使用无穷大的电阻。',
      '', '## C. SFG edge list','','```text']
 for e in edges:md.append(f"{e['id']}: {e['source']} --({e['gain']})--> {e['target']}    [{e['constraint']}]")
 md+=['```','','## D. ASCII SFG','','以下按目标节点分组绘制，重复出现的变量名指同一个节点；所有连接均列出。V 为电压节点，A 为电流节点。','','```text']
 for c in m['constraints']:
  terms=c['terms'];target=c['target'];unit='V' if next(n for n in nodes if n['id']==target)['kind']=='voltage' else 'A'
  stems=[f"{t['source']} --({t['gain']})--" for t in terms];width=max(map(len,stems))
  for i,stem in enumerate(stems):
   md.append(stem.ljust(width,'-')+('> ' if len(stems)==1 else '+--> ' if i==len(stems)-1 else '+')+(f"{target} [{unit}]  ({c['id']})" if i==len(stems)-1 else ''))
   if i<len(stems)-1:md.append(' '*width+'|')
  md.append('')
 md+=['```','',f"![{m['title']}](../assets/{m['id']}-sfg.svg)",'',
      '图中椭圆为电压节点，圆角矩形为电流节点，双边框为独立输入。每条边显示系数和约束编号；按图中箭头读取方向。',
      '',f"[打开 SVG 矢量图](../assets/{m['id']}-sfg.svg) · [DOT 连接文本](../assets/{m['id']}-sfg.dot) · [机器可读边表]({m['id']}-edges.json)",'',
      '## E. 主要正向通路与反馈环路','']
 md+=['- '+p for p in m['paths']]
 md+=['','## F. 逐边对应独立约束检查','','| 边 | 起点 → 终点 | 系数 | 唯一来源约束 |','|---|---|---|---|']
 for e in edges:md.append(f"| {e['id']} | ${tex(e['source'])}\\to {tex(e['target'])}$ | ${tex(e['gain'])}$ | {e['constraint']}：{e['law']} |")
 md+=['',f"共 {len(nodes)} 个节点、{len(m['constraints'])} 个独立约束、{len(edges)} 条边。每个非输入节点只有一个定义方程；每条边属于唯一约束。边系数仅含单个器件的本构参数（包括理想受控源的常数增益）、电容导纳或带符号的 1。",'',
      '本节输出止于 Physical / Causal SFG，不进一步化为 algebraic SFG。','']
 (SRC/'physical_sfg'/f"{m['id']}.md").write_text('\n'.join(md))
 ranks={n['id']:n['rank'] for n in nodes}
 dot=['digraph '+m['id']+'_sfg {','rankdir=TB; bgcolor="white"; pad=0.35; nodesep=0.45; ranksep=0.7;',
      'node [fontname="Helvetica",fontsize=17,color="#22696b",penwidth=1.4];',
      'edge [fontname="Helvetica",fontsize=13,color="#416b68",fontcolor="#234b52",arrowsize=0.75];']
 for n in nodes:
  voltage=n['kind']=='voltage';style='filled' if voltage else 'rounded,filled'
  dot.append(f'{n["id"]} [label="{n["id"]}\\n[{"V" if voltage else "A"}]",shape={"ellipse" if voltage else "box"},style="{style}",fillcolor="{"#edf5f2" if voltage else "#fff1d9"}",peripheries={2 if n["id"] in m["inputs"] else 1}];')
 for rank in sorted(set(ranks.values())):dot.append('{rank=same; '+'; '.join(n for n,r in ranks.items() if r==rank)+';}')
 for e in edges:
  g=e['gain'];dot.append(f'{e["source"]} -> {e["target"]} [label="{g} [{e["constraint"]}]",constraint={str(ranks[e["source"]]<ranks[e["target"]]).lower()},color="{"#ac4752" if g.startswith("-") else "#416b68"}"];')
 dot.append('}')
 (SRC/'assets'/f"{m['id']}-sfg.dot").write_text('\n'.join(dot)+'\n')
print('Generated A–F Markdown, edge maps and DOT from three physical constraint models.')
