#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build pairs-T12-annexB.json  (技术 12 + 附录 B).

Appendix-B pairs are built from the *extracted* table rows (so `old` is
byte-exact by construction) and only the `<td><code>...</td>` content is
rewritten by hand.  T12 pairs are typed and verified against the file.
"""
import difflib
import json
import re

SRC = "manuel-zh.html"
OUT = "pairs-T12-annexB.json"

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

TAGS = ["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table", "thead",
        "tbody", "tr", "td", "th", "div", "span", "code", "em", "i", "b",
        "a", "main", "body", "html", "head", "small", "blockquote",
        "details", "summary", "sub", "sup", "br", "src"]


def tagmultiset(s):
    out = {}
    for t in TAGS:
        n = (len(re.findall(r"<%s[\s>/]" % t, s))
             + len(re.findall(r"</%s\s*>" % t, s)))
        if n:
            out[t] = n
    return out


def strip_math(s):
    """Remove math spans and the empty <sub></sub> placeholders (see below)."""
    return re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", "", s).replace("<sub></sub>", "")


def is_subseq(a, b):
    it = iter(b)
    return all(ch in it for ch in a)


# ----------------------------------------------------------------- appendix B
# table rows, in document order
i = next(k for k, l in enumerate(lines) if 'id="annexe-b"' in l)
rows = []
for l in lines[i:]:
    if l.startswith("<tr><td>"):
        rows.append(l)
    if "</tbody></table>" in l:
        break
assert len(rows) == 24, len(rows)
for n, r in enumerate(rows, 1):
    print("row %2d: %s" % (n, r[:34]))

ROW = {}   # row number -> new line (rows not listed stay untouched)

ROW[1] = '<tr><td>欧姆定律</td><td><code>\\[ U = R \\cdot I \\]\u3000（即 \\[ I = \\dfrac{U}{R} \\]，\\[ R = \\dfrac{U}{I} \\]）</code></td><td class="small">\u00a71.2</td></tr>'
ROW[2] = '<tr><td>电功率</td><td><code>\\[ P = U \\cdot I = R \\cdot I^2 = \\dfrac{U^2}{R} \\]</code></td><td class="small">\u00a71.2</td></tr>'
ROW[3] = '<tr><td>电阻串联</td><td><code>\\[ R_t = R_1 + R_2 + \\dots \\]</code></td><td class="small">\u00a71.7</td></tr>'
ROW[4] = '<tr><td>电阻并联</td><td><code>\\[ \\dfrac{1}{R_t} = \\dfrac{1}{R_1} + \\dfrac{1}{R_2} + \\dots \\]；两电阻时 \\[ R_t = \\dfrac{R_1 \\cdot R_2}{R_1 + R_2} \\]</code></td><td class="small">\u00a71.7</td></tr>'
ROW[5] = '<tr><td>电容并联 / 串联</td><td><code>并联相加 \\[ C_t = C_1 + C_2 \\]；串联按倒数相加（与电阻相反）</code></td><td class="small">\u00a72.3</td></tr>'
ROW[7] = '<tr><td>容抗</td><td><code>\\[ Z_C = X_C = \\dfrac{1}{2\\pi f C} \\]<sub></sub><sub></sub></code></td><td class="small">\u00a72.3f1</td></tr>'
ROW[8] = '<tr><td>感抗</td><td><code>\\[ Z_L = X_L = 2\\pi f L \\]<sub></sub><sub></sub></code></td><td class="small">\u00a72.3f1</td></tr>'
ROW[9] = '<tr><td>阻抗（RLC 串联）</td><td><code>\\[ Z = \\sqrt{R^2 + (X_L - X_C)^2} \\]<sub></sub><sub></sub></code></td><td class="small">\u00a72.5</td></tr>'
ROW[10] = '<tr><td>谐振条件 / 谐振频率</td><td><code>\\[ X_L = X_C \\] 即 \\[ \\omega L = \\dfrac{1}{\\omega C} \\]；\\[ f = \\dfrac{1}{2\\pi\\sqrt{LC}} \\]（汤姆孙公式）<sub></sub><sub></sub></code></td><td class="small">\u00a74.3 / \u00a74.6</td></tr>'
ROW[11] = '<tr><td>谐振回路简化式</td><td><code>\\[ C\\,(\\text{pF}) = \\dfrac{25\\,330}{f^2\\,(\\text{MHz})} \\]；\\[ L\\,(\\mu\\text{H}) = \\dfrac{25\\,330}{f^2\\,(\\text{MHz})} \\]</code></td><td class="small">\u00a74.6</td></tr>'
ROW[12] = '<tr><td>品质因数 Q</td><td><code>\\[ Q = \\dfrac{Z}{R} = \\dfrac{1}{\\cos\\varphi} \\]；对线圈 \\[ Q = \\dfrac{2\\pi f L}{R} \\]；对电容 \\[ Q = \\dfrac{1}{2\\pi f C R} \\]</code></td><td class="small">\u00a72.3e</td></tr>'
ROW[13] = '<tr><td>交流电与周期</td><td><code>\\[ f = \\dfrac{1}{T} \\]；周期 \\[ T = \\dfrac{1}{f} \\]</code></td><td class="small">\u00a72.1</td></tr>'
ROW[14] = '<tr><td>分贝（功率比）</td><td><code>\\[ G\\,(\\text{dB}) = 10\\log\\left(\\dfrac{P_s}{P_e}\\right) \\]；\\[ P_s = P_e \\times 10^{\\text{dB}/10} \\]</code></td><td class="small">\u00a74.1</td></tr>'
ROW[15] = '<tr><td>常用 dB 值</td><td><code>\\[ 0\\ \\text{dB} = \\times 1 \\]；\\[ 3\\ \\text{dB} \\approx \\times 2 \\]；\\[ 6\\ \\text{dB} \\approx \\times 4 \\]；\\[ 7\\ \\text{dB} \\approx \\times 5 \\]；\\[ 9\\ \\text{dB} \\approx \\times 8 \\]；\\[ 10\\ \\text{dB} = \\times 10 \\]</code></td><td class="small">\u00a74.1</td></tr>'
ROW[16] = '<tr><td>变压器变比</td><td><code>\\[ N = \\dfrac{n_s}{n_p} \\]（\\[ N > 1 \\] 升压）；\\[ \\dfrac{U_s}{U_p} = \\dfrac{n_s}{n_p} \\]；\\[ \\dfrac{I_s}{I_p} = \\dfrac{n_p}{n_s} \\]</code></td><td class="small">\u00a73.1</td></tr>'
ROW[17] = '<tr><td>波长与频率</td><td><code>\\[ \\lambda\\,(\\text{m}) = \\dfrac{300}{f\\,(\\text{MHz})} \\]；\\[ \\lambda\\,(\\text{m}) \\cdot f\\,(\\text{Hz}) = 300\\,000\\,000\\ \\text{m/s} \\]</code></td><td class="small">\u00a79.1</td></tr>'
ROW[18] = '<tr><td>半波振子（偶极）总长</td><td><code>\\[ L\\,(\\text{m}) = \\dfrac{150}{f\\,(\\text{MHz})} \\]\u3000（实际再缩短约 5%）</code></td><td class="small">\u00a79.4</td></tr>'
ROW[19] = '<tr><td>四分之一波长垂直天线</td><td><code>\\[ L\\,(\\text{m}) = \\dfrac{75}{f\\,(\\text{MHz})} \\]\u3000（实际再缩短约 5%）</code></td><td class="small">\u00a79.5</td></tr>'
ROW[20] = '<tr><td>反射系数</td><td><code>\\[ \\rho = \\dfrac{U_r}{U_e} = \\dfrac{U_{max} - U_{min}}{U_{max} + U_{min}} = \\sqrt{\\dfrac{P_r}{P_e}} \\]</code></td><td class="small">\u00a710.3</td></tr>'
ROW[21] = '<tr><td>驻波比 / 百分比</td><td><code>\\[ ROS = \\dfrac{1 + \\rho}{1 - \\rho} \\]；反算 \\[ \\rho = \\dfrac{ROS - 1}{ROS + 1} \\]；\\[ TOS\\,(\\%) = 100 \\cdot \\rho \\]</code></td><td class="small">\u00a710.3</td></tr>'
ROW[22] = '<tr><td>反射功率</td><td><code>\\[ P_{\\text{r\u00e9fl\u00e9chie}} = P_{\\text{\u00e9mise}} \\cdot \\rho^2 \\]</code></td><td class="small">\u00a710.3</td></tr>'
ROW[23] = '<tr><td>AM 占用带宽</td><td><code>\\[ \\text{带宽} = 2 \\times \\text{最高调制频率} \\]（如话音 300\u20133000 Hz \u2192 6 kHz）</code></td><td class="small">\u00a712.3</td></tr>'
ROW[24] = '<tr><td>AM 功率分配（100% 调制）</td><td><code>载波占 \\[ 2/3 \\]，两个边带各占 \\[ 1/6 \\]（边带比载波低 6 dB）</code></td><td class="small">\u00a712.3</td></tr>'

# ------------------------------------------------------------------ 技术 12
T12 = [
    ("<td>占用带宽 = 2 \u00d7 频偏（excursion）</td>",
     "<td>占用带宽 = \\(2 \\times\\) 频偏（excursion）</td>",
     1, "\u00a712.1 \u8868\u683c\uff1a\u5360\u7528\u5e26\u5bbd = 2 \u00d7 \u9891\u504f"),
    ("可以取 2 个状态（0 与 \u03c0，即 2-PSK）、4 个状态（0、\u03c0/2、\u03c0、3\u03c0/2，即 4-PSK）",
     "可以取 2 个状态（\\(0\\) 与 \\(\\pi\\)，即 2-PSK）、4 个状态（\\(0\\)、\\(\\pi/2\\)、\\(\\pi\\)、\\(3\\pi/2\\)，即 4-PSK）",
     1, "\u00a712.1 PSK \u76f8\u4f4d\u72b6\u6001\u4e2d\u7684 \u03c0"),
    ("最多可有 256 个状态（即 16\u00b2）",
     "最多可有 256 个状态（即 \\(16^2\\)）",
     1, "\u00a712.1 QAM \u72b6\u6001\u6570 16\u00b2"),
    ("比特率（bps）= 每秒状态变化数（以 Baud 计，决定占用带宽）\u00d7 信号可取的状态数",
     "比特率（bps）\\(=\\) 每秒状态变化数（以 Baud 计，决定占用带宽）\\(\\times\\) 信号可取的状态数",
     1, "\u00a712.1 \u6bd4\u7279\u7387 = \u72b6\u6001\u53d8\u5316\u7387 \u00d7 \u72b6\u6001\u6570"),
    ("没有 BF 时，高频信号的幅度应为 B/2；",
     "没有 BF 时，高频信号的幅度应为 \\(B/2\\)；",
     1, "\u00a712.3 \u65e0\u8c03\u5236\u65f6\u5e45\u5ea6 B/2"),
    ("高频信号在 B/2 上下摆动",
     "高频信号在 \\(B/2\\) 上下摆动",
     1, "\u00a712.3 \u5305\u7edc\u5728 B/2 \u4e0a\u4e0b\u6446\u52a8"),
    ("在第 2 区测得 A = 4,2 V、a = 1,8 V，求调制深度。",
     "在第 2 区测得 \\(A = 4{,}2\\) V、\\(a = 1{,}8\\) V，求调制深度。",
     1, "\u00a712.3 \u539f\u6587\u4f8b\u9898\u7684\u6d4b\u91cf\u503c"),
    ('<div class="formula">b = A \u2013 a\u3000\u3000B = A + a</div>',
     '<div class="formula">\\[ b = A - a \\]\u3000\u3000\\[ B = A + a \\]</div>',
     1, "\u00a712.3 b = A - a\u3001B = A + a\uff08\u5c55\u793a\u5f0f\uff09"),
    ('<div class="formula">K(%) = (A \u2013 a) / (A + a) = b / B</div>',
     '<div class="formula">\\[ K\\,(\\%) = \\dfrac{A - a}{A + a} = \\dfrac{b}{B} \\]</div>',
     1, "\u00a712.3 \u8c03\u5236\u6df1\u5ea6 K\uff08\u5c55\u793a\u5f0f\uff09"),
    ('<div class="formula">K = (A \u2013 a)/(A + a) = (4,2 \u2013 1,8)/(4,2 + 1,8) = 2,4/6 = 0,4 = 40%\uff082,4 V \u4e0e 6 V \u5373 b \u4e0e B\uff09</div>',
     '<div class="formula">\\(K = \\dfrac{A - a}{A + a} = (4{,}2 - 1{,}8)/(4{,}2 + 1{,}8) = 2{,}4/6 = 0{,}4 = 40\\%\\)\uff08\\(2{,}4\\) V \u4e0e \\(6\\) V \u5373 \\(b\\) \u4e0e \\(B\\)\uff09</div>',
     1, "\u00a712.3 \u539f\u6587\u7b97\u4f8b K = 40%"),
    ("因此当最高调制频率为 fm 时，AM 占用带宽等于 <b>2 \u00d7 fm</b>",
     "因此当最高调制频率为 \\(f_m\\) 时，AM 占用带宽等于 <b>\\(2 \\times f_m\\)</b>",
     1, "\u00a712.3 AM \u5360\u7528\u5e26\u5bbd 2 \u00d7 fm"),
    ('<div class="formula">m = 频偏 (Hz) / BF maxi (Hz)</div>',
     '<div class="formula">\\(m = \\dfrac{\\text{频偏 (Hz)}}{\\text{BF maxi (Hz)}}\\)</div>',
     1, "\u00a712.4 \u8c03\u5236\u6307\u6570 m = \u9891\u504f / BF maxi"),
    ('<div class="formula">B = 2 (m + 1) \u00b7 BF maxi</div>',
     '<div class="formula">\\[ B = 2\\,(m + 1) \\cdot BF_{maxi} \\]</div>',
     1, "\u00a712.4 \u5361\u68ee\u89c4\u5219\uff08\u5c55\u793a\u5f0f\uff09"),
    ('<div class="formula">m = 频偏 / BF maxi = 7,5 kHz / 3000 Hz = 7,5 / 3 = 2,5</div>',
     '<div class="formula">\\(m = \\dfrac{\\text{频偏}}{\\text{BF maxi}} = 7{,}5\\ \\text{kHz} / 3000\\ \\text{Hz} = 7{,}5/3 = 2{,}5\\)</div>',
     1, "\u00a712.4 \u539f\u6587\u7b97\u4f8b m = 2,5"),
    ("当待解调频率接近 FI \u2013 \u03b4F 时",
     "当待解调频率接近 \\(FI - \\delta F\\) 时",
     1, "\u00a712.4 \u9274\u9891\u5668 FI - \u03b4F"),
    ("K = 100%", "\\(K = 100\\%\\)", 2,
     "\u00a712.6 \u529f\u7387\u5173\u7cfb\uff1aK = 100%\uff08\u51fa\u73b0\u4e24\u6b21\uff09"),
    ("载波占发射功率的 <b>2/3</b>",
     "载波占发射功率的 <b>\\(2/3\\)</b>", 1,
     "\u00a712.6 \u8f7d\u6ce2\u5360\u53d1\u5c04\u529f\u7387\u7684 2/3"),
    ("输出只有 f1 + f2 与 f1 \u2013 f2，",
     "输出只有 \\(f_1 + f_2\\) 与 \\(f_1 - f_2\\)，", 1,
     "\u00a712.6 \u73af\u5f62\u6df7\u9891\u5668\u8f93\u51fa f1 \u00b1 f2"),
    ("<td>B = 2(m + 1) \u00b7 BF maxi（卡森规则，含 98% 功率）；频偏低时约等于 2 \u00d7 频偏</td>",
     "<td>\\(B = 2\\,(m + 1) \\cdot BF_{maxi}\\)（卡森规则，含 98% 功率）；频偏低时约等于 \\(2 \\times\\) 频偏</td>",
     1, "\u00a712.6 \u5404\u7c7b\u53d1\u5c04\u5360\u7528\u5e26\u5bbd\u5c0f\u7ed3\u8868 FM \u884c"),
]

PAIRS = []
for old, new, cnt, note in T12:
    PAIRS.append({"old": old, "new": new, "count": cnt, "note": note})
for n in sorted(ROW):
    PAIRS.append({"old": rows[n - 1], "new": ROW[n], "count": 1,
                  "note": "附录 B \u7b2c %d \u884c\uff1a%s" % (n, rows[n - 1][8:26])})

# ----------------------------------------------------------------- validation
bad = 0
for k, p in enumerate(PAIRS, 1):
    old, new = p["old"], p["new"]
    tag = "%s#%d" % (p["note"][:22], k)
    if "\n" in old or "\n" in new:
        print("!! %s multi-line" % tag); bad += 1
    if "$" in new:
        print("!! %s dollar in new" % tag); bad += 1
    if tagmultiset(old) != tagmultiset(new):
        print("!! %s tag multiset %s -> %s" % (tag, tagmultiset(old), tagmultiset(new))); bad += 1
    got = text.count(old)
    if got != p["count"]:
        print("!! %s found %d want %d" % (tag, got, p["count"]))
        scored = sorted(((difflib.SequenceMatcher(None, old, l).ratio(), n, l)
                         for n, l in enumerate(lines, 1)), reverse=True)[:1]
        for r, n, l in scored:
            print("     closest line %d ratio %.3f" % (n, r))
            sm = difflib.SequenceMatcher(None, old, l)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != "equal":
                    print("       %-8s old[%d:%d]=%r  file=%r"
                          % (op, a1, a2, old[a1:a2], l[b1:b2]))
        bad += 1
    if new.count("\\(") != new.count("\\)") or new.count("\\[") != new.count("\\]"):
        print("!! %s unbalanced delimiters in new" % tag); bad += 1
    if not is_subseq(strip_math(new), old):
        print("!! %s strip_math(new) not a subsequence of old" % tag); bad += 1

print("\npairs: %d   problems: %d" % (len(PAIRS), bad))
if bad:
    raise SystemExit(1)

data = {"section": "T12 \u00a712.1\u2013\u00a712.6 \u8c03\u5236\u65b9\u5f0f\u4e0e\u5360\u7528\u5e26\u5bbd + \u9644\u5f55 B \u516c\u5f0f\u901f\u67e5",
        "pairs": PAIRS}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("wrote", OUT)
