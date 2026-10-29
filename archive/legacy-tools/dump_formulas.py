#!/usr/bin/env python3
"""Dump every candidate formula container, one per line, for review."""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "manuel-zh.html"
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9

with open(path, encoding="utf-8") as fh:
    text = fh.read()

# map char offset -> line number
starts = [0]
for m in re.finditer("\n", text):
    starts.append(m.end())


def lineno(off):
    lo_, hi_ = 0, len(starts) - 1
    while lo_ < hi_:
        mid = (lo_ + hi_ + 1) // 2
        if starts[mid] <= off:
            lo_ = mid
        else:
            hi_ = mid - 1
    return lo_ + 1


pat = re.compile(r'<(div|td|th|li|code|h3|p)\b[^>]*>(.*?)</\1>', re.S)
for m in pat.finditer(text):
    inner = m.group(2)
    if not re.search(r"[=√²³·×÷λπΩµμωτρφεθ]", inner):
        continue
    if not re.search(r"[=√·×²³λπµμ]", inner):
        continue
    ln = lineno(m.start())
    if not (lo <= ln <= hi):
        continue
    tag = m.group(1)
    attr = m.group(0)[:m.group(0).find(">") + 1]
    body = re.sub(r"\s+", " ", inner).strip()
    if len(body) > 400:
        body = body[:400] + " …"
    print("%5d %-4s %s :: %s" % (ln, tag, attr, body))
