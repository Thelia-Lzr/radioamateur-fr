#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build pairs-T34-section.json  (技术 3 + 技术 4).

Strings are written as Python raw triple-quoted literals so that a single
backslash in the source is a single LaTeX backslash.  Run:
    python3 gen-T34.py check     # self-test against manuel-zh.html
    python3 gen-T34.py json      # write pairs-T34-section.json
"""
import json
import sys

P = []


def add(old, new, count=1, note=r""):
    P.append({"old": old, "new": new, "count": count, "note": note})


# ---------------------------------------------------------------- 3.1
# (order matters: the long line-4341/4342 pairs must run before the short
#  bare ones, otherwise the short ones would match twice)
add(r"""定义<b>变比</b> N = n_s / n_p。N > 1 是升压变压器（élévateur），N < 1 是降压变压器""",
    r"""定义<b>变比</b> \(N = \dfrac{n_s}{n_p}\)。\(N > 1\) 是升压变压器（élévateur），\(N < 1\) 是降压变压器""",
    1, r"§3.1 变比 N 与升/降压判据")
add(r"""理想（完美）变压器 η = 100 %，""",
    r"""理想（完美）变压器 \(\eta = 100\) %，""",
    1, r"§3.1 理想变压器效率")
add(r"""有效电压。U_p = 282 Vmax × 0,707 = 200 Veff；U_s = U_p × N = 200 × 1/10 = 20 Veff。""",
    r"""有效电压。\(U_p = 282\ \text{V}_{max} \times 0{,}707 = 200\ \text{V}_{eff}\)；\(U_s = U_p \times N = 200 \times 1/10 = 20\ \text{V}_{eff}\)。""",
    1, r"§3.1 原文例题 1")
add(r"""N = n_s/n_p = 40/80 = 1/2 = 0,5；Z_p = Z_s / N² = 200 / 0,5² = 800 Ω。""",
    r"""\(N = \dfrac{n_s}{n_p} = 40/80 = 1/2 = 0{,}5\)；\(Z_p = \dfrac{Z_s}{N^2} = 200/0{,}5^2 = 800\) Ω。""",
    1, r"§3.1 原文例题 2 变比与阻抗")
add(r"""用表算：√Z_p = √Z_s × n_p/n_s，""",
    r"""用表算：\(\sqrt{Z_p} = \sqrt{Z_s} \times \dfrac{n_p}{n_s}\)，""",
    1, r"§3.1 交叉相乘（匝数比开方）")
add(r"""平方后 Z_p = Z_s × n_p²/n_s² = 200 × 80²/40² = 200 × 6400/1600 = 800 Ω。""",
    r"""平方后 \(Z_p = Z_s \times \dfrac{n_p^2}{n_s^2} = 200 \times 80^2/40^2 = 200 \times 6400/1600 = 800\) Ω。""",
    1, r"§3.1 阻抗变换平方")
add(r"""①由匝数算出 N = n_s/n_p；""",
    r"""①由匝数算出 \(N = \dfrac{n_s}{n_p}\)；""",
    1, r"§3.1 tips 步①")
add(r"""用 P = U²/R 或 I = U/R 求功率/电流""",
    r"""用 \(P = \dfrac{U^2}{R}\) 或 \(I = \dfrac{U}{R}\) 求功率/电流""",
    1, r"§3.1 tips 步③")
add(r"""直接用 Z_p = Z_s/N²。""",
    r"""直接用 \(Z_p = \dfrac{Z_s}{N^2}\)。""",
    1, r"§3.1 tips 步④")
add(r"""由功率守恒或 P = U·I 求""",
    r"""由功率守恒或 \(P = U \cdot I\) 求""",
    1, r"§3.1 典型考题表")
add(r"""N = 30/3000 = 1/100 ⇒ U_s = 500/100 = 5 V；P = U²/R = 25/50""",
    r"""\(N = 30/3000 = 1/100 \Rightarrow U_s = 500/100 = 5\) V；\(P = \dfrac{U^2}{R} = 25/50\)""",
    1, r"§3.1 典型考题表 500 mW")
add(r"""N = 0,1；Z_p = Z_s/N² = 4/0,1²""",
    r"""\(N = 0{,}1\)；\(Z_p = \dfrac{Z_s}{N^2} = 4/0{,}1^2\)""",
    1, r"§3.1 典型考题表 400 Ω")
add(r"""N = n_s / n_p = U_s / U_p""",
    r"""\(N = \dfrac{n_s}{n_p} = \dfrac{U_s}{U_p}\)""",
    1, r"§3.1 formula 块第 1 行")
add(r"""U_s = U_p × N""",
    r"""\(U_s = U_p \times N\)""",
    1, r"§3.1 formula 块第 2 行")
add(r"""I_s = I_p / N""",
    r"""\(I_s = \dfrac{I_p}{N}\)""",
    1, r"§3.1 formula 块第 3 行")
add(r"""（由功率守恒 U_p·I_p = U_s·I_s）""",
    r"""（由功率守恒 \(U_p \cdot I_p = U_s \cdot I_s\)）""",
    1, r"§3.1 功率守恒")
add(r"""Z_p = Z_s / N²""",
    r"""\(Z_p = \dfrac{Z_s}{N^2}\)""",
    1, r"§3.1 formula 块第 4 行")
add(r"""Z_s = Z_p × N²""",
    r"""\(Z_s = Z_p \times N^2\)""",
    1, r"§3.1 formula 块第 4 行后半")
add(r"""得 U_s = (N × U_p) / 1。""",
    r"""得 \(U_s = (N \times U_p)/1\)。""",
    1, r"§3.1 note 交叉相乘")
add(r"""√Z_p = √Z_s × n_p / n_s，两边平方得 Z_p = Z_s × n_p² / n_s²。""",
    r"""\(\sqrt{Z_p} = \sqrt{Z_s} \times \dfrac{n_p}{n_s}\)，两边平方得 \(Z_p = Z_s \times \dfrac{n_p^2}{n_s^2}\)。""",
    1, r"§3.1 note 阻抗平方")

# ---------------------------------------------------------------- 3.2
add(r"""效率还会放大阻抗变换比：N² / η。""",
    r"""效率还会放大阻抗变换比：\(N^2/\eta\)。""",
    1, r"§3.2 效率放大阻抗变换比")
add(r"""其初级与次级匝数相等（N = 1）。""",
    r"""其初级与次级匝数相等（\(N = 1\)）。""",
    1, r"§3.2 隔离变压器 N = 1")
add(r"""P_s = 14 × 7 = 98；P_p = 220 × 0,665 = 146,3；η = 98 / 146,3 ≈ 67 %。""",
    r"""\(P_s = 14 \times 7 = 98\)；\(P_p = 220 \times 0{,}665 = 146{,}3\)；\(\eta = 98/146{,}3 \approx 67\) %。""",
    1, r"§3.2 效率算例")

# ---------------------------------------------------------------- 3.3
add(r"""Icc(A) = E(V) / Ri(Ω)""",
    r"""\[I_{cc}\,(\text{A}) = \dfrac{E\,(\text{V})}{R_i\,(\Omega)}\]""",
    1, r"§3.3 短路电流（formula 块只有公式）")
add(r"""Q(C) = I(A)·t(s)；""",
    r"""\(Q\,(\text{C}) = I\,(\text{A}) \cdot t\,(\text{s})\)；""",
    1, r"§3.3 容量定义")
add(r"""1 Ah = 3600 C，即 1 C = 1 Ah / 3600。""",
    r"""\(1\ \text{Ah} = 3600\ \text{C}\)，即 \(1\ \text{C} = 1\ \text{Ah}/3600\)。""",
    1, r"§3.3 安时换算")
add(r"""U_R = R·I_R = 200 × 0,04 = 8 V；""",
    r"""\(U_R = R \cdot I_R = 200 \times 0{,}04 = 8\) V；""",
    1, r"§3.3 例题 1（1）")
add(r"""U_Ri = E − U_R = 9 − 8 = 1 V；""",
    r"""\(U_{Ri} = E - U_R = 9 - 8 = 1\) V；""",
    1, r"§3.3 例题 1（2）")
add(r"""Ri = 1 V / 0,04 A = 25 Ω（或 Ri = (E/I) − R = 225 − 200 = 25 Ω）。""",
    r"""\(R_i = 1\ \text{V}/0{,}04\ \text{A} = 25\ \Omega\)（或 \(R_i = \dfrac{E}{I} - R = 225 - 200 = 25\ \Omega\)）。""",
    1, r"§3.3 例题 1 内阻")
add(r"""I = E/(R + ri) = 4,5/(35 + 10) = 0,1 A；""",
    r"""\(I = \dfrac{E}{R + ri} = 4{,}5/(35 + 10) = 0{,}1\) A；""",
    1, r"§3.3 例题 2 电流")
add(r"""P_R = R·I² = 35 × 0,1² = 0,35 W = 350 mW。""",
    r"""\(P_R = R \cdot I^2 = 35 \times 0{,}1^2 = 0{,}35\ \text{W} = 350\ \text{mW}\)。""",
    1, r"§3.3 例题 2 功率")
add(r"""I = E/R = 12/10 = 1,2 A；""",
    r"""\(I = \dfrac{E}{R} = 12/10 = 1{,}2\) A；""",
    1, r"§3.3 例题 3 电流")
add(r"""Q = 1,2 × 3 × 3600 = 12 960 C，即 3,6 Ah。""",
    r"""\(Q = 1{,}2 \times 3 \times 3600 = 12\,960\ \text{C}\)，即 \(3{,}6\ \text{Ah}\)。""",
    1, r"§3.3 例题 3 容量")

# ---------------------------------------------------------------- 3.4
add(r"""或很小的电压（Ri × I_g，即几微伏）""",
    r"""或很小的电压（\(R_i \times I_g\)，即几微伏）""",
    1, r"§3.4 检流计满偏电压")
add(r"""电压表（串联）：R = (U_T / I_g) − Ri = (10 / 0,00002) − 10 = 500000 − 10 = 499990 Ω ≈ 500 kΩ""",
    r"""电压表（串联）：\(R = \dfrac{U_T}{I_g} - R_i = (10/0{,}00002) - 10 = 500000 - 10 = 499990\ \Omega \approx 500\ \text{k}\Omega\)""",
    1, r"§3.4 电压表串联电阻")
add(r"""（中间量：U_g = I_g × Ri = 0,00002 × 10 = 0,0002 V；U_R = U_T − U_g = 10 − 0,0002 = 9,9998 V）""",
    r"""（中间量：\(U_g = I_g \times R_i = 0{,}00002 \times 10 = 0{,}0002\ \text{V}\)；\(U_R = U_T - U_g = 10 - 0{,}0002 = 9{,}9998\ \text{V}\)）""",
    1, r"§3.4 中间量")
add(r"""电流表（并联）：R = U_g / I_R = (Ri × I_g) / (I_T − I_g) = (10 × 0,00002) / (1 − 0,00002) = 0,0002 / 9,99998 ≈ 0,0002 Ω""",
    r"""电流表（并联）：\(R = \dfrac{U_g}{I_R} = \dfrac{R_i \times I_g}{I_T - I_g} = (10 \times 0{,}00002)/(1 - 0{,}00002) = 0{,}0002/9{,}99998 \approx 0{,}0002\ \Omega\)""",
    1, r"§3.4 电流表分流电阻")
add(r"""（20 µA = 0,00002 A）""",
    r"""（\(20\ \mu\text{A} = 0{,}00002\ \text{A}\)）""",
    1, r"§3.4 单位统一")

# ---------------------------------------------------------------- 3.5
add(r"""Q = (R + Ri) / U_T = 1 / I_g""",
    r"""\(Q = \dfrac{R + R_i}{U_T} = \dfrac{1}{I_g}\)""",
    1, r"§3.5 电压表品质")
add(r"""即 R = (U_新 − U_原) × Q，等价地 R = (U_新 − U_原) / I_g。""",
    r"""即 \(R = (U_{\text{新}} - U_{\text{原}}) \times Q\)，等价地 \(R = \dfrac{U_{\text{新}} - U_{\text{原}}}{I_g}\)。""",
    1, r"§3.5 扩大量程")
add(r"""扩成 500 V 量程需串联 R = (500 − 10) × 2000 = 980 kΩ。""",
    r"""扩成 500 V 量程需串联 \(R = (500 - 10) \times 2000 = 980\ \text{k}\Omega\)。""",
    1, r"§3.5 真题 980 kΩ")
add(r"""即 I_g = 50 µA""",
    r"""即 \(I_g = 50\ \mu\text{A}\)""",
    1, r"§3.5 好电压表的 I_g")
# NOTE: the two <div class="warn"> blocks of §3.5 / §4.2 were rewritten by a
# parallel agent while this pass was running; their formulas are already
# converted there, so they are deliberately NOT touched here.

# ---------------------------------------------------------------- 3.6
add(r"""因 I = U/R，其刻度是""",
    r"""因 \(I = \dfrac{U}{R}\)，其刻度是""",
    1, r"§3.6 欧姆表")
add(r"""（要求 Ze = Zs = Zcalibre，且 R + Ri 远大于 Zcalibre）""",
    r"""（要求 \(Z_e = Z_s = Z_\text{calibre}\)，且 \(R + R_i\) 远大于 \(Z_\text{calibre}\)）""",
    1, r"§3.6 功率表条件")
add(r"""因 P = U²/R，指针行程的中点""",
    r"""因 \(P = \dfrac{U^2}{R}\)，指针行程的中点""",
    1, r"§3.6 功率表刻度")

# ---------------------------------------------------------------- 4.1
add(r"""增益 G(dB) = 10 × log(Ps / Pe)""",
    r"""增益 \(G\,(\text{dB}) = 10 \times \log\left(\dfrac{P_s}{P_e}\right)\)""",
    1, r"§4.1 功率比增益公式")
add(r"""反向换算：Ps = 10^(dB / 10) × Pe""",
    r"""反向换算：\(P_s = 10^{\text{dB}/10} \times P_e\)""",
    1, r"§4.1 功率比反算")
add(r"""G(dB) = 20 × log(Us / Ue)""",
    r"""\(G\,(\text{dB}) = 20 \times \log\left(\dfrac{U_s}{U_e}\right)\)""",
    1, r"§4.1 电压比增益公式")
add(r"""Us = 10^(dB / 20) × Ue""",
    r"""\(U_s = 10^{\text{dB}/20} \times U_e\)""",
    1, r"§4.1 电压比反算")
add(r"""因为功率与电压的平方成正比（P = U²/R）""",
    r"""因为功率与电压的平方成正比（\(P = \dfrac{U^2}{R}\)）""",
    1, r"§4.1 功率与电压平方")
add(r"""原文例题：Us = 16 V、Ue = 8 V，电压比 2，功率比 2² = 4，功率比 4 对应 6 dB；或直接算 20 log(16/8) = 20 × 0,3 = 6 dB。""",
    r"""原文例题：\(U_s = 16\) V、\(U_e = 8\) V，电压比 2，功率比 \(2^2 = 4\)，功率比 4 对应 6 dB；或直接算 \(20 \log(16/8) = 20 \times 0{,}3 = 6\ \text{dB}\)。""",
    1, r"§4.1 电压比算例")
add(r"""<code>G(dB) = 20 log(Us/Ue) + 10 log(Ze/Zs)</code>""",
    r"""<code>\(G\,(\text{dB}) = 20 \log\left(\dfrac{U_s}{U_e}\right) + 10 \log\left(\dfrac{Z_e}{Z_s}\right)\)</code>""",
    1, r"§4.1 阻抗不同时的公式")
add(r"""是输入与输出阻抗相同（Ze = Zs）""",
    r"""是输入与输出阻抗相同（\(Z_e = Z_s\)）""",
    1, r"§4.1 前提 Ze = Zs")
add(r"""例：Us = 8 V、增益 12 dB → 12 dB 对应电压比 4""",
    r"""例：\(U_s = 8\) V、增益 12 dB → 12 dB 对应电压比 4""",
    1, r"§4.1 四类算法之四")
add(r"""→ Ue = 8 ÷ 4 = <b>2 V</b>；或 Ue = Us / 10^(12/20) = 8 / 3,98 ≈ 2 V。""",
    r"""→ \(U_e = 8 \div 4 =\) <b>2 V</b>；或 \(U_e = \dfrac{U_s}{10^{12/20}} = 8/3{,}98 \approx 2\) V。""",
    1, r"§4.1 四类算法之四（续）")

# ---------------------------------------------------------------- 4.2
add(r"""电容的阻抗与电阻相等（Z_C = R），由此得到""",
    r"""电容的阻抗与电阻相等（\(Z_C = R\)），由此得到""",
    1, r"§4.2 截止频率条件")
add(r"""f_c = 1 / (2π R C)""",
    r"""\(f_c = \dfrac{1}{2\pi R C}\)""",
    1, r"§4.2 截止频率公式")
add(r"""简化式：f(Hz) = 159 / R(kΩ) / C(µF)""",
    r"""简化式：\(f\,(\text{Hz}) = \dfrac{159}{R\,(\text{k}\Omega) \times C\,(\mu\text{F})}\)""",
    1, r"§4.2 简化式")
add(r"""原文例题：R = 200 Ω、C = 5 µF → f = 1 ÷ (2 × π × 200 × 5×10⁻⁶) = 159,15 Hz ≈ <b>159 Hz</b>；""",
    r"""原文例题：\(R = 200\) Ω、\(C = 5\) µF → \(f = 1/(2 \times \pi \times 200 \times 5\times10^{-6}) = 159{,}15\ \text{Hz} \approx\) <b>159 Hz</b>；""",
    1, r"§4.2 原文例题")
add(r"""是频率 ×2ⁿ（即谐波 2ⁿ）；""",
    r"""是频率 \(\times 2^n\)（即谐波 \(2^n\)）；""",
    1, r"§4.2 上八度")
add(r"""第 n 个<b>上十倍频程</b>是 ×10ⁿ；下八度、下十倍频程分别是 ÷2ⁿ、÷10ⁿ。""",
    r"""第 n 个<b>上十倍频程</b>是 \(\times 10^n\)；下八度、下十倍频程分别是 \(\div 2^n\)、\(\div 10^n\)。""",
    1, r"§4.2 十倍频程与下移")
add(r"""功率按 P = U²/R 被除以 2""",
    r"""功率按 \(P = \dfrac{U^2}{R}\) 被除以 2""",
    1, r"§4.2 −3 dB 原理")
add(r"""电压比是 10^(−12/20) = 0,25，故 Vs = 4 × 0,25 = <b>1 V</b>。""",
    r"""电压比是 \(10^{-12/20} = 0{,}25\)，故 \(V_s = 4 \times 0{,}25 =\) <b>1 V</b>。""",
    1, r"§4.2 例题电压比")
add(r"""更精确地算：Z_C = 1/(2πfC) = 5,3052 Ω，Z_RC = √(21,22² + 5,3052²) = 21,873 Ω，Vs = 4 × (5,3052/21,873) = 0,9702 V，""",
    r"""更精确地算：\(Z_C = \dfrac{1}{2\pi f C} = 5{,}3052\) Ω，\(Z_{RC} = \sqrt{21{,}22^2 + 5{,}3052^2} = 21{,}873\) Ω，\(V_s = 4 \times (5{,}3052/21{,}873) = 0{,}9702\) V，""",
    1, r"§4.2 例题精确计算")
add(r"""<code>f = R / (2πL)</code>""",
    r"""<code>\(f = \dfrac{R}{2\pi L}\)</code>""",
    1, r"§4.2 RL 电路截止频率")
# (§4.2 warn block: rewritten by a parallel agent, already in LaTeX.)
add(r"""①问截止频率 → f = 159 / R(kΩ) / C(µF)；""",
    r"""①问截止频率 → \(f = \dfrac{159}{R\,(\text{k}\Omega) \times C\,(\mu\text{F})}\)；""",
    1, r"§4.2 tips 步①")
add(r"""例：输入 4 V、f = f_c = 100 MHz → 输出 2,8 V；""",
    r"""例：输入 4 V、\(f = f_c = 100\) MHz → 输出 2,8 V；""",
    1, r"§4.2 tips 步②")

# ---------------------------------------------------------------- 4.3
add(r"""都有 Z_C = Z_L，这就是""",
    r"""都有 \(Z_C = Z_L\)，这就是""",
    1, r"§4.3 汤姆逊定律的条件")
add(r"""f = 1 / (2π √(L C))""",
    r"""\(f = \dfrac{1}{2\pi\sqrt{L\,C}}\)""",
    1, r"§4.3 汤姆逊公式")
add(r"""简化式：f(MHz) = 159 / √(L(µH) × C(pF))""",
    r"""简化式：\(f\,(\text{MHz}) = \dfrac{159}{\sqrt{L\,(\mu\text{H}) \times C\,(\text{pF})}}\)""",
    1, r"§4.3 汤姆逊简化式")
add(r"""原文例题：L = 32 µH、C = 200 pF → f = 159 / √(32 × 200) = 159 / √6400 = 159 / 80 = 1,9875 ≈ <b>2 MHz</b>；""",
    r"""原文例题：\(L = 32\) µH、\(C = 200\) pF → \(f = \dfrac{159}{\sqrt{32 \times 200}} = \dfrac{159}{\sqrt{6400}} = \dfrac{159}{80} = 1{,}9875 \approx\) <b>2 MHz</b>；""",
    1, r"§4.3 原文例题")
add(r"""用自然书写 1 ÷ (2π√(32×10⁻⁶ × 200×10⁻¹²)) = 1,98944×10⁶ Hz ≈ 2 MHz。""",
    r"""用自然书写 \(1/(2\pi\sqrt{32\times10^{-6} \times 200\times10^{-12}}) = 1{,}98944\times10^{6}\) Hz ≈ 2 MHz。""",
    1, r"§4.3 自然书写校验")
add(r"""①求谐振频率用 159 / √(L(µH) × C(pF))，结果单位是 MHz；""",
    r"""①求谐振频率用 \(\dfrac{159}{\sqrt{L\,(\mu\text{H}) \times C\,(\text{pF})}}\)，结果单位是 MHz；""",
    1, r"§4.3 tips 步①")

# ---------------------------------------------------------------- 4.4
add(r"""原文例题：f_o = 159 / √(LC) = 159 / √(25 × 100) = 159 / 50 = <b>3,18 MHz</b>（L = 25 µH、C = 100 pF）；""",
    r"""原文例题：\(f_o = \dfrac{159}{\sqrt{L\,C}} = \dfrac{159}{\sqrt{25 \times 100}} = \dfrac{159}{50} =\) <b>3,18 MHz</b>（\(L = 25\) µH、\(C = 100\) pF）；""",
    1, r"§4.4 原文例题谐振频率")
add(r"""用自然书写 1 ÷ (2π√(25×10⁻⁶ × 100×10⁻¹²)) = 3,183×10⁶ Hz = 3,183 MHz。""",
    r"""用自然书写 \(1/(2\pi\sqrt{25\times10^{-6} \times 100\times10^{-12}}) = 3{,}183\times10^{6}\) Hz = 3,183 MHz。""",
    1, r"§4.4 自然书写校验")
add(r"""<code>√[ ρ(Ωm) / (π µ₀ µ_r f(Hz)) ]</code>""",
    r"""<code>\(\sqrt{\dfrac{\rho\,(\Omega\text{m})}{\pi \mu_0 \mu_r f\,(\text{Hz})}}\)</code>""",
    1, r"§4.4a1 集肤深度")
add(r"""Z_série = √( R² + [ ωL − 1/(ωC) ]² )""",
    r"""\[Z_{\text{série}} = \sqrt{R^2 + \left[\omega L - \dfrac{1}{\omega C}\right]^2}\]""",
    1, r"§4.4a2 串联阻抗（只有公式）")
add(r"""谐振时 X_L = X_C，即 ωL = 1/(ωC) → Z_série = R_série""",
    r"""谐振时 \(X_L = X_C\)，即 \(\omega L = \dfrac{1}{\omega C} \rightarrow Z_{\text{série}} = R_{\text{série}}\)""",
    1, r"§4.4a2 谐振时阻抗")
add(r"""Z_bouchon = (ωL / ωC) / R = X_L² / R = X_C² / R = L / (R × C)""",
    r"""\[Z_{\text{bouchon}} = \dfrac{(\omega L / \omega C)}{R} = \dfrac{X_L^2}{R} = \dfrac{X_C^2}{R} = \dfrac{L}{R \times C}\]""",
    1, r"§4.4a3 bouchon 阻抗（只有公式）")
add(r"""简化式：Z_bouchon(kΩ) = L(µH) ÷ R(kΩ) ÷ C(pF)""",
    r"""简化式：\(Z_{\text{bouchon}}\,(\text{k}\Omega) = L\,(\mu\text{H}) \div R\,(\text{k}\Omega) \div C\,(\text{pF})\)""",
    1, r"§4.4a3 简化式")
add(r"""例：L = 25 µH、C = 100 pF、R = 20 Ω（= 0,02 kΩ）→ Z = 25×10⁻⁶ / (20 × 100×10⁻¹²) = 1,25×10⁴ = <b>12,5 kΩ</b>；""",
    r"""例：\(L = 25\) µH、\(C = 100\) pF、\(R = 20\) Ω（\(= 0{,}02\) kΩ）→ \(Z = 25\times10^{-6}/(20 \times 100\times10^{-12}) = 1{,}25\times10^{4} =\) <b>12,5 kΩ</b>；""",
    1, r"§4.4a3 算例")
add(r"""所以 Z_parallèle = R_parallèle。原例中不用计算即可看出：Z_série = R = 20 Ω，Z_parallèle = R = 12,5 kΩ。""",
    r"""所以 \(Z_{\text{parallèle}} = R_{\text{parallèle}}\)。原例中不用计算即可看出：\(Z_{\text{série}} = R = 20\) Ω，\(Z_{\text{parallèle}} = R = 12{,}5\) kΩ。""",
    1, r"§4.4a4 并联电路")
add(r"""<tr><td>串联（série）</td><td>Z = R</td><td>Q = X_L / R = X_C / R = √(L/C) / R</td></tr>""",
    r"""<tr><td>串联（série）</td><td>\(Z = R\)</td><td>\(Q = \dfrac{X_L}{R} = \dfrac{X_C}{R} = \dfrac{\sqrt{L/C}}{R}\)</td></tr>""",
    1, r"§4.4 阻抗表第 1 行")
add(r"""<tr><td>并联 / bouchon（用串联电阻表示损耗）</td><td>Z = L / (R × C) = X_L² / R</td><td>Q = Z / X_L = √(L/C) / R</td></tr>""",
    r"""<tr><td>并联 / bouchon（用串联电阻表示损耗）</td><td>\(Z = \dfrac{L}{R \times C} = \dfrac{X_L^2}{R}\)</td><td>\(Q = \dfrac{Z}{X_L} = \dfrac{\sqrt{L/C}}{R}\)</td></tr>""",
    1, r"§4.4 阻抗表第 2 行")
add(r"""<tr><td>并联（用 R_parallèle 表示损耗）</td><td>Z = R_parallèle = R_bouchon × Q²</td><td>Q = R / √(L/C)</td></tr>""",
    r"""<tr><td>并联（用 R_parallèle 表示损耗）</td><td>\(Z = R_{\text{parallèle}} = R_{\text{bouchon}} \times Q^2\)</td><td>\(Q = \dfrac{R}{\sqrt{L/C}}\)</td></tr>""",
    1, r"§4.4 阻抗表第 3 行")
add(r"""Q_bouchon = Z_bouchon / X_L = Z_bouchon / X_C""",
    r"""\[Q_{\text{bouchon}} = \dfrac{Z_{\text{bouchon}}}{X_L} = \dfrac{Z_{\text{bouchon}}}{X_C}\]""",
    1, r"§4.4b Q 公式 1（只有公式）")
add(r"""Q_série    = X_L / Z_série = X_C / R""",
    r"""\[Q_{\text{série}} = \dfrac{X_L}{Z_{\text{série}}} = \dfrac{X_C}{R}\]""",
    1, r"§4.4b Q 公式 2（只有公式）")
add(r"""两者相同：Q = √(L / C) / R""",
    r"""两者相同：\(Q = \dfrac{\sqrt{L/C}}{R}\)""",
    1, r"§4.4b 两者相同的 Q")
add(r"""简化式：Q = √[ L(µH) / C(pF) ] / R(kΩ)""",
    r"""简化式：\(Q = \dfrac{\sqrt{L\,(\mu\text{H})/C\,(\text{pF})}}{R\,(\text{k}\Omega)}\)""",
    1, r"§4.4b Q 简化式")
add(r"""Q_parallèle = Z_parallèle / X_L = R / √(L / C)""",
    r"""\[Q_{\text{parallèle}} = \dfrac{Z_{\text{parallèle}}}{X_L} = \dfrac{R}{\sqrt{L/C}}\]""",
    1, r"§4.4b 并联 Q（只有公式）")
add(r"""X_L = 2πfL = 6,28 × 3,18×10⁶ × 25×10⁻⁶ = 499,26 Ω ≈ 500 Ω；""",
    r"""\(X_L = 2\pi f L = 6{,}28 \times 3{,}18\times10^{6} \times 25\times10^{-6} = 499{,}26\) Ω ≈ 500 Ω；""",
    1, r"§4.4b 原例 X_L")
add(r"""X_C = 1/(2πfC) ≈ 500 Ω；""",
    r"""\(X_C = \dfrac{1}{2\pi f C} \approx 500\) Ω；""",
    1, r"§4.4b 原例 X_C")
add(r"""于是 Q = 12 500 / 500 = <b>25</b>，或 Q = √(25×10⁻⁶ / 100×10⁻¹²) / 20 = 500 / 20 = 25；""",
    r"""于是 \(Q = 12\,500/500 =\) <b>25</b>，或 \(Q = \dfrac{\sqrt{\dfrac{25\times10^{-6}}{100\times10^{-12}}}}{20} = 500/20 = 25\)；""",
    1, r"§4.4b 原例 Q 的三种算法")
add(r"""简化式 Q = √(25/100) / 0,02 = 0,5 / 0,02 = 25。""",
    r"""简化式 \(Q = \sqrt{25/100}/0{,}02 = 0{,}5/0{,}02 = 25\)。""",
    1, r"§4.4b 原例简化式")
add(r"""U = √(P × Z) = √(50×10⁻¹² × 12,5×10³) = √(625×10⁻⁹) = 7,9×10⁻⁴ = <b>790 µV</b>""",
    r"""\(U = \sqrt{P \times Z} = \sqrt{50\times10^{-12} \times 12{,}5\times10^{3}} = \sqrt{625\times10^{-9}} = 7{,}9\times10^{-4} =\) <b>790 µV</b>""",
    1, r"§4.4b4 过压系数算例")
add(r"""恰好等于 √(12 500/50) = √250 = 15,8）""",
    r"""恰好等于 \(\sqrt{12\,500/50} = \sqrt{250} = 15{,}8\)）""",
    1, r"§4.4b4 比值校验")
add(r"""有效电压 U：Q = X_C/R = U_C/U。""",
    r"""有效电压 U：\(Q = \dfrac{X_C}{R} = \dfrac{U_C}{U}\)。""",
    1, r"§4.4b4 串联电路 Q 的第二种写法")
add(r"""③求带宽 → B = f_o / Q；""",
    r"""③求带宽 → \(B = \dfrac{f_o}{Q}\)；""",
    1, r"§4.4 tips 步③（须先于下一对执行）")
add(r"""B = f_o / Q""",
    r"""\[B = \dfrac{f_o}{Q}\]""",
    1, r"§4.4c 带宽（只有公式）")
add(r"""原例：B = 3,18 MHz / 25 = 0,127 MHz = <b>127 kHz</b>（三种电路相同）。""",
    r"""原例：\(B = 3{,}18\ \text{MHz}/25 = 0{,}127\ \text{MHz} =\) <b>127 kHz</b>（三种电路相同）。""",
    1, r"§4.4c 带宽算例")
add(r"""S(%) = ( B × 100 ) / δf à −60 dB""",
    r"""\[S\,(\%) = \dfrac{B \times 100}{\delta f\ \text{à}\ -60\ \text{dB}}\]""",
    1, r"§4.4e 选择性（只有公式）")
add(r"""F = 100 / S""",
    r"""\(F = \dfrac{100}{S}\)""",
    1, r"§4.4e 波形因数")
add(r"""F = δf à −60 dB / B""",
    r"""\(F = \dfrac{\delta f\ \text{à}\ -60\ \text{dB}}{B}\)""",
    1, r"§4.4e 波形因数（2）")
add(r"""原例：B = 5 kHz、δf à −60 dB = 25 kHz → S = 500/25 = <b>20 %</b>，""",
    r"""原例：\(B = 5\) kHz、\(\delta f\ \text{à}\ -60\ \text{dB} = 25\) kHz → \(S = 500/25 =\) <b>20 %</b>，""",
    1, r"§4.4e 选择性算例")
add(r"""<code>Bp = B × √(p − 1)</code>""",
    r"""<code>\(B_p = B \times \sqrt{p - 1}\)</code>""",
    1, r"§4.4e 带宽 Bp 与 B 的关系")
add(r"""因为 δf à −60 dB = √(1 000 000 − 1) × B ≈ 1000 × B。""",
    r"""因为 \(\delta f\ \text{à}\ -60\ \text{dB} = \sqrt{1\,000\,000 - 1} \times B \approx 1000 \times B\)。""",
    1, r"§4.4e 单节 RLC 波形因数")
add(r"""①求谐振阻抗（bouchon / 并联）→ Z(kΩ) = L(µH) ÷ R(kΩ) ÷ C(pF)；""",
    r"""①求谐振阻抗（bouchon / 并联）→ \(Z\,(\text{k}\Omega) = L\,(\mu\text{H}) \div R\,(\text{k}\Omega) \div C\,(\text{pF})\)；""",
    1, r"§4.4 tips 步①")
add(r"""②求 Q → Q = √[L(µH)/C(pF)] ÷ R(kΩ)；""",
    r"""②求 Q → \(Q = \sqrt{L\,(\mu\text{H})/C\,(\text{pF})} \div R\,(\text{k}\Omega)\)；""",
    1, r"§4.4 tips 步②")
add(r"""④求选择性 → S = (B × 100) / δf à −60 dB。""",
    r"""④求选择性 → \(S = \dfrac{B \times 100}{\delta f\ \text{à}\ -60\ \text{dB}}\)。""",
    1, r"§4.4 tips 步④")

# ---------------------------------------------------------------- 4.5
add(r"""合起来只等效为一个电容 C_T（这正是""",
    r"""合起来只等效为一个电容 \(C_T\)（这正是""",
    1, r"§4.5 等效电容 C_T")

# ---------------------------------------------------------------- 4.6
add(r"""（谐振时 X_L = X_C）""",
    r"""（谐振时 \(X_L = X_C\)）""",
    1, r"§4.6a 前提")
add(r"""<div class="formula">f = 1/(2π√(LC))""",
    r"""<div class="formula">\[f = \dfrac{1}{2\pi\sqrt{LC}}\]""",
    1, r"§4.6a 汤姆逊公式（只有公式）")
add(r"""f² = 1/(4π²LC)""",
    r"""\(f^2 = \dfrac{1}{4\pi^2 LC}\)""",
    1, r"§4.6a 两边平方")
add(r"""C = 1 / (4π² f² L)""",
    r"""\[C = \dfrac{1}{4\pi^2 f^2 L}\]""",
    1, r"§4.6a 由 f、L 求 C（只有公式）")
add(r"""L = 1 / (4π² f² C)""",
    r"""\[L = \dfrac{1}{4\pi^2 f^2 C}\]""",
    1, r"§4.6a 由 f、C 求 L（只有公式）")
add(r"""简化式：C(pF) = 25 330 / f²(MHz) / L(µH)""",
    r"""简化式：\(C\,(\text{pF}) = \dfrac{25\,330}{f^2\,(\text{MHz}) \times L\,(\mu\text{H})}\)""",
    1, r"§4.6a C 简化式")
add(r"""L(µH) = 25 330 / f²(MHz) / C(pF)""",
    r"""\(L\,(\mu\text{H}) = \dfrac{25\,330}{f^2\,(\text{MHz}) \times C\,(\text{pF})}\)""",
    1, r"§4.6a L 简化式")
add(r"""（式中 25 330 = 10 000/4π² ≈ 159²）""",
    r"""（式中 \(25\,330 = 10\,000/4\pi^2 \approx 159^2\)）""",
    1, r"§4.6a 常数来源")
add(r"""谐振角频率：ω = 1 / √(L × C)""",
    r"""谐振角频率：\(\omega = \dfrac{1}{\sqrt{L \times C}}\)""",
    1, r"§4.6a 谐振角频率")
add(r"""谐振电抗：X_L = X_C = √(L / C)""",
    r"""谐振电抗：\(X_L = X_C = \sqrt{L/C}\)""",
    1, r"§4.6a 谐振电抗")
add(r"""（也可用 X_L = 6,28 × f(MHz) × L(µH)、X_C = 159 / f(MHz) / C(nF)）""",
    r"""（也可用 \(X_L = 6{,}28 \times f\,(\text{MHz}) \times L\,(\mu\text{H})\)、\(X_C = \dfrac{159}{f\,(\text{MHz}) \times C\,(\text{nF})}\)）""",
    1, r"§4.6a 另两种写法")
add(r"""原文用 §4.4a 的 bouchon 电路（f = 3,183 MHz、L = 25 µH、C = 100 pF）验证：C = 1/(4π²f²L) = 100 pF（简化式 25 330 ÷ 3,183² ÷ 25 = 100 pF）；""",
    r"""原文用 §4.4a 的 bouchon 电路（\(f = 3{,}183\) MHz、\(L = 25\) µH、\(C = 100\) pF）验证：\(C = \dfrac{1}{4\pi^2 f^2 L} = 100\) pF（简化式 25 330 ÷ 3,183² ÷ 25 = 100 pF）；""",
    1, r"§4.6a 数值验证（C）")
add(r"""L = 1/(4π²f²C) = 25 µH；""",
    r"""\(L = \dfrac{1}{4\pi^2 f^2 C} = 25\) µH；""",
    1, r"§4.6a 数值验证（L）")
add(r"""ω = 1/√(25×10⁻⁶ × 100×10⁻¹²) = 20×10⁶ rad/s（与 2πf = 6,28 × 3,183×10⁶ ≈ 20×10⁶ rad/s 相符）；""",
    r"""\(\omega = \dfrac{1}{\sqrt{25\times10^{-6} \times 100\times10^{-12}}} = 20\times10^{6}\) rad/s（与 \(2\pi f = 6{,}28 \times 3{,}183\times10^{6} \approx 20\times10^{6}\) rad/s 相符）；""",
    1, r"§4.6a 数值验证（ω）")
add(r"""X_L = √(25×10⁻⁶ / 100×10⁻¹²) = 500 Ω。""",
    r"""\(X_L = \sqrt{\dfrac{25\times10^{-6}}{100\times10^{-12}}} = 500\) Ω。""",
    1, r"§4.6a 数值验证（X_L）")
add(r"""Z_bouchon = X_L² / R = X_C² / R""",
    r"""\[Z_{\text{bouchon}} = \dfrac{X_L^2}{R} = \dfrac{X_C^2}{R}\]""",
    1, r"§4.6b Z（只有公式）")
add(r"""Q_bouchon = X_L / R = X_C / R""",
    r"""\(Q_{\text{bouchon}} = \dfrac{X_L}{R} = \dfrac{X_C}{R}\)""",
    1, r"§4.6b Q")
add(r"""（与 Q_série 公式相同，两种电路 Q 相同）""",
    r"""（与 \(Q_{\text{série}}\) 公式相同，两种电路 Q 相同）""",
    1, r"§4.6b 括注")
add(r"""Z_bouchon(kΩ) = R_parallèle(kΩ) = √[ L(µH) / C(pF) ] × Q""",
    r"""\[Z_{\text{bouchon}}\,(\text{k}\Omega) = R_{\text{parallèle}}\,(\text{k}\Omega) = \sqrt{\dfrac{L\,(\mu\text{H})}{C\,(\text{pF})}} \times Q\]""",
    1, r"§4.6b Z 与 Q 的关系（只有公式）")
add(r"""R_bouchon(kΩ) = R_série(kΩ)""",
    r"""\(R_{\text{bouchon}}\,(\text{k}\Omega) = R_{\text{série}}\,(\text{k}\Omega)\)""",
    1, r"§4.6b R 与 Q 的关系（左半）")
add(r"""= √[ L(µH) / C(pF) ] ÷ Q""",
    r"""\(= \sqrt{\dfrac{L\,(\mu\text{H})}{C\,(\text{pF})}} \div Q\)""",
    1, r"§4.6b R 与 Q 的关系（右半）")
add(r"""Z_bouchon = R_parallèle = R_bouchon × Q²""",
    r"""\[Z_{\text{bouchon}} = R_{\text{parallèle}} = R_{\text{bouchon}} \times Q^2\]""",
    1, r"§4.6b 三者关系（只有公式）")
add(r"""原例（L = 25 µH、C = 100 pF、R = 20 Ω、Q = 25）：""",
    r"""原例（\(L = 25\) µH、\(C = 100\) pF、\(R = 20\) Ω、\(Q = 25\)）：""",
    1, r"§4.6b 原例数据")
add(r"""Z = X_L²/R = 500²/20 = 12 500 Ω；""",
    r"""\(Z = X_L^2/R = 500^2/20 = 12\,500\) Ω；""",
    1, r"§4.6b 原例 Z")
add(r"""√(L/C) = √(25/100) = 0,5 kΩ → Z = 0,5 × 25 = 12,5 kΩ，""",
    r"""\(\sqrt{L/C} = \sqrt{25/100} = 0{,}5\) kΩ → \(Z = 0{,}5 \times 25 = 12{,}5\) kΩ，""",
    1, r"§4.6b 原例 √(L/C) 与 Z")
add(r"""R = 0,5 ÷ 25 = 0,02 kΩ = 20 Ω；""",
    r"""\(R = 0{,}5 \div 25 = 0{,}02\ \text{k}\Omega = 20\ \Omega\)；""",
    1, r"§4.6b 原例 R")
add(r"""由 Q = f_o / B 得 Q""",
    r"""由 \(Q = \dfrac{f_o}{B}\) 得 Q""",
    1, r"§4.6b 由带宽反推 Q")
add(r"""先算中间值 √[L(µH)/C(pF)]（单位 kΩ）""",
    r"""先算中间值 \(\sqrt{L\,(\mu\text{H})/C\,(\text{pF})}\)（单位 kΩ）""",
    1, r"§4.6 tips 中间值")
add(r"""例：L = 25 µH、C = 400 pF、Q = 75 → √(25/400) = 0,25 kΩ → Z = 0,25 × 75 = 18,75 kΩ = <b>18 750 Ω</b>。""",
    r"""例：\(L = 25\) µH、\(C = 400\) pF、\(Q = 75\) → \(\sqrt{25/400} = 0{,}25\) kΩ → \(Z = 0{,}25 \times 75 = 18{,}75\) kΩ = <b>18 750 Ω</b>。""",
    1, r"§4.6 tips 算例")
add(r"""（bouchon）电路：L = 25 µH、C = 400 pF、Q = 75，谐振时的阻抗是多少？""",
    r"""（bouchon）电路：\(L = 25\) µH、\(C = 400\) pF、\(Q = 75\)，谐振时的阻抗是多少？""",
    1, r"§4.6 真题中文题干")
add(r"""图中放大器：输出电压 Us = 8 V、增益 12 dB，输入电压 Ue 是多少？""",
    r"""图中放大器：输出电压 \(U_s = 8\) V、增益 12 dB，输入电压 \(U_e\) 是多少？""",
    1, r"§4.1 真题中文题干")


# ---------------------------------------------------------------- checks
def check(path=r"/home/thelia/Documents/radioamateur-fr/manuel-zh.html"):
    text = open(path, encoding="utf-8").read()
    t = text
    bad = []
    for i, p in enumerate(P, 1):
        o, n, c = p["old"], p["new"], p["count"]
        if "$" in n:
            bad.append("#%d dollar in new" % i)
        if "\n" in o or "\n" in n:
            bad.append("#%d newline" % i)
        if n.count("\\(") != n.count("\\)"):
            bad.append("#%d unbalanced \\( \\)  %s" % (i, repr(n)))
        if n.count("\\[") != n.count("\\]"):
            bad.append("#%d unbalanced \\[ \\]  %s" % (i, repr(n)))
        got = t.count(o)
        if got != c:
            bad.append("#%d GOT %d WANT %d\n    old=%s" % (i, got, c, repr(o)))
            k = 0
            pre = o[:14]
            while True:
                j = text.find(pre, k)
                if j < 0:
                    break
                bad.append("    ctx: %s" % repr(text[max(0, j - 25):j + len(o) + 25]))
                k = j + 1
        else:
            t = t.replace(o, n)
    return bad, t


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "json":
        with open("pairs-T34-section.json", "w", encoding="utf-8") as fh:
            json.dump({"section": "T3 §3.1–§3.7 变压器/电池/测量 + T4 §4.1–§4.6 分贝与滤波",
                       "pairs": P}, fh, ensure_ascii=False, indent=1)
        print("wrote pairs-T34-section.json  (%d pairs)" % len(P))
    else:
        bad, t = check()
        print("total pairs: %d" % len(P))
        for b in bad:
            print(b)
        print("problems: %d" % len(bad))
