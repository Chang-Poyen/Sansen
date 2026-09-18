"""Extract embedded slides and their flowing book commentary, with provenance.

Run with the bundled Python (pypdf, pdfplumber, Pillow). No network required.
Coordinates are PDF points, origin top-left; page numbers are one-based.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import pdfplumber
from pypdf import PdfReader


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def clean_text(text):
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    text = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", text)
    return re.sub(r"\s+", " ", text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, default=Path("output/extraction"))
    args = ap.parse_args()
    out = args.out
    for name in ["slides", "pages", "cases", "ocr", "chapters", "regions"]:
        (out / name).mkdir(parents=True, exist_ok=True)
    reader = PdfReader(args.pdf)
    cases, pages, issues = [], [], []
    active = None
    with pdfplumber.open(args.pdf) as pdf:
        for pi, p in enumerate(pdf.pages):
            page_no = pi + 1
            words = p.extract_words(x_tolerance=1, extra_attrs=["fontname"])
            # Labels use CGUniversBold; some start at the left margin before a
            # slide that continues onto the next page. Body numbers are excluded.
            markers = [w for w in words if "CGUniversBold" in w["fontname"]
                       and re.fullmatch(r"\d{3,5}", w["text"])
                       and w["top"] > 110]
            markers.sort(key=lambda w: w["top"])
            header = p.crop((0, 80, p.width, 112)).extract_text(x_tolerance=1) or ""
            nums = [w["text"] for w in words if w["top"] < 108 and w["text"].isdigit()]
            footers = [w for w in words if w["text"].isdigit() and 280 < w["x0"] < 305
                       and 701 < w["top"] < 715 and "CGUniversBold" not in w["fontname"]]
            if not nums and footers:
                nums = [footers[0]["text"]]
            printed = int(nums[0]) if nums else None
            body_bottom = min(w["top"] for w in footers) - 2 if footers else p.height - 45
            raw = p.extract_text(x_tolerance=1) or ""
            (out / "pages" / f"p{page_no:04d}.txt").write_text(raw, encoding="utf-8")
            page_info = {"pdf_page": page_no, "printed_page": printed, "header": header,
                         "size_pt": [p.width, p.height], "slide_ids": [],
                         "text_file": f"pages/p{page_no:04d}.txt"}
            # Each interval starts at a slide label and continues until the next one,
            # including top-of-page continuations of the preceding slide.
            intervals = [(112, markers[0]["top"] - 1 if markers else body_bottom, None)]
            for mi, m in enumerate(markers):
                intervals.append((m["top"] - 1,
                                  markers[mi + 1]["top"] - 1 if mi + 1 < len(markers) else body_bottom,
                                  m))
            for top, bottom, marker in intervals:
                if marker:
                    sid = marker["text"]
                    active = {"case_id": "SANSEN-" + sid, "slide_id": sid,
                              "chapter": int(sid[:2]), "slide_number_in_chapter": int(sid[2:]),
                              "source": {"pdf_page": page_no, "printed_page": printed},
                              "slide_images": [], "commentary_segments": [],
                              "extraction_status": "source_extracted",
                              "semantic_review_status": "unreviewed"}
                    cases.append(active)
                    page_info["slide_ids"].append(sid)
                if bottom <= top:
                    continue
                region = p.crop((0, top, p.width, bottom))
                # Remove the marker itself, not other numeric/equation text.
                if marker:
                    region = region.filter(lambda o: not (o.get("object_type") == "char"
                        and marker["x0"] - .5 <= o.get("x0", 0) <= marker["x1"] + .5
                        and abs(o.get("top", 0) - marker["top"]) < 1))
                txt = region.extract_text(x_tolerance=1) or ""
                if txt.strip() and active:
                    active["commentary_segments"].append({"pdf_page": page_no,
                        "printed_page": printed, "bbox_pt": [0, top, p.width, bottom],
                        "text_raw": txt, "text": clean_text(txt)})
            # Match the image against its nearest preceding slide label. Labels can
            # appear on the previous page when a slide flows onto the following page.
            native = {x.name.rsplit(".", 1)[0]: x for x in reader.pages[pi].images}
            for ii, im in enumerate(sorted(p.images, key=lambda x: x["top"])):
                matches = [c for c in cases if c["source"]["pdf_page"] < page_no or
                           any(m["text"] == c["slide_id"] and m["top"] <= im["top"] + 18 for m in markers)]
                owner = matches[-1] if matches else None
                stem = f"p{page_no:04d}_{ii+1:02d}" + ("_" + owner["slide_id"] if owner else "_unmatched")
                obj = native.get(im["name"])
                if obj:
                    suffix = Path(obj.name).suffix
                    rel = f"slides/{stem}{suffix}"
                    (out / rel).write_bytes(obj.data)
                else:
                    rel = f"slides/{stem}.png"
                    p.crop((im["x0"], im["top"], im["x1"], im["bottom"])).to_image(resolution=150).save(out / rel)
                    issues.append({"pdf_page": page_no, "issue": "image_render_fallback"})
                asset = {"path": rel, "pdf_page": page_no, "printed_page": printed,
                         "bbox_pt": [im["x0"], im["top"], im["x1"], im["bottom"]],
                         "native_size_px": list(im["srcsize"]), "extraction": "native_embedded_image" if obj else "rendered"}
                if owner:
                    owner["slide_images"].append(asset)
                else:
                    issues.append({"pdf_page": page_no, "issue": "unmatched_image", "asset": asset})
            pages.append(page_info)
            p.close()
            if page_no % 50 == 0:
                print(f"Extracted {page_no}/{len(pdf.pages)} pages, {len(cases)} slide records", flush=True)
    for c in cases:
        c["commentary_text"] = "\n\n".join(s["text"] for s in c["commentary_segments"])
        dump(out / "cases" / (c["case_id"] + ".json"), c)
    manifest = {"source_file": args.pdf.name, "source_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
                "pdf_pages": len(pages), "slide_records": len(cases),
                "slide_images": sum(len(c["slide_images"]) for c in cases),
                "coordinate_system": "PDF points; top-left origin; one-based page indices",
                "issues": issues, "pages": pages}
    dump(out / "manifest.json", manifest)
    with (out / "cases.jsonl").open("w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(json.dumps({k:v for k,v in manifest.items() if k != "pages"}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
