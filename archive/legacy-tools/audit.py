#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-conversion audit: structure, delimiter balance and leftover Unicode maths.

    python3 audit.py [file] [--leftovers]
"""
import re
import sys

PATH = "/home/thelia/Documents/radioamateur-fr/manuel-zh.html"

# maths that must never survive outside \( \) or \[ \]
LEFTOVER = re.compile(
    u"[\u03bb\u03c0\u03c4\u221a\u00b7\u00d7\u00f7\u2264\u2265\u2260"
    u"\u21d2\u27f9\u221e\u221d\u03b5\u03a9\u03c1\u03c9\u03b7\u03b8\u03c6]"
    u"|[\u00b2\u00b3\u207b\u2079\u2076\u2070]"
    u"|(?:[A-Za-z]\\s?=\\s?[A-Za-z0-9]+\\s?[\u00b7\u00d7])"
)


def main():
    path = PATH
    for a in sys.argv[1:]:
        if not a.startswith("--"):
            path = a
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    print("file            :", path)
    print("chars           :", len(text))
    print("inline (\\)     :", text.count("\\("), text.count("\\)"))
    print("display [ ]     :", text.count("\\["), text.count("\\]"))
    print("literal $       :", text.count("$"))

    bad_fr = 0
    for m in re.finditer(r'<p class="fr">.*?</p>|<span class="fr">.*?</span>',
                         text, re.S):
        if "\\(" in m.group(0) or "\\[" in m.group(0):
            bad_fr += 1
            print("  !! math delimiter inside French text:", m.group(0)[:90])
    print("math in French  :", bad_fr, "OK" if bad_fr == 0 else "*** PROBLEM ***")

    bad_tag = [m.group(0) for m in re.finditer(r"</?[A-Za-z][^<>]*>", text)
               if "\\(" in m.group(0) or "\\[" in m.group(0)]
    print("math in tags    :", len(bad_tag), "OK" if not bad_tag else bad_tag[:3])

    stripped = re.sub(r"\\\(.*?\\\)", "", text, flags=re.S)
    stripped = re.sub(r"\\\[.*?\\\]", "", stripped, flags=re.S)
    stripped = re.sub(r'<p class="fr">.*?</p>', "", stripped, flags=re.S)
    stripped = re.sub(r'<span class="fr">.*?</span>', "", stripped, flags=re.S)
    lines = stripped.split("\n")
    hits = [(i + 1, ln) for i, ln in enumerate(lines) if LEFTOVER.search(ln)]
    print("leftover lines  :", len(hits))
    if "--leftovers" in sys.argv:
        for n, ln in hits:
            print("  %5d %s" % (n, ln.strip()[:170]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
