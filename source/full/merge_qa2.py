#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge out_part2_*.json into out_2.json and run QA checks (batch 2)."""
import json, glob, re, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "slice_2.json")
OUT = os.path.join(BASE, "out_2.json")

items = json.load(open(SRC))
by_num = {x["num"]: x for x in items}
want = [x["num"] for x in items]

merged = {}
dup = []
for p in sorted(glob.glob(os.path.join(BASE, "out_part2_*.json"))):
    part = json.load(open(p))
    for k, v in part.items():
        if k in merged:
            dup.append((os.path.basename(p), k))
        merged[k] = v

missing = [n for n in want if n not in merged]
extra = [k for k in merged if k not in by_num]

print("source items :", len(want))
print("merged keys  :", len(merged))
print("missing      :", len(missing), missing[:20])
print("extra        :", len(extra), extra[:20])
print("duplicates   :", dup[:20])

problems = []
for n in want:
    e = merged.get(n)
    if not e:
        continue
    for f in ("stem_zh", "ans_zh", "com_zh", "explain"):
        if f not in e:
            problems.append((n, "missing field " + f))
    if "$" in json.dumps(e, ensure_ascii=False):
        problems.append((n, "contains $"))
    ex = e.get("explain", "")
    han = len(re.findall(r"[\u4e00-\u9fff]", ex))
    if han < 80:
        problems.append((n, "explain too short (%d han)" % han))
    if han > 260:
        problems.append((n, "explain too long (%d han)" % han))
    src = by_num[n]
    if src["commentaire_fr"].strip() and not e.get("com_zh", "").strip():
        problems.append((n, "com_zh empty but source comment not"))
    if not src["commentaire_fr"].strip() and e.get("com_zh", "").strip():
        problems.append((n, "com_zh not empty but source comment empty"))
    # numeric consistency: every decimal number in the FR stem should survive
    for tok in re.findall(r"\d+(?:[.,]\d+)?", src["stem_fr"]):
        t = tok.replace(",", ".")
        if t not in e["stem_zh"].replace(",", "."):
            problems.append((n, "stem number %r lost -> %s" % (tok, e["stem_zh"][:60])))
    if "此题需看图" in ex:
        pass

print("problems     :", len(problems))
for p in problems[:80]:
    print("   ", p)

flagged = [n for n in want if merged.get(n) and "待核" in json.dumps(merged[n], ensure_ascii=False)]
print("flagged 待核 :", len(flagged), flagged)

if missing or extra:
    sys.exit(2)

json.dump(merged, open(OUT, "w"), ensure_ascii=False, indent=1)
chk = json.load(open(OUT))
print("WROTE", OUT, "keys:", len(chk), "== 195 ?", len(chk) == 195)
