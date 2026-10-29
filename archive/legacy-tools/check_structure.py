#!/usr/bin/env python3
"""Structure validator for manuel-zh.html during LaTeX conversion.

Usage:
    python3 check_structure.py <file> [--save-baseline]
Compares tag/anchor/math-delimiter counts against structure-baseline.json.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, "structure-baseline.json")

TAGS = ["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table", "thead",
        "tbody", "tr", "td", "th", "div", "span", "code", "em", "i", "b",
        "a", "main", "body", "html", "head", "small", "blockquote"]


def stats(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    out = {"chars": len(text), "bytes": len(text.encode("utf-8"))}
    for t in TAGS:
        out["open_" + t] = len(re.findall(r"<%s[\s>]" % t, text))
        out["close_" + t] = len(re.findall(r"</%s\s*>" % t, text))
    out["id_attrs"] = len(re.findall(r'\bid\s*=', text))
    out["ids_unique"] = len(set(re.findall(r'\bid="([^"]*)"', text)))
    # math delimiters
    out["inline_open"] = text.count("\\(")
    out["inline_close"] = text.count("\\)")
    out["display_open"] = text.count("\\[")
    out["display_close"] = text.count("\\]")
    out["dollar"] = text.count("$")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = args[0] if args else os.path.join(HERE, "manuel-zh.html")
    cur = stats(path)

    if "--save-baseline" in sys.argv:
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump(cur, fh, indent=1, sort_keys=True)
        print("baseline saved from", path)
        for k, v in sorted(cur.items()):
            print("  %-16s %s" % (k, v))
        return 0

    with open(BASELINE, encoding="utf-8") as fh:
        base = json.load(fh)

    bad = 0
    print("=== structural fields (must be identical to baseline) ===")
    for k in sorted(base):
        if k in ("chars", "bytes", "inline_open", "inline_close",
                 "display_open", "display_close", "dollar"):
            continue
        ok = base[k] == cur.get(k)
        if not ok:
            bad += 1
        print("  %-16s base=%-7s now=%-7s %s" % (k, base[k], cur.get(k),
                                                 "OK" if ok else "*** CHANGED ***"))

    print("=== variable fields ===")
    for k in ("chars", "bytes", "inline_open", "inline_close",
              "display_open", "display_close", "dollar"):
        print("  %-16s base=%-8s now=%-8s delta=%+d"
              % (k, base[k], cur[k], cur[k] - base[k]))

    print("=== well-formedness (open == close for every tag) ===")
    for t in TAGS:
        o, c = cur["open_" + t], cur["close_" + t]
        if o != c:
            bad += 1
            print("  %-12s open=%d close=%d  *** UNBALANCED ***" % (t, o, c))
    print("  all %d tracked tag kinds balanced" % len(TAGS))

    print("=== delimiter pairing ===")
    pairs = [("inline", cur["inline_open"], cur["inline_close"]),
             ("display", cur["display_open"], cur["display_close"])]
    for name, o, c in pairs:
        ok = o == c
        if not ok:
            bad += 1
        print("  %-8s open=%d close=%d %s" % (name, o, c, "OK" if ok else "*** UNBALANCED ***"))
    if cur["dollar"]:
        bad += 1
        print("  *** %d literal $ found - forbidden ***" % cur["dollar"])
    else:
        print("  no literal $            OK")

    print("RESULT:", "STRUCTURE OK" if bad == 0 else "%d PROBLEM(S)" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
