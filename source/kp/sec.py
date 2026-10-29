# -*- coding: utf-8 -*-
"""从 cours_utf8.html 抽取某个章节（按 seclab），去标签后输出纯文本。"""
import re, sys, html

SRC = "/home/thelia/Documents/radioamateur-fr/source/cours_utf8.html"


def to_text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|tr|li|h[1-6]|table)>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h)
    h = h.replace("\xa0", " ")
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    return h.strip()


def main():
    sec = sys.argv[1]
    idx = int(sys.argv[2]) if len(sys.argv) > 2 else -1
    raw = open(SRC, encoding="utf-8").read()
    txt = to_text(raw)
    # 找形如 "9.4)" 或 "R-4.2)" 的章节标记
    pat = re.compile(r"(?<![0-9A-Za-z.\-])" + re.escape(sec) + r"\s*\)")
    ms = list(pat.finditer(txt))
    if not ms:
        print("NOT FOUND", sec)
        return
    starts = [m.start() for m in ms]
    if idx >= 0:
        starts = [starts[idx]] if idx < len(starts) else []
        if not starts:
            print("INDEX OOB", sec, len(ms))
            return
    end = len(txt)
    # 下一个章节号（数字.数字 或 R-数字.数字）出现的位置作为结尾
    nxt = re.compile(r"(?<![0-9A-Za-z.\-])(?:R-)?\d{1,2}\.\d{1,2}[a-z]?\s*\)")
    for m in nxt.finditer(txt, starts[0] + len(sec) + 1):
        end = m.start()
        break
    print("OCCURRENCES:", len(ms), "span", starts[0], end)
    print(txt[starts[0]:end])


if __name__ == "__main__":
    main()
