#!/usr/bin/env python3
"""Merge out_part_*.json into out_1.json and run QA checks."""
import json, glob, re, os, sys, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "slice_1.json")
OUT = os.path.join(BASE, "out_1.json")

items = json.load(open(SRC))
by_num = {x["num"]: x for x in items}
want = [x["num"] for x in items]

merged = {}
dup = []
if os.path.exists(OUT):
    merged = json.load(open(OUT))

for p in sorted(glob.glob(os.path.join(BASE, "out_part_*.json"))):
    part = json.load(open(p))
    for k, v in part.items():
        if k in merged:
            dup.append((p, k))
        merged[k] = v

missing = [n for n in want if n not in merged]
extra = [k for k in merged if k not in by_num]

print("source items :", len(want))
print("merged keys  :", len(merged))
print("missing      :", len(missing), missing[:20])
print("extra        :", len(extra), extra[:20])
print("duplicates   :", dup[:20])

FRENCH = re.compile(
    r"\b(le|la|les|un|une|des|du|de|est|sont|dans|pour|avec|sur|par|que|qui|"
    r"quelle|quelles|quel|est|sont|pas|plus|moins|entre|et|ou|au|aux|ce|cette|"
    r"nous|vous|il|elle|on|se|sa|son|ses|leur|leurs|mais|donc|car|si|"
    r"tension|puissance|courant|bande|frequence|fréquence)\b",
    re.I,
)


def strip_math(s):
    s = re.sub(r"\\\[.*?\\\]", " ", s, flags=re.S)
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)
    return s


problems = []
han_counts = []
for n in want:
    e = merged.get(n)
    if not e:
        continue
    for f in ("stem_zh", "ans_zh", "com_zh", "explain"):
        if f not in e:
            problems.append((n, "missing field " + f))
        elif not isinstance(e[f], str):
            problems.append((n, "field not str: " + f))
    if "$" in json.dumps(e, ensure_ascii=False):
        problems.append((n, "contains $"))
    ex = e.get("explain", "")
    han = len(re.findall(r"[\u4e00-\u9fff]", ex))
    han_counts.append(han)
    if han < 80:
        problems.append((n, "explain too short (%d han)" % han))
    if han > 160:
        problems.append((n, "explain long (%d han)" % han))
    if len(ex) > 340:
        problems.append((n, "explain string too long (%d chars)" % len(ex)))
    if ex.count("\\(") != ex.count("\\)"):
        problems.append((n, "unbalanced \\("))
    if ex.count("\\[") != ex.count("\\]"):
        problems.append((n, "unbalanced \\["))
    plain = strip_math(ex)
    if "^" in plain:
        problems.append((n, "'^' outside math mode"))
    if re.search(r"\d,\d", json.dumps(e, ensure_ascii=False)):
        problems.append((n, "french decimal comma"))
    src = by_num[n]
    if src["commentaire_fr"].strip() and not e.get("com_zh", "").strip():
        problems.append((n, "com_zh empty but source comment not"))
    if not src["commentaire_fr"].strip() and e.get("com_zh", "").strip():
        problems.append((n, "com_zh filled but source comment empty"))
    for f in ("stem_zh", "ans_zh", "com_zh"):
        if FRENCH.search(strip_math(e.get(f, ""))):
            problems.append((n, "french word in " + f))
    if not e.get("stem_zh", "").strip() or not e.get("ans_zh", "").strip():
        problems.append((n, "empty stem_zh/ans_zh"))

print("problems     :", len(problems))
for p in problems[:80]:
    print("   ", p)
print("han min/med/max:", min(han_counts), sorted(han_counts)[len(han_counts) // 2], max(han_counts))
print("waitai (⚠️待核) count:",
      sum(1 for n in want if "⚠️" in json.dumps(merged.get(n, {}), ensure_ascii=False)),
      [n for n in want if "⚠️" in json.dumps(merged.get(n, {}), ensure_ascii=False)])
print("need-figure (需看图) count:",
      sum(1 for n in want if "需看图" in merged.get(n, {}).get("explain", "")))

if missing:
    sys.exit(2)

json.dump(merged, open(OUT, "w"), ensure_ascii=False, indent=1)
chk = json.load(open(OUT))
print("WROTE", OUT, "keys:", len(chk), "== 195 ?", len(chk) == 195)
