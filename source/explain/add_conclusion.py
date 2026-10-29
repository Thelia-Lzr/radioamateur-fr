# -*- coding: utf-8 -*-
"""给「结论不在开头」的条目补一句「选 X。」，让卡片一眼能看到答案。

判断规则：若正确答案的前 8 个字符没有出现在讲解正文的前 110 字里，
就在开头（「此题需看图」标记之后）补上结论。
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_1.json")
SLICE = os.path.join(HERE, "slice_1.json")
CJK = re.compile(r"[\u4e00-\u9fff]")


def main():
    out = json.load(open(OUT, encoding="utf-8"))
    data = {x["num"]: x for x in json.load(open(SLICE, encoding="utf-8"))}
    changed = []
    for k, v in out.items():
        ans = data[k]["ans_zh"].strip().replace("\u00a0", " ")
        core = ans[:8]
        if core and core in v[:110]:
            continue
        head = "选 %s。" % re.sub(r"\s*\n\s*", " ", ans)
        if v.startswith("此题需看图，"):
            new = "此题需看图，" + head + v[len("此题需看图，"):]
        elif v.startswith("此题需看图。"):
            new = "此题需看图。" + head + v[len("此题需看图。"):]
        else:
            new = head + v
        n = len(CJK.findall(new))
        if n > 250:
            print("跳过 %s（会超长 %d）" % (k, n))
            continue
        out[k] = new
        changed.append(k)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    chk = json.load(open(OUT, encoding="utf-8"))
    assert len(chk) == 227
    print("补结论 %d 条" % len(changed))
    print(" ".join(changed))
    L = [len(CJK.findall(x)) for x in chk.values()]
    print("中文字数 min/max:", min(L), max(L))


if __name__ == "__main__":
    main()
