#!/usr/bin/env python3
"""Merge a batch translation file into source/translations_2.json."""
import json, sys, os

BASE = "/home/thelia/Documents/radioamateur-fr/source"
OUT = os.path.join(BASE, "translations_2.json")


def main(batch_path):
    batch = json.load(open(batch_path, encoding="utf-8"))
    if os.path.exists(OUT):
        cur = json.load(open(OUT, encoding="utf-8"))
    else:
        cur = {}
    added, replaced = 0, 0
    for k, v in batch.items():
        assert set(v.keys()) == {"stem", "answer", "com"}, (k, v.keys())
        if k in cur:
            replaced += 1
        else:
            added += 1
        cur[k] = v
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cur, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, OUT)
    print(f"batch={os.path.basename(batch_path)} size={len(batch)} added={added} replaced={replaced} total={len(cur)}")


if __name__ == "__main__":
    main(sys.argv[1])
