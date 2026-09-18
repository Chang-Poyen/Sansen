"""Build a provenance-first, offline extraction catalog. Heuristics are labeled."""
import argparse
import collections
import csv
import html
import json
import re
from pathlib import Path
from PIL import Image

TITLES = ["Comparison of MOST and bipolar transistors", "Amplifiers, source followers and cascodes",
"Differential voltage and current amplifiers", "Noise performance of elementary transistor stages",
"Stability of operational amplifiers", "Systematic design of operational amplifiers",
"Important opamp configurations", "Fully-differential amplifiers", "Design of multistage operational amplifiers",
"Current-input operational amplifiers", "Rail-to-rail input and output amplifiers", "Class AB and driver amplifiers",
"Feedback voltage and transconductance amplifiers", "Feedback transimpedance and current amplifiers",
"Offset and CMRR: random and systematic", "Bandgap and current reference circuits", "Switched-capacitor filters",
"Distortion in elementary transistor circuits", "Continuous-time filters", "CMOS ADC and DAC principles",
"Low-power sigma-delta AD converters", "Design of crystal oscillators", "Low-noise amplifiers",
"Coupling effects in mixed analog-digital ICs"]

TITLES_ORIGINAL = TITLES
TITLES = ['MOS 晶体管与双极型晶体管的比较', '放大器、源极跟随器与共源共栅级', '差分电压放大器与电流放大器', '基本晶体管级的噪声性能', '运算放大器的稳定性', '运算放大器的系统化设计', '常用运算放大器电路', '全差分放大器', '多级运算放大器设计', '电流输入型运算放大器', '轨到轨输入与输出放大器', 'AB 类放大器与驱动放大器', '反馈电压放大器与跨导放大器', '反馈跨阻放大器与电流放大器', '失调与共模抑制比：随机误差及系统误差', '带隙基准与电流基准电路', '开关电容滤波器', '基本晶体管电路的失真', '连续时间滤波器', 'CMOS 模数与数模转换原理', '低功耗 ΣΔ 模数转换器', '晶体振荡器设计', '低噪声放大器', '数模混合集成电路中的耦合效应']

# Manually located on the native slide images, top-left normalized xyxy.
VERIFIED_REGIONS = {
    "027": [("circuit", [.07,.18,.50,.59])],
    "028": [("bode_graph", [.05,.19,.67,.85])],
    "0210": [("circuit", [.075,.20,.53,.65])],
    "0211": [("circuit", [.08,.20,.53,.64])],
    "0212": [("circuit_original", [.08,.20,.515,.64]), ("circuit_input_equivalent", [.52,.20,.95,.64])],
    "0242": [("pole_and_gain_graphs", [.025,.15,.625,.94])],
    "0243": [("pole_and_impedance_graphs", [.025,.15,.625,.93])],
    "0244": [("pole_and_impedance_graphs", [.025,.15,.625,.94])],
    "0512": [("circuit", [.04,.20,.46,.60]), ("bode_graph", [.49,.175,.93,.69])],
    "0513": [("bode_graph", [.067,.175,.648,.902])],
    "0514": [("feedback_block_diagram", [.16,.195,.836,.515])],
}


