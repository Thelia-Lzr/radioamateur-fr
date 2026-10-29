# -*- coding: utf-8 -*-
"""合并 partN.py 到 out_3.json，并做 json.load 校验与字数统计。"""
import json, re, sys, importlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_3.json")


def main(parts):
    data = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    for p in parts:
        sys.path.insert(0, HERE)
        mod = importlib.import_module(p)
        importlib.reload(mod)
        for k, v in mod.D.items():
            assert set(v) == {"title_fr", "title_zh", "front", "body"}, (k, list(v))
            data[k] = v
    order = sorted(data, key=lambda x: x)
    data = {k: data[k] for k in order}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    # 校验
    with open(OUT, encoding="utf-8") as f:
        chk = json.load(f)
    print("json.load OK, 知识点数 =", len(chk))
    for k, v in chk.items():
        han = len(re.findall(r"[\u4e00-\u9fff]", v["body"]))
        tzh = len(re.findall(r"[\u4e00-\u9fff]", v["title_zh"]))
        flag = "OK " if 400 <= han <= 800 else "!! "
        print("%s%-5s body汉字=%4d  title_zh汉字=%2d  %s" % (flag, k, han, tzh, v["title_zh"]))


if __name__ == "__main__":
    main(sys.argv[1:])
