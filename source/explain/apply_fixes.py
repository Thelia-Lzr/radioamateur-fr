# -*- coding: utf-8 -*-
"""把某个 FIX 字典（题号 -> 新讲解）应用到 out_1.json。

用法: python3 apply_fixes.py fixes_1.py
FIX 文件形如:  FIX = {"10022": r'''...'''}
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CJK = re.compile(r"[\u4e00-\u9fff]")
OUT = os.path.join(HERE, "out_1.json")


def load_fix(path):
    spec = importlib.util.spec_from_file_location("fx", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FIX


def main():
    fix_path = sys.argv[1]
    if not os.path.isabs(fix_path):
        fix_path = os.path.join(HERE, fix_path)
    fix = load_fix(fix_path)
    out = json.load(open(OUT, encoding="utf-8"))
    problems = []
    for k, v in fix.items():
        if k not in out:
            problems.append("%s 不在 out_1.json" % k)
            continue
        if "$" in v or "\n" in v or "\r" in v:
            problems.append("%s 含非法字符" % k)
        if v.count("\\(") != v.count("\\)") or v.count("\\[") != v.count("\\]"):
            problems.append("%s 公式定界符不配对" % k)
        n = len(CJK.findall(v))
        if n < 80 or n > 250:
            problems.append("%s 中文字数 %d 越界" % (k, n))
    if problems:
        print("拒绝应用:")
        for p in problems:
            print(" *", p)
        sys.exit(1)
    before = len(out)
    for k, v in fix.items():
        out[k] = v
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    chk = json.load(open(OUT, encoding="utf-8"))
    assert len(chk) == before, (len(chk), before)
    print("已应用 %d 条修补，out_1.json 仍为 %d 条" % (len(fix), len(chk)))


if __name__ == "__main__":
    main()
