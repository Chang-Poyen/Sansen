"""Prepare traceable module/slide metadata and readable Markdown exports."""
import json, shutil, re
from pathlib import Path
from ch02_metadata import GROUPS, CONTEXT, SFG, DIFFERENCES
src=Path('derivations/ch02'); out=Path('output/derivations/ch02'); out.mkdir(parents=True,exist_ok=True)
cases=[json.loads(x) for x in Path('output/extraction/cases.jsonl').read_text().splitlines()]
by={c['slide_id']:c for c in cases if c['chapter']==2}
def dump(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2))
modules=[]; mapping={}; diffs=[]
for did,sid,mid,kind,title,explain,status in DIFFERENCES:
 c=by[sid];a=c['slide_images'][0]
 diffs.append(dict(id=did,slide_id=sid,module_id=mid,kind=kind,title=title,explanation_zh=explain,status=status,
                   pdf_page=a['pdf_page'],printed_page=a['printed_page']))
for mid,title,sids,summary in GROUPS:
 sources=[]
 for sid in sids.split():
  assert sid not in mapping,sid
  c=by[sid];a=c['slide_images'][0];issues=[d['id'] for d in diffs if d['slide_id']==sid]
  sources.append(dict(slide_id=sid,pdf_page=a['pdf_page'],printed_page=a['printed_page'],
                      commentary_pdf_pages=sorted({x['pdf_page'] for x in c['commentary_segments']}),image='../../extraction/'+a['path']))
  mapping[sid]=dict(module_id=mid,title=title,summary_zh=summary,html='../derivations/ch02/'+mid+'.html',
    markdown='../derivations/ch02/'+mid+'.md',status='derived_with_source_notes' if issues else 'derived_in_stated_model',
    discrepancy_ids=issues,sfg='used' if mid in SFG else 'not_needed',
    sfg_reason=SFG.get(mid,'此组以微分、KCL 或矩阵即可说明机制，没有必要另画 SFG。'))
 modules.append(dict(id=mid,title=title,summary_zh=summary,slides=sids.split(),sources=sources,
                     sfg=mid in SFG,discrepancy_ids=[d['id'] for d in diffs if d['module_id']==mid]))
for sid,reason in CONTEXT.items():
 assert sid not in mapping
 mapping[sid]=dict(module_id='00-conventions',title='章节脉络与共同模型',summary_zh=reason,
                   html='../derivations/ch02/00-conventions.html',markdown='../derivations/ch02/00-conventions.md',
                   status='context_reviewed_no_independent_derivation',discrepancy_ids=[],sfg='not_applicable',sfg_reason='本页为章节脉络，无独立小信号模型需建图。')
assert set(mapping)==set(by) and len(mapping)==72
intro=dict(id='00-conventions',title='模型、符号与阅读方式',summary_zh='全章共同假设、精确式与近似式的区别，以及 SFG 选用原则。',slides=list(CONTEXT),sources=[],sfg=False,discrepancy_ids=[])
for sid in CONTEXT:
 a=by[sid]['slide_images'][0]
 intro['sources'].append(dict(slide_id=sid,pdf_page=a['pdf_page'],printed_page=a['printed_page'],commentary_pdf_pages=sorted({x['pdf_page'] for x in by[sid]['commentary_segments']}),image='../../extraction/'+a['path']))
allmods=[intro]+modules
coverage=[]
for sid,c in by.items():
 a=c['slide_images'][0]
 coverage.append(dict(slide_id=sid,pdf_page=a['pdf_page'],printed_page=a['printed_page'],**mapping[sid]))
dump(out/'modules.json',allmods);dump(out/'case_map.json',mapping);dump(out/'coverage.json',coverage);dump(out/'discrepancies.json',diffs)
shutil.copytree(src/'assets',out/'assets',dirs_exist_ok=True)
shutil.copytree(src/'physical_sfg',out/'physical_sfg',dirs_exist_ok=True)
def include_physical(match):
 name=match.group(1)
 body=(src/'physical_sfg'/f'{name}.md').read_text().split('\n',1)[1]
 body=body.replace('](../assets/','](assets/').replace(f']({name}-edges.json)',f'](physical_sfg/{name}-edges.json)')
 return f'[独立 Physical / Causal SFG Markdown](physical_sfg/{name}.md)\n\n'+body
full=[]
for m in allmods:
 body=(src/(m['id']+'.md')).read_text()
 body=re.sub(r'<!-- physical-sfg:([a-z]+) -->',include_physical,body)
 provenance='\n\n## 来源对照\n\n| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |\n|---|---:|---:|---|\n'
 for a in m['sources']:
  provenance+=f"| [{a['slide_id']}](../../extraction/index.html#SANSEN-{a['slide_id']}) | {a['pdf_page']} | {a['printed_page']} | {', '.join(map(str,a['commentary_pdf_pages']))} |\n"
 body+=provenance
 (out/(m['id']+'.md')).write_text(body)
 full.append(body)
(out/'full.md').write_text('\n\n---\n\n'.join(full))
md='# 第二章：教材公式差异与待厘清项目\n\n这份表区分模型、符号与近似的限制，并非将所有差异都判成教材错误。对应推导保留完整方程；待厘清式不算已证明。\n\n'
for d in diffs:
 md+=f"## {d['id']} · {d['slide_id']} · {d['title']}\n\n**{d['kind']}** · PDF {d['pdf_page']}／书本 {d['printed_page']}\n\n{d['explanation_zh']}\n\n[查看完整推导]({d['module_id']}.html) · [Markdown]({d['module_id']}.md)\n\n"
(out/'discrepancies.md').write_text(md)
print(f'Prepared {len(modules)} modules, {len(coverage)} slide mappings and {len(diffs)} source notes.')
