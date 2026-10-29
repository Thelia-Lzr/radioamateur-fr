#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply exact-match replacement pairs to the manual, with hard assertions.

Usage:
    python3 apply_pairs.py pairs-XX.json [more.json ...] [--dry-run] [--quiet]

A pair is {"old":..., "new":..., "count":<int|None>, "note":...}
  * `old` must occur exactly `count` times (None = at least once)
  * `old`/`new` must be single-line
  * `new` may never contain a literal '$'
  * `old` and `new` must contain the SAME multiset of HTML tags: a pair may
    never add or remove a tag, which is what guarantees the conversion
    cannot damage the document structure.

The manual is being maintained concurrently by another process, so this tool
NEVER writes a cached copy: it re-reads the file, checks the protected
content, and re-applies the whole batch on the newest content if it changed
underneath.  It refuses to write if the protected content would be lost.
"""
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "manuel-zh.html")

TAGS = ["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table", "thead",
        "tbody", "tr", "td", "th", "div", "span", "code", "em", "i", "b",
        "a", "main", "body", "html", "head", "small", "blockquote",
        "details", "summary", "sub", "sup", "br", "src"]

VOID_TAGS = {"br", "img", "hr", "meta", "link"}

MARK_VERIFIED = "\u2705 \u5df2\u6838\u5b9e"          # "✅ 已核实"
MARK_PENDING = "\u26a0\ufe0f \u5f85\u6838\u5b9e\uff1a"  # "⚠️ 待核实："
MIN_CHARS = 550000
NEED_VERIFIED = 35


def tagmultiset(s):
    out = {}
    for t in TAGS:
        n = (len(re.findall(r"<%s[\s>/]" % t, s))
             + len(re.findall(r"</%s\s*>" % t, s)))
        if n:
            out[t] = n
    return out


def tag_balanced(s):
    """every tracked tag must be opened and closed the same number of times"""
    for t in TAGS:
        o = len(re.findall(r"<%s[\s>/]" % t, s))
        c = len(re.findall(r"</%s\s*>" % t, s))
        if o != c:
            return False
    return True


def guard(text, where):
    """Protected concurrent content must survive.  Returns list of problems."""
    bad = []
    if len(text) < MIN_CHARS:
        bad.append("%s: only %d chars (need > %d)" % (where, len(text), MIN_CHARS))
    n = text.count(MARK_VERIFIED)
    if n != NEED_VERIFIED:
        bad.append("%s: '已核实' x%d (need %d)" % (where, n, NEED_VERIFIED))
    m = text.count(MARK_PENDING)
    if m != 0:
        bad.append("%s: '待核实：' x%d (need 0)" % (where, m))
    return bad


def load_pairs(files):
    jobs = []
    for jf in files:
        path = jf if os.path.isabs(jf) else os.path.join(HERE, jf)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        jobs.append((data.get("section", os.path.basename(path)), data["pairs"]))
    return jobs


def try_apply(text, jobs):
    applied, problems = [], []
    for section, pairs in jobs:
        for idx, p in enumerate(pairs, 1):
            old, new = p["old"], p["new"]
            label = "%s #%d" % (section, idx)
            if "$" in new:
                problems.append("%s: '$' in replacement" % label)
                continue
            if "\n" in old or "\n" in new:
                problems.append("%s: multi-line pair" % label)
                continue
            to, tn = tagmultiset(old), tagmultiset(new)
            diff = {k: (to.get(k, 0), tn.get(k, 0))
                    for k in set(to) | set(tn) if to.get(k, 0) != tn.get(k, 0)}
            worse = {k: v for k, v in diff.items()
                     if not (k in ("sub", "sup") and v[1] <= v[0])}
            if worse:
                problems.append("%s: tag multiset differs %s -> %s\n      old: %s"
                                % (label, to, tn, old[:120]))
                continue
            got = text.count(old)
            want = p.get("count")
            ok = (got >= 1) if want is None else (got == want)
            if not ok:
                problems.append("%s: found %d, expected %s\n      old: %s"
                                % (label, got, ">=1" if want is None else want, old[:140]))
                continue
            text = text.replace(old, new)
            applied.append((section, idx, got, p.get("note") or old))
    return text, applied, problems


def report(applied, problems, total, quiet):
    for section, idx, got, note in applied:
        if not quiet:
            print("  ok     %-30s #%-3d x%d  %s"
                  % (section[:30], idx, got, note[:58]))
    print("\npairs applied : %d / %d" % (len(applied), total))
    print("pairs failed  : %d" % len(problems))
    for pr in problems:
        print("  !! " + pr)


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    quiet = "--quiet" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: apply_pairs.py pairs-XX.json [--dry-run] [--quiet]")
        return 2
    jobs = load_pairs(files)
    total = sum(len(p) for _, p in jobs)

    for attempt in range(6):
        with open(TARGET, encoding="utf-8") as fh:
            before = fh.read()

        g = guard(before, "file on disk")
        if g:
            print("*** REFUSING TO WORK - protected concurrent content missing ***")
            for x in g:
                print("  !! " + x)
            return 3

        text, applied, problems = try_apply(before, jobs)
        if not quiet:
            report(applied, problems, total, quiet)
        else:
            print("applied %d / %d, failed %d" % (len(applied), total, len(problems)))
            for pr in problems:
                print("  !! " + pr)
        if problems:
            print("NOTHING WRITTEN.")
            return 1

        ib, ic = text.count("\\("), text.count("\\)")
        db, dc = text.count("\\["), text.count("\\]")
        print("delimiters    : \\( %d /\\) %d   \\[ %d /\\] %d   $ %d"
              % (ib, ic, db, dc, text.count("$")))
        if ib != ic or db != dc or "$" in text:
            print("*** DELIMITER PROBLEM - not written ***")
            return 1

        unb = []
        for t in TAGS:
            if t in VOID_TAGS:
                continue
            o = len(re.findall(r"<%s[\s>/]" % t, text))
            c = len(re.findall(r"</%s\s*>" % t, text))
            if o != c:
                unb.append("%s %d/%d" % (t, o, c))
        print("tags          : %s" % ("all %d kinds balanced" % (len(TAGS) - len(VOID_TAGS))
                                      if not unb else "*** UNBALANCED: " + ", ".join(unb)))
        if unb:
            print("*** TAG BALANCE PROBLEM - not written ***")
            return 1

        g = guard(text, "result")
        if g:
            print("*** REFUSING TO WRITE - result would lose protected content ***")
            for x in g:
                print("  !! " + x)
            return 3
        print("guard         : 已核实=%d (need %d)  待核实：=%d  len=%d  OK"
              % (text.count(MARK_VERIFIED), NEED_VERIFIED,
                 text.count(MARK_PENDING), len(text)))

        if dry:
            print("DRY RUN - nothing written.")
            return 0

        # nothing else may have touched the file since we read it
        with open(TARGET, encoding="utf-8") as fh:
            now = fh.read()
        if now != before:
            print("[retry %d] another writer changed the file, re-applying..."
                  % (attempt + 1))
            time.sleep(0.5)
            continue

        tmp = TARGET + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, TARGET)
        after = open(TARGET, encoding="utf-8").read()
        print("\nwrote %s (%+d chars)" % (TARGET, len(text) - len(before)))
        print("post-write    : len=%d  已核实=%d  待核实：=%d  锚点=%d  \\( %d/%d"
              % (len(after), after.count(MARK_VERIFIED), after.count(MARK_PENDING),
                 len(re.findall(r'\bid="[^"]*"', after)),
                 after.count("\\("), after.count("\\)")))
        return 0

    print("gave up after repeated concurrent writes")
    return 1


if __name__ == "__main__":
    sys.exit(main())
