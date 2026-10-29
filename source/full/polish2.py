#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalise flags / stem wording in out_2.json after merging.

Policy applied here:
  * keep （⚠️待核） only when the SOURCE is defective or self-contradictory, or when
    the question is image-only and neither stem nor official comment carries any data;
  * purely graphical questions whose data IS recoverable from the official comment
    are signalled by 「此题需看图」 inside explain instead of a flag;
  * editorial parentheses inside stem_zh (meta talk about "the figure is missing")
    are removed so the stems read like real questions.
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out_2.json")

# num -> replacement stem_zh (None = leave untouched)
STEM_FIX = {
    "20399": "一个线圈的阻抗是多少？",
    "20403": "图中标注的这一级叫什么？（⚠️待核）",
    "20405": "计算基极电流。",
    "20409": "分流电阻 S 的阻值是多少？",
    "20412": "该方框图表示哪一类接收机？",
    "20413": "该方框图表示哪一类设备？",
    "20436": "图中标注的这一级是什么？（⚠️待核）",
    "20450": "接收机方框图带有 CAG，但没有混频器，也没有振荡器，请找出缺失的那一级。",
    "20460": "等效电阻是多少？",
    "20464": "该电阻的阻值是多少？",
    "20466": "该电阻的阻值是多少？",
    "20467": "该电阻的阻值是多少？",
}

# remove the ⚠️ marker from these items (source is not defective)
UNFLAG = ["20399", "20405", "20409", "20412", "20413", "20450",
          "20460", "20464", "20466", "20467", "20647", "20693"]


def strip_marker(s):
    s = re.sub(r"[（(]\s*⚠️?\s*待核\s*[）)]", "", s)
    return re.sub(r"\s{2,}", " ", s).strip()


def main():
    d = json.load(open(OUT))
    for n, new in STEM_FIX.items():
        if n in d:
            d[n]["stem_zh"] = new
    for n in UNFLAG:
        if n in d:
            for f in ("stem_zh", "ans_zh"):
                if "待核" in d[n][f]:
                    d[n][f] = strip_marker(d[n][f])
    # consistency: com_zh empty iff source comment empty
    items = {x["num"]: x for x in json.load(open(os.path.join(BASE, "slice_2.json")))}
    prob = []
    for n, e in d.items():
        src = items.get(n)
        if src is None:
            prob.append((n, "unknown num")); continue
        if bool(src["commentaire_fr"].strip()) != bool(e["com_zh"].strip()):
            prob.append((n, "com_zh/comment mismatch"))
        if "$" in json.dumps(e, ensure_ascii=False):
            prob.append((n, "dollar sign"))
        han = len(re.findall(r"[\u4e00-\u9fff]", e["explain"]))
        if not (80 <= han <= 260):
            prob.append((n, "explain han=%d" % han))
        if "待核" in e["ans_zh"] and "待核" not in e["stem_zh"]:
            pass
        if re.search(r"\d,\d", e["stem_zh"]) and not re.search(r"\d{1,3},\d{3}\s*(k|M|G)?Hz", e["stem_zh"]):
            prob.append((n, "possible decimal comma left: " + e["stem_zh"][:50]))
    print("items:", len(d), "| problems:", len(prob))
    for p in prob:
        print("   ", p)
    flagged = sorted(n for n, e in d.items() if "待核" in json.dumps(e, ensure_ascii=False))
    print("flagged:", len(flagged), flagged)
    json.dump(d, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("rewrote", OUT, len(json.load(open(OUT))))


if __name__ == "__main__":
    main()