def dump(p, o):
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def pick(c, pattern, limit=8):
    out = []
    for seg in c["commentary_segments"]:
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", seg["text"])
        for s in sentences:
            if re.search(pattern, s, re.I):
                out.append({"text": s, "pdf_page": seg["pdf_page"],
                            "printed_page": seg["printed_page"], "origin": "book_commentary_text_layer"})
    return out[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("output/extraction"))
    args = ap.parse_args()
    root = args.out
    cases = [json.loads(s) for s in (root / "cases.jsonl").read_text().splitlines()]
    manifest = json.loads((root / "manifest.json").read_text())
    reviews_path = Path(__file__).with_name("reviewed_cases.json")
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else {}
    deriv_root = root.parent / "derivations" / "ch02"
    deriv_map = json.loads((deriv_root / "case_map.json").read_text()) if (deriv_root / "case_map.json").exists() else {}
    deriv_modules = json.loads((deriv_root / "modules_data.json").read_text()) if (deriv_root / "modules_data.json").exists() else {}
    sim_path = root.parent / 'simulations' / 'ch02' / 'module_summary.json'
    sim_groups = json.loads(sim_path.read_text()) if sim_path.exists() else {}
    for c in cases:
        c["schema_version"] = "1.0"
        c["commentary_status"] = ("present" if c['commentary_text'] else
            "absent_in_source_verified_reference_slide" if c['slide_id'] in {'1170','1171','1249','1250','1251','2253','2254'} else "missing_requires_review")
        c["chapter_title"] = TITLES[c["chapter"] - 1]
        c["chapter_title_original"] = TITLES_ORIGINAL[c["chapter"] - 1]
        asset = c["slide_images"][0]
        op = root / "ocr" / (Path(asset["path"]).stem + ".json")
        ocr = json.loads(op.read_text()) if op.exists() else {"status": "missing", "lines": []}
        lines = ocr["lines"]
        title_lines = [x for x in lines if x["bbox"][1] < .19 and x["bbox"][0] < .8 and len(x["text"]) > 7]
        c["title"] = " ".join(x["text"] for x in sorted(title_lines, key=lambda x:x["bbox"][1])) or "Slide " + c["slide_id"]
        c["title_status"] = "ocr_unverified"
        c["ocr"] = {"path": str(op.relative_to(root)), "status": ocr["status"], "lines": lines,
                    "warning": "OCR confidence is not mathematical correctness. Subscripts, signs and fractions need visual verification."}
        combined = c["title"] + " " + c["commentary_text"]
        tags = []
        for tag, pattern in [("circuit",r"\b(circuit|amplifier|transistor|cascode|follower|current mirror|opamp|op-amp)\b"),
                             ("graph",r"\b(plot|curve|bode|diagram|characteristic|slope)\b"),
                             ("frequency_response",r"\b(bandwidth|pole|zero|frequency response|bode|GBW)\b"),
                             ("feedback",r"\b(feedback|loop gain|miller|bootstrapp)"),
                             ("noise",r"\bnoise\b"), ("distortion",r"\b(distortion|nonlinear)"),
                             ("reference",r"^References?\b|^Books?\b")]:
            if re.search(pattern, combined, re.I): tags.append(tag)
        c["content_tags"] = {"values": tags, "method": "keyword_candidates_not_visual_inventory"}
        c["analysis_objective_excerpts"] = pick(c, r"\b(show|explain|calculate|determine|derive|compare|find|illustrate|examine)\w*\b", 3)
        c["circuit"] = {"image": asset["path"], "topology_status": "not_netlist_verified",
                         "connection_description_excerpts": pick(c, r"\b(connect\w*|in parallel|in series|feedback path|gate|drain|source|base|collector|emitter)\b", 10),
                         "devices": None, "connections": None}
        c["source_conclusions"] = pick(c, r"\b(thus|therefore|as a result|equal\w*|proportional|depend\w*|independent|increase\w*|decrease\w*|limit\w*|conclusion|gain|bandwidth)\b", 8)
        c["graph_conclusion_excerpts"] = pick(c, r"\b(plot\w*|curve\w*|bode|slope|phase|axis|axes|peak\w*|roll.off|characteristic\w*)\b", 8)
        c["explicit_assumption_excerpts"] = pick(c, r"\b(assum\w*|approxim\w*|neglect\w*|ignor\w*|provided|only if|suppose|saturat\w*|much larger|much smaller)\b", 8)
        c["inferred_assumptions"] = []
        # Preserve raw math candidates and a surrounding crop. These crops are
        # evidence windows, not a claim to have segmented a complete equation.
        c["formula_candidates"] = []
        with Image.open(root / asset["path"]) as im:
            c["verified_visual_regions"] = []
            for kind, box in VERIFIED_REGIONS.get(c['slide_id'], []):
                rel = f"regions/{c['case_id']}_{kind}.png"
                im.crop(tuple(round(v * im.size[k%2]) for k,v in enumerate(box))).save(root / rel)
                c["verified_visual_regions"].append({"kind":kind,"path":rel,"bbox_normalized":box,
                    "source_image":asset['path'],"status":"region_manually_located_not_netlist_verified"})
            for line in lines:
                if not re.search(r"[=≈≃≤≥<>]|\b(?:GBW|BW|FOM)\s*[=:]", line["text"]):
                    continue
                b = line["bbox"]
                if b[1] > .91 or b[1] < .15:
                    continue
                i = len(c["formula_candidates"]) + 1
                box = [max(0,b[0]-.04), max(.13,b[1]-.10), min(1,b[2]+.23), min(.93,b[3]+.13)]
                rel = f"regions/{c['case_id']}_math_{i:02d}.png"
                im.crop(tuple(round(v * im.size[k%2]) for k,v in enumerate(box))).save(root / rel)
                c["formula_candidates"].append({"id": f"{c['case_id']}-M{i:02d}",
                    "ocr_text": line["text"], "confidence": line["confidence"], "bbox_normalized": b,
                    "context_crop": rel, "context_bbox_normalized": box, "source_image": asset["path"],
                    "status": "ocr_candidate_requires_visual_review", "latex": None})
        c["sfg_triage"] = {"priority": "candidate" if "feedback" in tags and "circuit" in tags else "unassessed",
                          "method": "keyword_triage_only", "reason": "需核对小信号模型与反馈结构后才能决定分析方法。"}
        c["simulation_status"] = "not_started_step_1_only"
        c["quality"] = {"source_pairing": "label_font_position_and_sequence_checked",
                        "math_text_layer_warning": "正文内的上下标、希腊字母及特殊符号可能错位；公式以原图为准。",
                        "extractive_fields": "以上 excerpt 字段是原文候选摘录，不是逐张人工判读的结论。"}
        if c["slide_id"] in reviews:
            c["reviewed_extraction"] = reviews[c["slide_id"]]
            c["semantic_review_status"] = "representative_case_visually_reviewed"
            c["title"] = reviews[c["slide_id"]]["title"]
            c["title_status"] = "visually_reviewed"
        if c['chapter'] == 2 and c['slide_id'] in deriv_map:
            c['derivation'] = deriv_map[c['slide_id']]
            c['simulation_status'] = 'not_started_theory_and_nodal_checks_only'
            sim = sim_groups.get(c['derivation']['module_id'])
            if sim:
                c['simulation_status'] = 'derivation_group_representative_models_verified'
                c['simulation'] = sim
            else:
                c.pop('simulation', None)
            c['sfg_triage'] = {'priority':c['derivation']['sfg'], 'method':'topology_and_explanatory_value_reviewed', 'reason':c['derivation']['sfg_reason']}
        else:
            c.pop('derivation', None)
        dump(root / "cases" / (c["case_id"] + ".json"), c)
        md = [f"# {c['case_id']} · {c['title']}", "",
              f"章节：{c['chapter']:02d} {c['chapter_title']}  ",
              f"PDF 页：{asset['pdf_page']}；书本页：{asset['printed_page']}；幻灯片编号：{c['slide_id']}  ",
              f"状态：{c['semantic_review_status']}", "", f"![原始幻灯片](../{asset['path']})", "",
              "## 对应教材讲解", ""]
        if c.get('derivation'):
            d=c['derivation']
            md[8:8] = ['## 第二章公式推导', '', d['summary_zh'], '',
                        f"[完整 Markdown 解释](../{d['markdown']}) · [排版公式网页](../{d['html']})", '',
                        f"状态：{d['status']}；SFG：{d['sfg']}。{d['sfg_reason']}", '',
                        '模型、近似与来源差异以新推导页为准；下方保留第一步的原始抽取。', '']
            if c.get('simulation'):
                md[8:8] = ['## Spectre 仿真', '', c['simulation']['scope_zh'], '',
                    f"[本组波形与仿真报告](../../simulations/ch02/index.html#{d['module_id']})", '']
        for seg in c["commentary_segments"]:
            md += [f"### PDF {seg['pdf_page']} · 书本 {seg['printed_page']}", "", seg["text"], ""]
        if not c['commentary_segments']:
            md += ["本页为参考文献幻灯片；已查看原 PDF，原页没有另外的正文讲解。", ""]
        if c.get("reviewed_extraction"):
            r = c["reviewed_extraction"]
            md += ["## 已核对的抽取", "", r["summary_zh"], ""]
            for f in r.get("formulas", []): md += [f"- `{f['latex']}` — {f['meaning_zh']}"]
            md += [""]
            for region in c['verified_visual_regions']:
                md += [f"![{region['kind']}](../{region['path']})", ""]
            for field, label in [("graph_conclusions_zh","曲线结论"),("conditions_zh","条件与近似注记"),("topology_zh","连接关系")]:
                md += [f"### {label}", ""] + ["- " + s for s in r.get(field, [])] + [""]
        for field, title in [("source_conclusions","公式／性能结论候选摘录"), ("graph_conclusion_excerpts","曲线结论候选摘录"),
                             ("explicit_assumption_excerpts","原文条件与近似候选摘录")]:
            md += ["## " + title, "", "以下为规则截取的原文，尚未逐项判读。", ""]
            md += [f"- PDF {e['pdf_page']}: {e['text']}" for e in c[field]] or ["（未由规则找到；不代表原页没有此类内容。）"]
            md += [""]
        md += ["## 幻灯片 OCR（未校正）", "", "```text", "\n".join(x["text"] for x in lines), "```", "",
               "数学上下标、分数及正负号以原图为准。电路图已保留；未核对的连接不输出成可仿真 netlist。", ""]
        (root / "cases" / (c["case_id"] + ".md")).write_text("\n".join(md), encoding="utf-8")
    with (root / "cases.jsonl").open("w") as f:
        for c in cases: f.write(json.dumps(c,ensure_ascii=False)+"\n")
    dump(root / "catalog.json", cases)
    with (root / "catalog.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id","chapter","slide_id","title","pdf_page","printed_page","tags","formula_candidates","sfg_triage","review_status"])
        for c in cases: writer.writerow([c['case_id'],c['chapter'],c['slide_id'],c['title'],c['slide_images'][0]['pdf_page'],c['slide_images'][0]['printed_page'],";".join(c['content_tags']['values']),len(c['formula_candidates']),c['sfg_triage']['priority'],c['semantic_review_status']])
    chapters=[]
    for ch in range(1,25):
        subset=[c for c in cases if c['chapter']==ch]
        summary={"chapter":ch,"title":TITLES[ch-1],"slides":len(subset),"pdf_page_start":subset[0]['source']['pdf_page'],"pdf_page_end":max(s['pdf_page'] for c in subset for s in c['commentary_segments']+c['slide_images'])}
        chapters.append(summary)
        md=[f"# Chapter {ch}: {TITLES[ch-1]}","",f"共 {len(subset)} 张幻灯片。", "", "| 编号 | 主题 | PDF 页 | 书本页 |", "|---|---|---:|---:|"]
        for c in subset:
            a=c['slide_images'][0]
            md.append(f"| {c['slide_id']} | [{c['title'].replace('|',' / ')}](../cases/{c['case_id']}.md) | {a['pdf_page']} | {a['printed_page']} |")
        (root/'chapters'/f'ch{ch:02d}.md').write_text('\n'.join(md))
    dump(root/'chapters.json',chapters)
    stats={"pdf_pages":manifest['pdf_pages'],"chapters":24,"slides":len(cases),"images":sum(len(c['slide_images']) for c in cases),
           "ocr_ok":sum(c['ocr']['status']=='ok' for c in cases), "formula_candidates":sum(len(c['formula_candidates']) for c in cases),
           "visually_reviewed_cases":sum(c['semantic_review_status']!='unreviewed' for c in cases),
           "manually_located_visual_regions":sum(len(c['verified_visual_regions']) for c in cases),
           "sfg_keyword_candidates":sum(c['sfg_triage']['priority']=='candidate' for c in cases),
           "commentary_cross_page_cases":sum(len({s['pdf_page'] for s in c['commentary_segments']})>1 for c in cases)}
    stats['chapter_2_derivation_mappings']=sum(bool(c.get('derivation')) for c in cases)
    stats['reference_slides_without_separate_commentary']=sum(not c['commentary_text'] for c in cases)
    dump(root/'statistics.json',stats)
    # Inline JSON makes the catalog work from file:// without a server or network.
    template=Path(__file__).with_name('catalog_template.html').read_text()
    payload=json.dumps(cases,ensure_ascii=False).replace('</','<\\/')
    (root/'index.html').write_text(template.replace('__CASES_JSON__',payload).replace('__STATS_JSON__',json.dumps(stats)).replace('__DERIVATIONS_JSON__',json.dumps(deriv_modules,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
