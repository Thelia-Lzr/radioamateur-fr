# -*- coding: utf-8 -*-
"""把无法在 cours.txt 中核实的「教材 §x.y」引用换成题库真实锚点 §<anchor>。

只做定向字符串替换，改完后校验条数、字数与定界符。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_1.json")
CJK = re.compile(r"[\u4e00-\u9fff]")

REPL = {
    "20104": [("教材 §3.5 还指出数字电压表内阻恒定且很高，不再用 Ω/V 表示。",
               "数字电压表的内阻恒定且极高（常在 100 MΩ 量级），因此不再用 Ω/V 表示（本题锚点 §T034b）。")],
    "20110": [("（教材 §3.5 提到数字表常在 100 MΩ 量级）",
               "（数字表内阻常在 100 MΩ 量级，本题锚点 §T035a）")],
    "20488": [("教材 §9.5 核对。", "（本题锚点 §T095a）")],
    "20529": [("教材 §10.3b6。", "（本题锚点 §T103b6）")],
    "20532": [("教材 §11.5e 明确写着：", "关键是：")],
    "20553": [("教材 §11.5c 指出鉴频器", "鉴频器")],
    "20564": [("教材 §9.6e 明确：", "")],
    "20565": [("教材 §10.2b：理想情况下", "理想情况下")],
}


def main():
    out = json.load(open(OUT, encoding="utf-8"))
    n_before = len(out)
    for k, pairs in REPL.items():
        v = out[k]
        for old, new in pairs:
            if old not in v:
                print("!! %s 未找到: %r" % (k, old))
                sys.exit(1)
            v = v.replace(old, new)
        n = len(CJK.findall(v))
        if not (80 <= n <= 250):
            print("!! %s 字数越界 %d" % (k, n))
            sys.exit(1)
        if "$" in v or "\n" in v:
            print("!! %s 非法字符" % k)
            sys.exit(1)
        out[k] = v
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    chk = json.load(open(OUT, encoding="utf-8"))
    assert len(chk) == n_before == 227
    print("已替换 %d 条的引用，out_1.json 仍为 %d 条" % (len(REPL), len(chk)))


if __name__ == "__main__":
    main()
