# -*- coding: utf-8 -*-
"""打印 slice_1.json 中索引区间 [start, end) 的题目，供撰写讲解时阅读。

用法: python3 dump_part.py 0 45
"""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    data = json.load(open(os.path.join(HERE, "slice_1.json"), encoding="utf-8"))
    for i, x in enumerate(data):
        if not (start <= i < end):
            continue
        print("#%d %s [%s] %s" % (i, x["num"], x["anchor"], x["theme_zh"]))
        print(" FR-Q:", x["stem_fr"])
        print(" Q:", x["stem_zh"])
        print(" O:", " // ".join(x["options"]))
        print(" A:", x["ans_zh"], "| ans_idx:", x["ans_idx"])
        if x["commentaire_fr"].strip():
            print(" C:", x["commentaire_fr"].replace("\n", " ")[:500])
        if x["com_zh"].strip():
            print(" C_zh:", x["com_zh"].replace("\n", " ")[:500])
        print()


if __name__ == "__main__":
    main()
