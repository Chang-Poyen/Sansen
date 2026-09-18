"""Integrity checks for the actual extraction artifacts; no network."""
import collections
import hashlib
import json
from pathlib import Path
from PIL import Image

root=Path('output/extraction')
cases=json.loads((root/'catalog.json').read_text())
manifest=json.loads((root/'manifest.json').read_text())
errors=[]
def check(condition,message):
    if not condition: errors.append(message)

check(len(cases)==manifest['slide_records']==1468,'slide count')
check(len(manifest['pages'])==759,'page count')
check(len({c['case_id'] for c in cases})==len(cases),'duplicate case IDs')
check({c['chapter'] for c in cases}==set(range(1,25)),'chapter coverage')
for chapter in range(1,25):
    nums=[c['slide_number_in_chapter'] for c in cases if c['chapter']==chapter]
    check(nums==list(range(1,max(nums)+1)),f'chapter {chapter}: missing/out-of-order slides')
images=[]
for c in cases:
    check(len(c['slide_images'])==1,c['case_id']+': expected one source image')
    check(bool(c['commentary_text']) or c['commentary_status']=='absent_in_source_verified_reference_slide',c['case_id']+': unexplained empty commentary')
    check(c['ocr']['status']=='ok' and bool(c['ocr']['lines']),c['case_id']+': OCR missing/empty')
    check(c['source']['printed_page'] is not None,c['case_id']+': printed page unknown')
    paths=[c['ocr']['path'],f"cases/{c['case_id']}.json",f"cases/{c['case_id']}.md"]
    for a in c['slide_images']:
        paths.append(a['path']);images.append(a['path'])
        with Image.open(root/a['path']) as im: check(list(im.size)==a['native_size_px'],c['case_id']+': image resolution')
        check(1<=a['pdf_page']<=759,c['case_id']+': source page invalid')
    paths += [f['context_crop'] for f in c['formula_candidates']]
    paths += [f['path'] for f in c['verified_visual_regions']]
    for p in paths: check((root/p).is_file(),c['case_id']+': missing '+p)
    for s in c['commentary_segments']:
        check(1<=s['pdf_page']<=759 and s['printed_page'] is not None,c['case_id']+': bad commentary provenance')
check(len(set(images))==len(images),'duplicate source image assignments')
actual_images={str(p.relative_to(root)) for p in (root/'slides').iterdir()}
check(actual_images==set(images),'unassigned/stale source images')
check(hashlib.sha256(Path(manifest['source_file']).read_bytes()).hexdigest()==manifest['source_sha256'],'source PDF hash changed')
page_nums=[p['printed_page'] for p in manifest['pages']]
missing=sorted(set(range(min(page_nums),max(page_nums)+1))-set(page_nums))
# Specific regression checks cover cross-page labels, continuation text, and
# chapter-opening folios. The original extraction's tricky layouts are exercised.
by_id={c['slide_id']:c for c in cases}
check(by_id['0111']['source']['pdf_page']==6 and by_id['0111']['slide_images'][0]['pdf_page']==7,'0111 cross-page label/image pairing')
check(by_id['021']['source']['printed_page']==51,'chapter-opening footer page')
check(by_id['027']['slide_images'][0]['pdf_page']==53,'027 source pointer')
check(by_id['2456']['slide_images'][0]['pdf_page']==759,'last slide pointer')
report={'status':'passed' if not errors else 'failed','checks_scope':'structural completeness and provenance; not correctness of all OCR or circuit topology',
        'errors':errors,'source_sha256':manifest['source_sha256'],'pdf_pages':759,'slide_records':len(cases),
        'chapters':24,'source_images':len(images),'ocr_records':sum(c['ocr']['status']=='ok' for c in cases),
        'manually_reviewed_cases': [c['slide_id'] for c in cases if c.get('reviewed_extraction')],
        'transcribed_reviewed_equations':sum(len(c.get('reviewed_extraction',{}).get('formulas',[])) for c in cases),
        'reference_slides_without_separate_commentary':[c['slide_id'] for c in cases if not c['commentary_text']],
        'printed_page_gaps_in_supplied_pdf':missing,
        'browser_preview':'not_performed: local file URL was blocked by browser policy; no workaround used'}
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
