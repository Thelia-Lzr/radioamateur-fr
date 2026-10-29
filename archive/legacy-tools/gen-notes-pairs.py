#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build pairs-notes-section.json for the 68 <div class="note"> blocks.

Every `old` is checked against the real file; `count` is computed from the
file.  A dry in-memory application also verifies that the pairs do not
interfere with each other.
"""
import json
import os
import sys

HERE = "/home/thelia/Documents/radioamateur-fr"
sys.path.insert(0, HERE)
import apply_pairs  # noqa: E402  (tagmultiset / tag_balanced)

TARGET = os.path.join(HERE, "manuel-zh.html")

P = []  # (old, new, note)


def add(old, new, note):
    P.append((old, new, note))


# ---------------------------------------------------------------- L2758
add("**PIRE = PAR + 2,14 dB = PAR × 1,64**",
    r"**\(\mathrm{PIRE} = \mathrm{PAR} + 2{,}14\ \mathrm{dB} = \mathrm{PAR} \times 1{,}64\)**",
    "L2758 PIRE/PAR 换算（加粗行内式）")
add("补充系数 1,64 = 1 + 2/π。",
    r"补充系数 \(1{,}64 = 1 + 2/\pi\)。",
    "L2758 1,64 = 1 + 2/π")

# ---------------------------------------------------------------- L2998
add("<td>A + B = C – D</td><td>A × B = C / D</td><td>A² = B ou C = √D</td>",
    r"<td>\(A + B = C - D\)</td><td>\(A \times B = \dfrac{C}{D}\)</td>"
    r"<td>\(A^2 = B\) ou \(C = \sqrt{D}\)</td>",
    "L2998 方程变换表 Équation 行")
add("<td>X + A = C − D → X = C − D − A；X − A = 0 → X = A</td>"
    "<td>X × A = C × D → X = (C × D) / A；X / A = B → X = B × A</td>"
    "<td>X² = B → X = √B；√X = D → X = D²</td>",
    r"<td>\(X + A = C - D \rightarrow X = C - D - A\)；\(X - A = 0 \rightarrow X = A\)</td>"
    r"<td>\(X \times A = C \times D \rightarrow X = \dfrac{C \times D}{A}\)；"
    r"\(\dfrac{X}{A} = B \rightarrow X = B \times A\)</td>"
    r"<td>\(X^2 = B \rightarrow X = \sqrt{B}\)；\(\sqrt{X} = D \rightarrow X = D^2\)</td>",
    "L2998 方程变换表 Exemples 行")

# ---------------------------------------------------------------- L4172
add("（20084：Z = 1/(2πFC)，题解用 159/F(MHz)/C(nF)）",
    r"（20084：\(Z = \dfrac{1}{2\pi F C}\)，题解用 \(159/F\,(\text{MHz})/C\,(\text{nF})\)）",
    "L4172 电容电抗 20084")
add("（两只电容时 C1·C2/(C1+C2)）",
    r"（两只电容时 \(\dfrac{C_1 \cdot C_2}{C_1 + C_2}\)）",
    "L4172 两只电容串联")
add("并用 Q = C·U（电量）",
    r"并用 \(Q = C \cdot U\)（电量）",
    "L4172 电量 Q = C·U")
add("（PDF 第 52 页）：Q = Z / R = 1 / cos φ，且 Q = 2πfL/R = 1/(2πfCR)；"
    "原文例：Z = 80 Ω、R = 69 Ω → Q = 1,16。",
    r"（PDF 第 52 页）：\(Q = \dfrac{Z}{R} = \dfrac{1}{\cos\varphi}\)，且 "
    r"\(Q = \dfrac{2\pi f L}{R} = \dfrac{1}{2\pi f C R}\)；原文例：\(Z = 80\) Ω、\(R = 69\) Ω → "
    r"\(Q = 1{,}16\)。",
    "L4172 品质因数 Q（§2.5e）")
add("Z_C = Z_L → ωL = 1/(ωC) →",
    r"\(Z_C = Z_L \rightarrow \omega L = \dfrac{1}{\omega C}\) →",
    "L4172 汤姆孙定律开头 Z_C = Z_L …")
add("；完整变体见 §4.6a（C = 1/4π²f²L、ω = 1/√(LC)、X_L = X_C = √(L/C) 等）。",
    r"；完整变体见 §4.6a（\(C = \dfrac{1}{4\pi^2 f^2 L}\)、\(\omega = \dfrac{1}{\sqrt{LC}}\)、"
    r"\(X_L = X_C = \sqrt{L/C}\) 等）。",
    "L4172 §4.6a 完整变体")

# ---------------------------------------------------------------- L4483
add("图给出 R = 10 Ω、I = 5 mA，求",
    r"图给出 \(R = 10\) Ω、\(I = 5\) mA，求",
    "L4483 题 20357 已知数据")
add("R 上的电压 U = R·I = 10 × 5·10⁻³ = 50 mV，而 10 mΩ 的内阻在 5 mA 下只产生 "
    "10 mΩ × 5 mA = 50 µV 的扰动",
    r"R 上的电压 \(U = R \cdot I = 10 \times 5 \cdot 10^{-3} = 50\ \text{mV}\)，"
    r"而 10 mΩ 的内阻在 5 mA 下只产生 "
    r"\(10\ \text{m}\Omega \times 5\ \text{mA} = 50\ \mu\text{V}\) 的扰动",
    "L4483 U = R·I 与 10 mΩ × 5 mA")
add("例题里的 Ri = 10 Ω 只是",
    r"例题里的 \(R_i = 10\) Ω 只是",
    "L4483 §3.4 例题 Ri = 10 Ω")

# ---------------------------------------------------------------- L4707
add("（= 1 − 1/e，e = 2,718；约记作 2/3）",
    r"（\(= 1 - \dfrac{1}{e}\)，\(e = 2{,}718\)；约记作 2/3）",
    "L4707 充电 63,21 % = 1 − 1/e")
add("原文例：C = 100 µF 经 R = 8 kΩ 放电，T = 8 kΩ × 100 µF = 800 ms，5 T = 4 s。",
    r"原文例：\(C = 100\) µF 经 \(R = 8\) kΩ 放电，"
    r"\(T = 8\ \text{k}\Omega \times 100\ \mu\text{F} = 800\ \text{ms}\)，\(5T = 4\) s。",
    "L4707 时间常数算例")
add("只讲截止频率（f = 1/(2πRC)，简化式 159/R(kΩ)/C(µF)）",
    r"只讲截止频率（\(f = \dfrac{1}{2\pi R C}\)，简化式 "
    r"\(159/R\,(\text{k}\Omega)/C\,(\mu\text{F})\)）",
    "L4707 §4.2 截止频率")

# ---------------------------------------------------------------- L4988
for cell, new in [
    ("<td>灰 8、棕 1、绿 5 → 81 × 10⁵</td>", r"<td>灰 8、棕 1、绿 5 → \(81 \times 10^5\)</td>"),
    ("<td>橙 3、蓝 6、蓝 6 → 36 × 10⁶</td>", r"<td>橙 3、蓝 6、蓝 6 → \(36 \times 10^6\)</td>"),
    ("<td>灰 8、黑 0、绿 5 → 80 × 10⁵</td>", r"<td>灰 8、黑 0、绿 5 → \(80 \times 10^5\)</td>"),
    ("<td>灰 8、蓝 6、绿 5 → 86 × 10⁵</td>", r"<td>灰 8、蓝 6、绿 5 → \(86 \times 10^5\)</td>"),
    ("<td>蓝 6、红 2、蓝 6 → 62 × 10⁶</td>", r"<td>蓝 6、红 2、蓝 6 → \(62 \times 10^6\)</td>"),
    ("<td>蓝 6、黄 4、灰 8 → 64 × 10⁸</td>", r"<td>蓝 6、黄 4、灰 8 → \(64 \times 10^8\)</td>"),
]:
    add(cell, new, "L4988 色环题计算列 " + cell[8:14])

# ---------------------------------------------------------------- L5471
add("A 类 a = 360°（全周期导通）、B 类 a = 180°、AB 类 180° < a < 360°、"
    "C 类 0 < a < 180°、D 类为开关工作 a = 0。",
    r"A 类 \(a = 360^\circ\)（全周期导通）、B 类 \(a = 180^\circ\)、"
    r"AB 类 \(180^\circ < a < 360^\circ\)、C 类 \(0 < a < 180^\circ\)、"
    r"D 类为开关工作 \(a = 0\)。",
    "L5471 导通角外部补充（a = 360° 等）")

# ---------------------------------------------------------------- L5588
add("「Gain (dB) = 10 log (Ps / Pe)」",
    r"「\(\text{Gain (dB)} = 10 \log \left(\dfrac{P_s}{P_e}\right)\)」",
    "L5588 功率增益公式")
add("「Ps = 10^(dB/10) × Pe」",
    r"「\(P_s = 10^{\text{dB}/10} \times P_e\)」",
    "L5588 功率比换算")
add("「Gain (dB) = 20 log (Us / Ue)」",
    r"「\(\text{Gain (dB)} = 20 \log \left(\dfrac{U_s}{U_e}\right)\)」",
    "L5588 电压增益公式")
add("「Gain (dB) = 20 log (Us / Ue) + 10 log (Ze / Zs)」",
    r"「\(\text{Gain (dB)} = 20 \log \left(\dfrac{U_s}{U_e}\right) + "
    r"10 \log \left(\dfrac{Z_e}{Z_s}\right)\)」",
    "L5588 阻抗不同时的电压增益")

# ---------------------------------------------------------------- L5776
add("输出端产生 F1 + F2 与 F1 − F2，",
    r"输出端产生 \(F_1 + F_2\) 与 \(F_1 - F_2\)，",
    "L5776 混频器输出 F1 ± F2")
add("除 f1、f2、2f1、2f2、f1 ± f2（二次失真）外还有 (2f1 + f2)、(2f1 − f2) 等三次项",
    r"除 \(f_1\)、\(f_2\)、\(2f_1\)、\(2f_2\)、\(f_1 \pm f_2\)（二次失真）外还有 "
    r"\((2f_1 + f_2)\)、\((2f_1 - f_2)\) 等三次项",
    "L5776 非理想混频的产物")
add("给出 FI = HF − FO（infradyne，FO < HF）、FI = FO − HF（supradyne，FO > HF）或 FI = FO + HF",
    r"给出 \(FI = HF - FO\)（infradyne，\(FO < HF\)）、\(FI = FO - HF\)"
    r"（supradyne，\(FO > HF\)）或 \(FI = FO + HF\)",
    "L5776 §11.2 中频三式")
add("示例 HF = 14 MHz、FO = 5 MHz、FI = 9 MHz 时 Fim = |2·FO − HF| = |2·FI − HF| = 4 MHz",
    r"示例 \(HF = 14\) MHz、\(FO = 5\) MHz、\(FI = 9\) MHz 时 "
    r"\(Fim = |2 \cdot FO - HF| = |2 \cdot FI - HF| = 4\) MHz",
    "L5776 §11.3 镜像频率算例")

# ---------------------------------------------------------------- L5777
add("放大器输入端同时有 f1 = 145 MHz 与 f2 = 150 MHz 两个频率",
    r"放大器输入端同时有 \(f_1 = 145\) MHz 与 \(f_2 = 150\) MHz 两个频率",
    "L5777 题 20155 两个输入频率")
add("二次（交调）失真下输出为 f1、f2、2f1、2f2、f1 + f2、f1 − f2，"
    "即 145、150、290（= 2 × 145，145 MHz 的二次谐波）、"
    "300（= 2 × 150，150 MHz 的二次谐波）、295（= 145 + 150，和频）、"
    "5（= 150 − 145 或 145 − 150，差频）MHz",
    r"二次（交调）失真下输出为 \(f_1\)、\(f_2\)、\(2f_1\)、\(2f_2\)、"
    r"\(f_1 + f_2\)、\(f_1 - f_2\)，即 145、150、290（\(= 2 \times 145\)，145 MHz 的二次谐波）、"
    r"300（\(= 2 \times 150\)，150 MHz 的二次谐波）、295（\(= 145 + 150\)，和频）、"
    r"5（\(= 150 - 145\) 或 \(145 - 150\)，差频）MHz",
    "L5777 二次失真产物清单")
add("其中 300 MHz 对应 2 × f2，即输入端 150 MHz 信号的二次谐波；290 MHz 对应 2 × f1。",
    r"其中 300 MHz 对应 \(2 \times f_2\)，即输入端 150 MHz 信号的二次谐波；"
    r"290 MHz 对应 \(2 \times f_1\)。",
    "L5777 谐波归属")
add("「一次谐波 2f1、2f2 与和差频 f1 + f2、f1 − f2 同时出现」",
    r"「一次谐波 \(2f_1\)、\(2f_2\) 与和差频 \(f_1 + f_2\)、\(f_1 - f_2\) 同时出现」",
    "L5777 §7.4b3 引述")

# ---------------------------------------------------------------- L6247
add("写明 L(m) = 150 / f(MHz) = λ/2，题图上的偶极总长 18 m，故 f = 150 / 18 = 8,33 MHz；"
    "同一长度的其它公式正好构成干扰项：300 / 18 = 16,66 MHz（全波）、"
    "75 / 18 = 4,16 MHz（四分之一波）。",
    r"写明 \(L\,(\text{m}) = \dfrac{150}{f\,(\text{MHz})} = \lambda/2\)，"
    r"题图上的偶极总长 18 m，故 \(f = 150/18 = 8{,}33\) MHz；"
    r"同一长度的其它公式正好构成干扰项：\(300/18 = 16{,}66\) MHz（全波）、"
    r"\(75/18 = 4{,}16\) MHz（四分之一波）。",
    "L6247 偶极长度公式与三个干扰项")

# ---------------------------------------------------------------- L6456
add("16 dB ⇒ 10^(16/10) = 39,8 ≈ 40，PIRE = 10 W × 40 = 400 W PIRE。",
    r"16 dB ⇒ \(10^{16/10} = 39{,}8 \approx 40\)，"
    r"\(\mathrm{PIRE} = 10\ \text{W} \times 40 = 400\ \text{W}\) PIRE。",
    "L6456 题 20188 的换算")
add("100 W × 20 = 2000 W PAR（注意该例用的是 dBd）",
    r"\(100\ \text{W} \times 20 = 2000\ \text{W}\) PAR（注意该例用的是 dBd）",
    "L6456 §9.8 例题 100 W × 20")
add("原文 §9.8 给出：PIRE = PAR + 2,14 dB = PAR × 1,64。",
    r"原文 §9.8 给出：\(\mathrm{PIRE} = \mathrm{PAR} + 2{,}14\ \mathrm{dB} = \mathrm{PAR} \times 1{,}64\)。",
    "L6456 PIRE/PAR 换算（§9.8）")
add("答案才是 400 / 1,64 ≈ 244 W",
    r"答案才是 \(400/1{,}64 \approx 244\) W",
    "L6456 换算回 PAR")

# ---------------------------------------------------------------- L6530
add("f(MHz) = 159 / √(L(µH) × C(pF))，例题为 L = 32 µH、C = 200 pF → "
    "f = 159 / √(32 × 200) = 159 / 80 = 1,9875 ≈ 2 MHz。",
    r"\(f\,(\text{MHz}) = \dfrac{159}{\sqrt{L\,(\mu\text{H}) \times C\,(\text{pF})}}\)，"
    r"例题为 \(L = 32\) µH、\(C = 200\) pF → "
    r"\(f = \dfrac{159}{\sqrt{32 \times 200}} = 159/80 = 1{,}9875 \approx 2\) MHz。",
    "L6530 题 20427 简化式与例题")
add("本题 C = 400 pF、L = 25 nH，即 0,025 µH："
    "f = 159 / √(0,025 × 400) = 159 / √10 = 159 / 3,16 = 50,28 ≈ 50 MHz"
    "（自然式 f = 1 / (2π√(LC)) = 1 / (2π√(25·10⁻⁹ × 400·10⁻¹²)) = 50,3 MHz）。",
    r"本题 \(C = 400\) pF、\(L = 25\) nH，即 \(0{,}025\) µH："
    r"\(f = \dfrac{159}{\sqrt{0{,}025 \times 400}} = \dfrac{159}{\sqrt{10}} = 159/3{,}16 "
    r"= 50{,}28 \approx 50\) MHz（自然式 \(f = \dfrac{1}{2\pi\sqrt{LC}} "
    r"= \dfrac{1}{2\pi\sqrt{25 \cdot 10^{-9} \times 400 \cdot 10^{-12}}} = 50{,}3\) MHz）。",
    "L6530 本题 L/C 代入与自然式")

# ---------------------------------------------------------------- L6656
add("（60 · ln(10) = 138,2）",
    r"（\(60 \cdot \ln(10) = 138{,}2\)）",
    "L6656 系数 138,2 的来历")
add("「PE 介质、编织网/内导体直径比 3,5 时 Z = 50 Ω」",
    r"「PE 介质、编织网/内导体直径比 3,5 时 \(Z = 50\) Ω」",
    "L6656 唯一算例 Z = 50 Ω")
add("（(138/√2,3) × log₁₀3,5 ≈ 49,5 Ω ≈ 50 Ω）",
    r"（\((138/\sqrt{2{,}3}) \times \log_{10} 3{,}5 \approx 49{,}5\ \Omega \approx 50\ \Omega\)）",
    "L6656 算例代入")

# ---------------------------------------------------------------- L6984
# (两张表的单元格已由另一位同事在并发编辑中转好，此处只做正文)
add("原文算例：HF = 14 MHz、FO = 5 MHz、FI = 9 MHz。",
    r"原文算例：\(\text{HF} = 14\) MHz、\(\text{FO} = 5\) MHz、\(\text{FI} = 9\) MHz。",
    "L6984 原文算例已知量")
add("Fim 由 2·FO 或 2·FI 算出",
    r"Fim 由 \(2 \cdot \text{FO}\) 或 \(2 \cdot \text{FI}\) 算出",
    "L6984 Fim 的两种算法")
add("混频得到 9 MHz（4 + 5 = 9），即中频",
    r"混频得到 9 MHz（\(4 + 5 = 9\)），即中频",
    "L6984 4 + 5 = 9")
add("（本例如上，低外差且 FI = HF – FO）：Fim = \\|(2 × 5) – 14\\| = "
    "\\|(2 × 9) – 14\\| = 4 MHz。",
    r"（本例如上，低外差且 \(\text{FI} = \text{HF} - \text{FO}\)）："
    r"\(\text{Fim} = |(2 \times 5) - 14| = |(2 \times 9) - 14| = 4\) MHz。",
    "L6984 原文算例续")

# ---------------------------------------------------------------- L7315
add("AM 的频谱是载波加两条边带 HF + BF 与 HF – BF（§12.1c：",
    r"AM 的频谱是载波加两条边带 \(HF + BF\) 与 \(HF - BF\)（§12.1c：",
    "L7315 两条边带")
add("所以整段频谱宽度 = (HF + BFmaxi) – (HF – BFmaxi) = 2 · BFmaxi。",
    r"所以整段频谱宽度 \(= (HF + BF_{maxi}) - (HF - BF_{maxi}) = 2 \cdot BF_{maxi}\)。",
    "L7315 带宽推导")
add("即 6 kHz = 2 × 3 kHz；",
    r"即 \(6\ \text{kHz} = 2 \times 3\ \text{kHz}\)；",
    "L7315 数值印证")
add("例：常规话务 BF 300–3000 Hz ⇒ AM 占用带宽 = 2 × 3000 = 6000 Hz = 6 kHz；",
    r"例：常规话务 BF 300–3000 Hz ⇒ AM 占用带宽 \(= 2 \times 3000 = 6000\ \text{Hz} = 6\ \text{kHz}\)；",
    "L7315 常规话务算例")

# ---------------------------------------------------------------- L7379
add("调制指数 m < 1（窄带 FM，NBFM）时应使用的替换公式",
    r"调制指数 \(m < 1\)（窄带 FM，NBFM）时应使用的替换公式",
    "L7379 窄带条件")
add("而 AM 带宽 = 2 × BFmaxi（§12.1c/§12.6a，见本教材 §12.3 一条）。",
    r"而 AM 带宽 \(= 2 \times BF_{maxi}\)（§12.1c/§12.6a，见本教材 §12.3 一条）。",
    "L7379 AM 带宽")
add("当 m → 0 时 B → 2 · BFmaxi；m < 1 时该式给出 2·BFmaxi < B < 4·BFmaxi，"
    "工程上取窄带近似 B ≈ 2 · BFmaxi（m ≪ 1 时只保留载波与一次边带，故带宽 = 2·fm）。",
    r"当 \(m \rightarrow 0\) 时 \(B \rightarrow 2 \cdot BF_{maxi}\)；\(m < 1\) 时该式给出 "
    r"\(2 \cdot BF_{maxi} < B < 4 \cdot BF_{maxi}\)，工程上取窄带近似 "
    r"\(B \approx 2 \cdot BF_{maxi}\)（\(m \ll 1\) 时只保留载波与一次边带，"
    r"故带宽 \(= 2 \cdot f_m\)）。",
    "L7379 卡森极限")
add("3) 外部印证：窄带调频（调制指数 h ≪ 1）的带宽约为 2·fm，fm 为最高调制频率。",
    r"3) 外部印证：窄带调频（调制指数 \(h \ll 1\)）的带宽约为 \(2 \cdot f_m\)，"
    r"\(f_m\) 为最高调制频率。",
    "L7379 窄带调频带宽")
add("例：BFmaxi = 3 kHz、频偏 (±ΔF) = 1,5 kHz ⇒ m = 0,5 < 1，取 B ≈ 2 × 3 = 6 kHz"
    "（若用卡森公式得 9 kHz，属偏大的上限）。",
    r"例：\(BF_{maxi} = 3\) kHz、频偏 \((\pm\Delta F) = 1{,}5\) kHz ⇒ "
    r"\(m = 0{,}5 < 1\)，取 \(B \approx 2 \times 3 = 6\) kHz"
    r"（若用卡森公式得 9 kHz，属偏大的上限）。",
    "L7379 数值算例")
add("「m ≥ 1 ⇒ B = 2(m + 1) · BFmaxi（卡森规则，含 98% 功率）；"
    "m < 1（NBFM）⇒ B ≈ 2 × BFmaxi，即等于 AM 带宽」",
    r"「\(m \ge 1 \Rightarrow B = 2(m + 1) \cdot BF_{maxi}\)（卡森规则，含 98% 功率）；"
    r"\(m < 1\)（NBFM）\(\Rightarrow B \approx 2 \times BF_{maxi}\)，即等于 AM 带宽」",
    "L7379 小结表写法")

# ---------------------------------------------------------------- L652
add("实际是 1×10⁻⁴ 与 5×10⁻⁵。",
    r"实际是 \(1 \times 10^{-4}\) 与 \(5 \times 10^{-5}\)。",
    "L652 规范值 1×10⁻⁴ / 5×10⁻⁵")


def main():
    text = open(TARGET, encoding="utf-8").read()
    out = []
    bad = []
    for i, (old, new, note) in enumerate(P, 1):
        if "\n" in old or "\n" in new:
            bad.append((i, "multiline", note))
            continue
        if "$" in new:
            bad.append((i, "dollar", note))
            continue
        to, tn = apply_pairs.tagmultiset(old), apply_pairs.tagmultiset(new)
        if to != tn or not apply_pairs.tag_balanced(new):
            bad.append((i, "tagmultiset %s -> %s" % (to, tn), note))
            continue
        n = text.count(old)
        if n == 0:
            bad.append((i, "NOT FOUND", note))
            continue
        out.append({"old": old, "new": new, "count": n, "note": note})
    if bad:
        print("PROBLEMS:")
        for i, why, note in bad:
            print("  #%d %s  %s" % (i, why, note))
        raise SystemExit(1)

    # dry simulation in order
    sim = text
    for p in out:
        sim = sim.replace(p["old"], p["new"])
    ib, ic = sim.count("\\("), sim.count("\\)")
    db, dc = sim.count("\\["), sim.count("\\]")
    print("pairs: %d   \\( %d / \\) %d   \\[ %d / \\] %d   $ %d"
          % (len(out), ib, ic, db, dc, sim.count("$")))
    print("已核实=%d  待核实：=%d  len %d -> %d"
          % (sim.count("\u2705 \u5df2\u6838\u5b9e"),
             sim.count("\u26a0\ufe0f \u5f85\u6838\u5b9e\uff1a"), len(text), len(sim)))
    multi = [p["note"] for p in out if p["count"] != 1]
    if multi:
        print("count != 1:", multi)

    data = {"section": "全部 <div class=\"note\"> 块（68 个，跨全书的待核实事项核对结果）",
            "pairs": out}
    dst = os.path.join(HERE, "pairs-notes-section.json")
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote", dst)


if __name__ == "__main__":
    main()
