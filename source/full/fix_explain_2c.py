# -*- coding: utf-8 -*-
"""Third pass: append one extra sentence (memory hook / reasoning) where CJK < 80."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out_part_2.json")

EXTRA = {
    "10045": "记忆：6 米段是 VHF 入门频率，法国只给 50 至 52 MHz，宽度自然就是 2 MHz。",
    "10046": "口诀：波段名看波长，宽度看差值。",
    "10047": "凡是问宽度，就在两端之间做减法，不要照抄整个区间。",
    "10048": "12 米只分到很窄的一段频率，做减法时尤其要看清位数。",
    "10049": "做这类题先分清问的是界限还是宽度，再看单位是 kHz 还是 MHz，两步走就不容易错。",
    "10050": "注意把波段名和宽度分开，名字里的数字不是答案。",
    "10051": "口诀：问宽度就上端减下端，问界限才抄两端。",
    "10052": "6 米这一段的边界与波长数字毫无关系，别把两者混用。",
    "10053": "WARC 波段都是窄带，宽度既小又互相像，务必逐个核对。",
    "10054": "20 米是最经典的远距离波段，宽度 350 kHz，与 15 米的 450 kHz 只差 100 kHz，只靠数字硬记很容易混。",
    "10055": "看清题目要的是界限还是宽度，再看是哪个区域。",
    "10056": "kHz 与 MHz 相差一千倍，窄波段尤其容易抄错单位。",
    "10057": "口诀：问宽度就做减法，问界限才抄两端，这条在 HF 段处处适用。",
    "10058": "别把界限当宽度，两个数一减才是答案。",
    "10059": "80 米是夜间主力波段，口诀「80 米配 3.5 兆，宽度三百千赫」。",
    "10060": "160 米是最窄的 HF 业余波段，只有 40 kHz，靠这个特点可以记牢。",
    "20010": "已知电压与电阻时，用电压平方除以电阻最直接，先平方再相除，别把顺序弄反。",
    "20011": "已知电压与电流时功率就是二者之积，量纲正好是瓦特，不必再绕道电阻。",
    "20013": "把 kΩ 与 mA 先换算成 Ω 和 A 再计算，是本题最关键的一步。",
    "20014": "求电池端电压就是求这条回路上电阻两端的电压，回路只有一只电阻时二者相同。",
    "20015": "记住量级：千欧级电阻配上零点几安，结果落在百伏附近。",
    "20016": "已知电压与电流就直接相乘，不必再绕道电阻。",
    "20019": "安时是电量的另一种单位，1 安时等于 3600 库仑，两套单位可以互相验算。",
    "20023": "串联只会越加越大，先看量级、再动笔算。",
    "20026": "分压题的检验办法：各部分电压之和应当等于总电压，用它一眼就能剔掉比总电压还大的选项。",
    "20027": "先由总电压减去已知分压，得到另一只上的电压，再用串联电流相同的条件求阻值，两步就够。",
    "20029": "记忆：并联结果一定小于其中最小的一只，据此可先排除偏大的选项。",
    "20031": "先算并联组、再与串联部分相加，顺序不能颠倒。",
}

d = json.load(open(OUT, encoding="utf-8"))


def cjk(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


for n, extra in EXTRA.items():
    assert n in d, n
    old = d[n]["explain"].rstrip()
    assert extra not in old, n
    d[n]["explain"] = old + extra

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

d2 = json.load(open(OUT, encoding="utf-8"))
src = [e["num"] for e in json.load(open(os.path.join(BASE, "in_2.json"), encoding="utf-8"))]
assert len(d2) == 39 and sorted(d2) == sorted(src), "key mismatch"
bad = [(n, cjk(v["explain"]), len(v["explain"]))
       for n, v in sorted(d2.items()) if not (80 <= cjk(v["explain"]) <= 160) or len(v["explain"]) > 340]
print("violations:", bad)
cs = [cjk(v["explain"]) for v in d2.values()]
ls = [len(v["explain"]) for v in d2.values()]
print("keys:", len(d2))
print("cjk min/max:", min(cs), max(cs))
print("total-length max:", max(ls), "| min:", min(ls))
for n in sorted(d2):
    print(n, "cjk=", cjk(d2[n]["explain"]), "len=", len(d2[n]["explain"]))
