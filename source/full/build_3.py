#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 批构建脚本：把 c3_1..c3_5 的译文与 c3_extra* 的补充合并，
做法语小数点逗号 -> 点的转换，输出 out_3.json。"""
import json, importlib.util, re

HERE = "/home/thelia/Documents/radioamateur-fr/source/full"

def load(fname, attr="D"):
    spec = importlib.util.spec_from_file_location(fname[:-3], f"{HERE}/{fname}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, attr)

def main():
    src = json.load(open(f"{HERE}/slice_3.json"))
    data = {}
    for f in ["c3_1.py", "c3_2.py", "c3_3.py", "c3_4.py", "c3_5.py"]:
        data.update(load(f))
    extras = [load("c3_extra.py", "EXTRA"), load("c3_extra2.py", "EXTRA2"),
              load("c3_extra3.py", "EXTRA3")]
    # 法语小数逗号 -> 点（千位分隔点已原样保留）
    conv = lambda s: re.sub(r"(?<=\d),(?=\d)", ".", s)
    out = {}
    for x in src:
        n = x["num"]
        stem, ans, com, exp = data[n]
        exp += "".join(e.get(n, "") for e in extras)
        out[n] = {"stem_zh": conv(stem), "ans_zh": conv(ans),
                  "com_zh": conv(com), "explain": conv(exp)}
    json.dump(out, open(f"{HERE}/out_3.json", "w"), ensure_ascii=False, indent=1)
    return out

if __name__ == "__main__":
    o = main()
    zh = lambda s: len(re.findall(r"[\u4e00-\u9fff]", s))
    print("entries:", len(o))
    print("explain 中文字数 min/max:",
          min(zh(v["explain"]) for v in o.values()),
          max(zh(v["explain"]) for v in o.values()))
    print("含 ⚠️待核 的条数:", sum(1 for v in o.values() if "待核" in v["explain"]))
