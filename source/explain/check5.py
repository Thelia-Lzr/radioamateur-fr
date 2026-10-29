# -*- coding: utf-8 -*-
"""校验并合并 b5_*.py 的讲解放进 out_5.json（slice_5.json，227 条）。

用法:
    python3 check5.py            # 只校验已存在的分块
    python3 check5.py --write    # 校验后合并写入 out_5.json
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CJK = re.compile(r"[\u4e00-\u9fff]")
PARTS = ["b5_1.py", "b5_2.py", "b5_3.py", "b5_4.py", "b5_5.py"]
# 各分块对应 slice_5.json 索引区间 [start, end)
RANGES = [(0, 46), (46, 91), (91, 136), (136, 181), (181, 227)]


def load_part(path):
    ns = {}
    with open(path, encoding="utf-8") as f:
        exec(compile(f.read(), path, "exec"), ns)
    return ns["DATA"]


def check(d):
    problems = []
    if not isinstance(d, dict):
        return ["DATA 不是 dict"]
    for k, v in d.items():
        if not isinstance(v, str):
            problems.append("%s 不是字符串" % k)
            continue
        if "$" in v:
            problems.append("%s 用了 $ 定界符" % k)
        if "\n" in v or "\r" in v:
            problems.append("%s 含换行" % k)
        if v.count("\\(") != v.count("\\)"):
            problems.append("%s 行内公式定界符不配对" % k)
        if v.count("\\[") != v.count("\\]"):
            problems.append("%s 独立公式定界符不配对" % k)
        if "\ufffd" in v:
            problems.append("%s 含替换字符" % k)
        if '"' in v:
            problems.append("%s 含 ASCII 双引号" % k)
        n = len(CJK.findall(v))
        if n < 80:
            problems.append("%s 偏短 (%d 中文字)" % (k, n))
        if n > 260 or len(v) > 620:
            problems.append("%s 偏长 (%d 中文字, %d 字符)" % (k, n, len(v)))
    return problems


def main():
    data = json.load(open(os.path.join(HERE, "slice_5.json"), encoding="utf-8"))
    nums = [x["num"] for x in data]
    index = {n: i for i, n in enumerate(nums)}
    merged, dup, all_problems = {}, [], []
    for name, (a, b) in zip(PARTS, RANGES):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            print("%-10s 缺失" % name)
            continue
        d = load_part(path)
        expected = nums[a:b]
        miss = [n for n in expected if n not in d]
        extra = [n for n in d if n not in expected]
        if miss:
            all_problems.append("%s 缺 %d: %s" % (name, len(miss), miss[:8]))
        if extra:
            all_problems.append("%s 多 %d: %s" % (name, len(extra), extra[:8]))
        all_problems += ["%s: %s" % (name, p) for p in check(d)]
        for k, v in d.items():
            if k in merged:
                dup.append(k)
            merged[k] = v
        print("%-10s %3d 条 (预期 %d)" % (name, len(d), len(expected)))
    missing_all = [n for n in nums if n not in merged]
    print("---- 合计 %d / 227，缺失 %d，重复 %d" % (len(merged), len(missing_all), len(dup)))
    if missing_all:
        print("缺失:", missing_all[:20])
    if dup:
        print("重复:", dup)
    if all_problems:
        print("---- 问题 %d 项" % len(all_problems))
        for p in all_problems:
            print(" *", p)
    else:
        print("---- 无格式问题")
    if "--write" in sys.argv:
        out = os.path.join(HERE, "out_5.json")
        old = {}
        if os.path.exists(out):
            try:
                old = json.load(open(out, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                old = {}
        old.update(merged)
        json.dump(old, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        chk = json.load(open(out, encoding="utf-8"))
        print("已写 out_5.json: %d 条，json.load OK" % len(chk))


if __name__ == "__main__":
    main()
