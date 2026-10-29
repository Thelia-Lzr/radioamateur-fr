# -*- coding: utf-8 -*-
"""回退 add_conclusion.py 误加在已有结论条目上的重复「选 X。」"""
import json
import re

OUT = "out_1.json"
BAK = "/tmp/out_1.bak.json"
CJK = re.compile(r"[\u4e00-\u9fff]")

RESTORE = ["20088", "20374", "20383", "20386", "20411", "20416", "20421",
           "20444", "20477", "20509", "20560"]

TWEAK = {
    "20223": ("选 AM 调幅。", "选调幅（AM）。"),
    "20548": ("选 振荡器。", "选振荡器。"),
    "20204": ("选 音频放大器（AF）。", "选音频放大器（AF）。"),
    "20205": ("选 射频放大器（RF）。", "选射频放大器（RF）。"),
    "20207": ("选 中频放大器（FI）。", "选中频放大器（FI）。"),
    "20208": ("选 双变频接收机。", "选双变频接收机。"),
    "20215": ("选 射频放大器（RF）。", "选射频放大器（RF）。"),
    "20361": ("此题需看图。选 滤波器。", "此题需看图。选滤波器。"),
}

out = json.load(open(OUT, encoding="utf-8"))
bak = json.load(open(BAK, encoding="utf-8"))
for k in RESTORE:
    out[k] = bak[k]
out["20443"] = bak["20443"].replace("此题需看图，结论 CAG。", "此题需看图，选 CAG。")
for k, (a, b) in TWEAK.items():
    if a not in out[k]:
        raise SystemExit("!! %s 未找到 %r" % (k, a))
    out[k] = out[k].replace(a, b)
for k, v in out.items():
    assert "$" not in v and "\n" not in v, k
    n = len(CJK.findall(v))
    assert 80 <= n <= 250, (k, n)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
chk = json.load(open(OUT, encoding="utf-8"))
assert len(chk) == 227
print("回退 %d 条 + 措辞微调 %d 条，out_1.json 仍为 %d 条" % (len(RESTORE), len(TWEAK), len(chk)))
