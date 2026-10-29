# -*- coding: utf-8 -*-
"""合并 part_*.json 到 out_1.json，并做完整性/格式校验。

用法:
    python3 check_merge.py            # 只校验，报告问题
    python3 check_merge.py --write    # 校验通过的部分合并写入 out_1.json
    python3 check_merge.py --final    # 要求 227 条齐全后才写入
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CJK = re.compile(r"[\u4e00-\u9fff]")

# 各分块文件负责的 slice_1.json 索引区间 [start, end)
RANGES = {
    "part_A.json": (0, 45),
    "part_B.json": (45, 91),
    "part_C.json": (91, 136),
    "part_D.json": (136, 181),
    "part_E.json": (181, 227),
}


def load_slice():
    return json.load(open(os.path.join(HERE, "slice_1.json"), encoding="utf-8"))


def check_part(path, expected_nums):
    problems = []
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return None, ["%s: json.load 失败: %s" % (os.path.basename(path), e)]
    missing = [n for n in expected_nums if n not in data]
    extra = [n for n in data if n not in expected_nums]
    if missing:
        problems.append("缺 %d 条: %s" % (len(missing), missing[:10]))
    if extra:
        problems.append("多 %d 条: %s" % (len(extra), extra[:10]))
    for k, v in data.items():
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
        n_cjk = len(CJK.findall(v))
        if n_cjk < 80:
            problems.append("%s 偏短 (%d 个中文字)" % (k, n_cjk))
        if n_cjk > 260 or len(v) > 560:
            problems.append("%s 偏长 (%d 个中文字, 共 %d 字符)" % (k, n_cjk, len(v)))
    return data, problems


def main():
    data = load_slice()
    all_nums = [x["num"] for x in data]
    index = {x["num"]: i for i, x in enumerate(data)}
    parts = sorted(glob.glob(os.path.join(HERE, "part_*.json")))
    merged = {}
    dup = []
    all_problems = []
    for p in parts:
        name = os.path.basename(p)
        rng = RANGES.get(name)
        expected = all_nums[rng[0]:rng[1]] if rng else all_nums
        d, problems = check_part(p, expected)
        if d is None:
            all_problems += problems
            continue
        for k, v in d.items():
            if k not in index:
                problems.append("键 %s 不在题库中" % k)
            if k in merged:
                dup.append(k)
            merged[k] = v
        all_problems += ["%s: %s" % (name, pr) for pr in problems]
        print("%-14s %3d 条 (预期 %d)" % (name, len(d), len(expected)))
    print("---- 合计 %d 条，重复键 %d 个" % (len(merged), len(dup)))
    if dup:
        print("重复:", dup)
    missing_all = [n for n in all_nums if n not in merged]
    print("相对 slice_1.json 缺失 %d 条: %s" % (len(missing_all), missing_all))
    if all_problems:
        print("---- 问题 %d 项:" % len(all_problems))
        for pr in all_problems:
            print(" *", pr)
    else:
        print("---- 无格式问题")

    if "--write" in sys.argv or ("--final" in sys.argv and not missing_all):
        out = os.path.join(HERE, "out_1.json")
        if os.path.exists(out):
            try:
                old = json.load(open(out, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                old = {}
            old.update(merged)
            merged = old
        ordered = {n: merged[n] for n in all_nums if n in merged}
        json.dump(ordered, open(out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        chk = json.load(open(out, encoding="utf-8"))
        assert len(chk) == len(ordered)
        print("已写 out_1.json: %d 条" % len(chk))


if __name__ == "__main__":
    main()
