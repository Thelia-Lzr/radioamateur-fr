#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate pairs-T1011-section.json (T10 §10.1-§10.4 + T11 §11.1-§11.7).

Simulates apply_pairs.py's algorithm (sequential str.replace, counting
occurrences on the current text) so that every recorded `count` is exactly
what the tool will see, and refuses to emit a pair whose tag multiset would
change or whose `new` contains a '$'.
"""
import json
import sys

import apply_pairs as ap

TARGET = "manuel-zh.html"
OUT = "pairs-T1011-section.json"

# (old, new, note)
P = []


def add(old, new, note=""):
    P.append((old, new, note))


# ---------------------------------------------------------------- T10 heads
# TOC entry + h3 title of §10.3 both carry the symbol rho
add("：ρ、TOS、ROS 与天调",
    "：\\(\\rho\\)、TOS、ROS 与天调",
    "目录 §10.3 条目 + 正文 h3 标题（同一串两次）")

# ---------------------------------------------------------------- §10.1
add("为 √(L/C)（见 §10.2a）",
    "为 \\(\\sqrt{\\dfrac{L}{C}}\\)（见 §10.2a）",
    "§10.1 正文：特性阻抗 √(L/C)")

add("<div class=\"formula\">Z ligne (Ω) = √( L(H/m) / C(F/m) )</div>",
    "<div class=\"formula\">\\[Z_{\\text{ligne}}\\,(\\Omega) = "
    "\\sqrt{\\dfrac{L\\,(\\text{H/m})}{C\\,(\\text{F/m})}}\\]</div>",
    "§10.1 展示式：线路特性阻抗")

add("<code>U = √(P × R)</code>",
    "<code>\\(U = \\sqrt{P \\times R}\\)</code>",
    "§10.1 tips：有效值公式")

add("<code>Ucrête = √(2 × P × R)</code>",
    "<code>\\(U_{\\text{crête}} = \\sqrt{2 \\times P \\times R}\\)</code>",
    "§10.1 tips：峰值电压公式")

add("20 W 加到 75 Ω 上：√(20 × 75) = 38,7 V 是有效值，峰值 = 38,7 × 1,414 = <b>54,7 V</b>。",
    "20 W 加到 75 Ω 上：\\(\\sqrt{20 \\times 75} = 38{,}7\\) V 是有效值，"
    "峰值 \\(= 38{,}7 \\times 1{,}414 =\\) <b>54,7 V</b>。",
    "§10.1 tips：峰值电压算例")

add("衰减 = 10·lg(200/100) ≈ 3 dB，折合每米约 3/33 ≈ <b>0,09 dB/m</b>。",
    "衰减 \\(= 10 \\cdot \\lg(200/100) \\approx 3\\) dB，"
    "折合每米约 \\(3/33 \\approx\\) <b>0,09 dB/m</b>。",
    "§10.1 tips：线性衰减算例")

add("（图中 C = 20 pF/m、L = 50 nH/m）这条同轴线的特性阻抗是多少？",
    "（图中 \\(C = 20\\ \\text{pF/m}\\)、\\(L = 50\\ \\text{nH/m}\\)）这条同轴线的特性阻抗是多少？",
    "§10.2 真题（中文题干）参数")

add("（图中同轴电缆 d = 3 mm、D = 10 mm）",
    "（图中同轴电缆 \\(d = 3\\) mm、\\(D = 10\\) mm）",
    "§10.2 真题（中文题干）参数")

add("（图中同轴电缆 D = 10、d = 2）",
    "（图中同轴电缆 \\(D = 10\\)、\\(d = 2\\)）",
    "§10.2 真题（中文题干）参数")

# ---------------------------------------------------------------- §10.2
add("<div class=\"formula\">Z ligne (Ω) = √(ωL / ωC) = √( L(H/m) / C(F/m) )</div>",
    "<div class=\"formula\">\\[Z_{\\text{ligne}}\\,(\\Omega) = "
    "\\sqrt{\\dfrac{\\omega L}{\\omega C}} = \\sqrt{\\dfrac{L\\,(\\text{H/m})}{C\\,(\\text{F/m})}}\\]</div>",
    "§10.2 展示式：Z = √(ωL/ωC) = √(L/C)")

add("传播介质阻抗 Z milieu = √(ZL × ZC)。",
    "传播介质阻抗 \\(Z_{\\text{milieu}} = \\sqrt{Z_L \\times Z_C}\\)。",
    "§10.2：介质阻抗")

add("原文例题：某电缆 L = 0,5 µH/m、C = 200 pF/m，则 Z = √(0,5.10⁻⁶ / 200.10⁻¹²) "
    "= √2500 = <b>50 Ω</b>；真题给出 C = 20 pF/m、L = 50 nH/m，同样算得 50 Ω。",
    "原文例题：某电缆 \\(L = 0{,}5\\ \\mu\\text{H/m}\\)、\\(C = 200\\ \\text{pF/m}\\)，"
    "则 \\(Z = \\sqrt{\\dfrac{0{,}5 \\cdot 10^{-6}}{200 \\cdot 10^{-12}}} = \\sqrt{2500} =\\) "
    "<b>50 Ω</b>；真题给出 \\(C = 20\\ \\text{pF/m}\\)、\\(L = 50\\ \\text{nH/m}\\)，"
    "同样算得 \\(50\\ \\Omega\\)。",
    "§10.2 原文例题：由 L、C 求 Zc")

add("<div class=\"formula\">Z (Ω) = 138,2 × log(D/d) / √ε      （138,2 = 60 × ln(10)）</div>",
    "<div class=\"formula\">\\[Z\\,(\\Omega) = \\dfrac{138{,}2 \\times \\log(D/d)}"
    "{\\sqrt{\\varepsilon}}\\]      （\\(138{,}2 = 60 \\times \\ln(10)\\)）</div>",
    "§10.2 展示式：同轴电缆 Z 的估算式")

# 注意：文末「核实附录」里有一份近似的副本（分隔符是换行而不是空格），
# 下列各 pair 的 old 都跨过正文里的空格分隔符，因此只落在本节正文里。
add("并按空气（ε = 1）作答：Z = 138 · log₁₀(D/d)。 · 题 20360："
    "Z = 138 · log₁₀(10/3) = 138 × 0,5229 ≈ 72 Ω（答案 D）。 · 题 20385："
    "Z = 138 · log₁₀(10/2) = 138 × 0,699 ≈ 96 Ω（答案 C）。 "
    "若按教材常用的 PE（ε = 2,3）算，题 20360 得 (138/√2,3) × 0,5229 ≈ 48 Ω，"
    "不在选项中，可见「未注明介质」时命题人的默认口径就是空气。 "
    "带介质的一般式（题库题 20787 给出实例：ε = 4、D/d = 5 ⇒ Z = 48 Ω）：",
    "并按空气（\\(\\varepsilon = 1\\)）作答：\\(Z = 138 \\cdot \\log_{10}(D/d)\\)。 · "
    "题 20360：\\(Z = 138 \\cdot \\log_{10}(10/3) = 138 \\times 0{,}5229 \\approx 72\\ \\Omega\\)"
    "（答案 D）。 · 题 20385：\\(Z = 138 \\cdot \\log_{10}(10/2) = 138 \\times 0{,}699 "
    "\\approx 96\\ \\Omega\\)（答案 C）。 若按教材常用的 PE（\\(\\varepsilon = 2{,}3\\)）算，"
    "题 20360 得 \\((138/\\sqrt{2{,}3}) \\times 0{,}5229 \\approx 48\\ \\Omega\\)，"
    "不在选项中，可见「未注明介质」时命题人的默认口径就是空气。 "
    "带介质的一般式（题库题 20787 给出实例：\\(\\varepsilon = 4\\)、\\(D/d = 5\\) ⇒ "
    "\\(Z = 48\\ \\Omega\\)）：",
    "§10.2 warn 注：空气介质公式 + 两个算例 + 带介质一般式（整段，锚定正文）")

add("，其中 60 · ln(10) = 138,2。 作答口径：题面未注明 ε 时一律取 ε = 1（空气）。",
    "，其中 \\(60 \\cdot \\ln(10) = 138{,}2\\)。 作答口径：题面未注明 ε 时一律取 "
    "\\(\\varepsilon = 1\\)（空气）。",
    "§10.2 warn 注：138,2 的来历 + 作答口径")

add("（电视天线）。 原文口径：§10.2b 只给出 \\(Z = \\dfrac{138}{\\sqrt{\\varepsilon}} "
    "\\cdot \\log_{10}(D/d)\\) 的来历（60 · ln(10) = 138,2）、损耗来源（R2 集肤效应、"
    "R1 介质)与速度系数，以及唯一算例「PE 介质、编织网/内导体直径比 3,5 时 Z = 50 Ω」"
    "（(138/√2,3) × log₁₀3,5 ≈ 49,5 Ω ≈ 50 Ω）",
    "（电视天线）。 原文口径：§10.2b 只给出 \\(Z = \\dfrac{138}{\\sqrt{\\varepsilon}} "
    "\\cdot \\log_{10}(D/d)\\) 的来历（\\(60 \\cdot \\ln(10) = 138{,}2\\)）、损耗来源"
    "（R2 集肤效应、R1 介质)与速度系数，以及唯一算例「PE 介质、编织网/内导体直径比 "
    "3,5 时 Z = 50 Ω」（\\((138/\\sqrt{2{,}3}) \\times \\log_{10} 3{,}5 \\approx "
    "49{,}5\\ \\Omega \\approx 50\\ \\Omega\\)）",
    "§10.2 note 注：原文口径段（锚定正文，避开文末附录副本）")

add("倍率由介质决定，v = 1/√ε，以空气中速度的",
    "倍率由介质决定，\\(v = \\dfrac{1}{\\sqrt{\\varepsilon}}\\)，以空气中速度的",
    "§10.2：速度系数 v = 1/√ε")

add("<td>66 %（= 1/√2,3）</td>",
    "<td>66 %（\\(= 1/\\sqrt{2{,}3}\\)）</td>",
    "§10.2 速度系数表：PE 行")

add("计算 λ/4、λ/2 线的<b>物理长度</b>时必须乘上速度系数。",
    "计算 \\(\\lambda/4\\)、\\(\\lambda/2\\) 线的<b>物理长度</b>时必须乘上速度系数。",
    "§10.2：λ/4、λ/2")

add("的电缆，λ/4 长度 = (c/f)/4 × 0,66 = (300/28)/4 × 0,66 ≈ <b>1,77 m</b>",
    "的电缆，\\(\\lambda/4\\) 长度 \\(= \\dfrac{c/f}{4} \\times 0{,}66 = "
    "\\dfrac{300/28}{4} \\times 0{,}66 \\approx\\) <b>1,77 m</b>",
    "§10.2：λ/4 物理长度算例")

add("（用一段 75 Ω 的 λ/4 同轴线把 100 Ω 天线变到接近 50 Ω）",
    "（用一段 75 Ω 的 \\(\\lambda/4\\) 同轴线把 100 Ω 天线变到接近 50 Ω）",
    "§10.2：75 Ω 匹配线")

# ---------------------------------------------------------------- §10.3
add("相距 <b>λ/4</b>，整个现象每隔 <b>λ/2</b> 重复一次",
    "相距 <b>\\(\\lambda/4\\)</b>，整个现象每隔 <b>\\(\\lambda/2\\)</b> 重复一次",
    "§10.3：驻波极值间距 λ/4、周期 λ/2")

add("<b>1）反射系数 ρ</b>",
    "<b>1）反射系数 \\(\\rho\\)</b>",
    "§10.3：反射系数标题")

add("因为 U = √(P·R)；",
    "因为 \\(U = \\sqrt{P \\cdot R}\\)；",
    "§10.3：U = √(P·R)")

add("等于 100 ρ；反射功率等于发射功率乘以 ρ 的平方。",
    "等于 \\(100\\,\\rho\\)；反射功率等于发射功率乘以 \\(\\rho\\) 的平方。",
    "§10.3：TOS = 100ρ、反射功率 ∝ ρ²")

add("ρ = U R / U E = (U maxi – U mini) / (U maxi + U mini)",
    "\\[\\rho = \\dfrac{U_R}{U_E} = "
    "\\dfrac{U_{maxi} - U_{mini}}{U_{maxi} + U_{mini}}\\]",
    "§10.3 展示式：反射系数（电压式）")

add("ρ = I R / I E = (I maxi – I mini) / (I maxi + I mini)",
    "\\[\\rho = \\dfrac{I_R}{I_E} = \\dfrac{I_{maxi} - I_{mini}}{I_{maxi} + I_{mini}}\\]",
    "§10.3 展示式：反射系数（电流式）")

add("ρ = √(P R / P E)        TOS (%) = 100 ρ        P réfléchie = P émise × ρ²",
    "\\[\\rho = \\sqrt{\\dfrac{P_R}{P_E}}\\qquad \\text{TOS}\\,(\\%) = 100\\,\\rho "
    "\\qquad P_{\\text{réfléchie}} = P_{\\text{émise}} \\times \\rho^2\\]",
    "§10.3 展示式：ρ（功率式）、TOS、反射功率")

add("<div class=\"formula\">ROS (rapport / 1) = Z plus forte (Ω) / Z plus faible (Ω) "
    "= U maxi / U mini = I maxi / I mini</div>",
    "<div class=\"formula\">\\[\\text{ROS}\\;(\\text{rapport}/1) = "
    "\\dfrac{Z_{\\text{plus forte}}\\,(\\Omega)}{Z_{\\text{plus faible}}\\,(\\Omega)} = "
    "\\dfrac{U_{maxi}}{U_{mini}} = \\dfrac{I_{maxi}}{I_{mini}}\\]</div>",
    "§10.3 展示式：驻波比 ROS")

add("<code>100 × (Pr / Pe)</code>",
    "<code>\\(100 \\times (P_r / P_e)\\)</code>",
    "§10.3：反射功率百分比的 <code> 定义式")

add("<div class=\"formula\">ROS = (1 + ρ) / (1 – ρ)            "
    "ρ = (ROS – 1) / (ROS + 1)</div>",
    "<div class=\"formula\">\\[\\text{ROS} = \\dfrac{1 + \\rho}{1 - \\rho}\\qquad "
    "\\rho = \\dfrac{\\text{ROS} - 1}{\\text{ROS} + 1}\\]</div>",
    "§10.3 展示式：ROS 与 ρ 互换")

add("<td>反射系数 ρ</td>",
    "<td>反射系数 \\(\\rho\\)</td>",
    "§10.3 表格：反射系数行首")

add("<li>测到 UE = 100 V、UR = 4 V ⇒ ρ = 4/100 = 0,04，TOS = 4 %。</li>",
    "<li>测到 \\(U_E = 100\\) V、\\(U_R = 4\\) V ⇒ \\(\\rho = 4/100 = 0{,}04\\)，"
    "\\(\\text{TOS} = 4\\) %。</li>",
    "§10.3 原文例题 1")

add("<li>50 Ω 同轴接 75 Ω 的半波振子（doublet λ/2）⇒ ROS = 75/50 = 1,5/1；"
    "接 36 Ω 的 λ/4 垂直天线 ⇒ ROS = 50/36 = 1,389/1。</li>",
    "<li>50 Ω 同轴接 75 Ω 的半波振子（doublet \\(\\lambda/2\\)）⇒ "
    "\\(\\text{ROS} = 75/50 = 1{,}5/1\\)；接 36 Ω 的 \\(\\lambda/4\\) 垂直天线 ⇒ "
    "\\(\\text{ROS} = 50/36 = 1{,}389/1\\)。</li>",
    "§10.3 原文例题 2")

add("<li>线上 U maxi / U mini = 10/8（即 I maxi / I mini = 0,2/0,16）⇒ ROS = 1,25/1；"
    "ρ = (10 – 8)/(10 + 8) = 0,111，TOS = 11 %。</li>",
    "<li>线上 \\(U_{maxi} / U_{mini} = 10/8\\)（即 \\(I_{maxi} / I_{mini} = 0{,}2/0{,}16\\)）⇒ "
    "\\(\\text{ROS} = 1{,}25/1\\)；\\(\\rho = (10 - 8)/(10 + 8) = 0{,}111\\)，"
    "\\(\\text{TOS} = 11\\) %。</li>",
    "§10.3 原文例题 3")

add("<li>TOS = 33 % ⇒ ρ = 0,33 ⇒ ROS = (1 + 0,33)/(1 – 0,33) = 2/1；反过来 ROS = 2/1 ⇒ "
    "ρ = (2 – 1)/(2 + 1) = 1/3 = 0,33，TOS = 33 %。</li>",
    "<li>\\(\\text{TOS} = 33\\) % ⇒ \\(\\rho = 0{,}33\\) ⇒ "
    "\\(\\text{ROS} = (1 + 0{,}33)/(1 - 0{,}33) = 2/1\\)；反过来 \\(\\text{ROS} = 2/1\\) ⇒ "
    "\\(\\rho = (2 - 1)/(2 + 1) = 1/3 = 0{,}33\\)，\\(\\text{TOS} = 33\\) %。</li>",
    "§10.3 原文例题 4（互换）")

add("发生器送出 9 V、反射 1 V（负载 40 Ω 对 50 Ω，ROS = 1,25/1）⇒ 反射功率比 ρ² = 1,23 %"
    "（= 1/9²）。Pe = U²/R = 9²/50 = 1,62 W，P charge = U × I = 8 × 0,2 = 1,6 W "
    "= Pe × (1 – ρ²)。",
    "发生器送出 9 V、反射 1 V（负载 40 Ω 对 50 Ω，\\(\\text{ROS} = 1{,}25/1\\)）⇒ "
    "反射功率比 \\(\\rho^2 = 1{,}23\\) %（\\(= 1/9^2\\)）。"
    "\\(P_e = U^2/R = 9^2/50 = 1{,}62\\) W，"
    "\\(P_{\\text{charge}} = U \\times I = 8 \\times 0{,}2 = 1{,}6\\) W "
    "\\(= P_e \\times (1 - \\rho^2)\\)。",
    "§10.3 原文例题 5")

add("①给出 Pi、Pr 时先算 ρ = √(Pr / Pi)，再套 ROS = (1 + ρ)/(1 – ρ)"
    "（如 Pi = 4 W、Pr = 1 W ⇒ ρ = 0,5 ⇒ ROS = <b>3</b>）。",
    "①给出 \\(P_i\\)、\\(P_r\\) 时先算 \\(\\rho = \\sqrt{P_r / P_i}\\)，再套 "
    "\\(\\text{ROS} = (1 + \\rho)/(1 - \\rho)\\)（如 \\(P_i = 4\\) W、\\(P_r = 1\\) W ⇒ "
    "\\(\\rho = 0{,}5\\) ⇒ \\(\\text{ROS} =\\) <b>3</b>）。",
    "§10.3 tips ①：由 Pi、Pr 求 ROS")

add("②给出两端阻抗时 ROS = 大 / 小（50 Ω 与 75 Ω ⇒ <b>1,5</b>）。",
    "②给出两端阻抗时 \\(\\text{ROS} =\\) 大 / 小（50 Ω 与 75 Ω ⇒ <b>1,5</b>）。",
    "§10.3 tips ②：ROS = 大/小")

add("（TOS = 100 ρ，理想失配为零）",
    "（\\(\\text{TOS} = 100\\,\\rho\\)，理想失配为零）",
    "§10.3 tips ③：TOS 定义")

add("让你挑 ROS = 1,5 的那张",
    "让你挑 \\(\\text{ROS} = 1{,}5\\) 的那张",
    "§10.3 tips ④")

add("选 12/8 = 1,5 的那一张（该图 0,24/0,16 也等于 1,5）。",
    "选 \\(12/8 = 1{,}5\\) 的那一张（该图 \\(0{,}24/0{,}16\\) 也等于 \\(1{,}5\\)）。",
    "§10.3 tips ④：波形比")

add("（图中入射功率 Pi = 4 W、反射功率 Pr = 1 W）驻波比（ROS）是多少？",
    "（图中入射功率 \\(P_i = 4\\) W、反射功率 \\(P_r = 1\\) W）驻波比（ROS）是多少？",
    "§10.3 真题（中文题干）参数")

add("（图中 Ze = 50 Ω、Za = 75 Ω）驻波比（ROS）是多少？",
    "（图中 \\(Z_e = 50\\ \\Omega\\)、\\(Z_a = 75\\ \\Omega\\)）驻波比（ROS）是多少？",
    "§10.3 真题（中文题干）参数")

add("哪一张表示驻波比 ROS = 1,5？",
    "哪一张表示驻波比 \\(\\text{ROS} = 1{,}5\\)？",
    "§10.3 真题（中文题干）参数")

# ---------------------------------------------------------------- §10.4
add("下面用 Zc = 电缆阻抗、Ze = 输入阻抗、Zs = 输出阻抗：",
    "下面用 \\(Z_c =\\) 电缆阻抗、\\(Z_e =\\) 输入阻抗、\\(Z_s =\\) 输出阻抗：",
    "§10.4：Zc / Ze / Zs 约定")

add("<li><b>λ/4 的偶数倍（也就是每半个波长）</b>：Ze = Zs，阻抗被原样\"复制\"过去；</li>",
    "<li><b>\\(\\lambda/4\\) 的偶数倍（也就是每半个波长）</b>：\\(Z_e = Z_s\\)，"
    "阻抗被原样\"复制\"过去；</li>",
    "§10.4：λ/4 偶数倍")

add("<li><b>λ/4 的奇数倍</b>：Zc² = Ze × Zs，即</li>",
    "<li><b>\\(\\lambda/4\\) 的奇数倍</b>：\\(Z_c^2 = Z_e \\times Z_s\\)，即</li>",
    "§10.4：λ/4 奇数倍")

add("<div class=\"formula\">Zc = √( Ze × Zs )</div>",
    "<div class=\"formula\">\\[Z_c = \\sqrt{Z_e \\times Z_s}\\]</div>",
    "§10.4 展示式：λ/4 线与两端阻抗")

add("<p>原文例题：要把 Ze = 50 Ω 与 Zs = 100 Ω 匹配，λ/4 电缆的阻抗应为 "
    "Zc = √(50 × 100) = √5000 = <b>70,7 Ω</b>。</p>",
    "<p>原文例题：要把 \\(Z_e = 50\\) Ω 与 \\(Z_s = 100\\) Ω 匹配，\\(\\lambda/4\\) "
    "电缆的阻抗应为 \\(Z_c = \\sqrt{50 \\times 100} = \\sqrt{5000} =\\) <b>70,7 Ω</b>。</p>",
    "§10.4 原文例题 1：Zc = √(Ze·Zs)")

add("一段 75 Ω 的 λ/4 同轴能把 100 Ω 的天线变到接近 50 Ω——此时电缆输入端的阻抗 "
    "Ze = Zc²/Zs = 75²/100 = <b>56,25 Ω</b>，相对 50 Ω 只有 1,125/1 的 ROS，"
    "而若直接用 50 Ω 电缆则是 2/1（= 100/50）。",
    "一段 75 Ω 的 \\(\\lambda/4\\) 同轴能把 100 Ω 的天线变到接近 50 Ω——此时电缆输入端的阻抗 "
    "\\(Z_e = Z_c^2/Z_s = 75^2/100 =\\) <b>56,25 Ω</b>，相对 50 Ω 只有 \\(1{,}125/1\\) 的 ROS，"
    "而若直接用 50 Ω 电缆则是 \\(2/1\\)（\\(= 100/50\\)）。",
    "§10.4 原文例题 2 前半")

add("电缆输出端的阻抗 Zs = Zc²/Ze = 75²/50 = <b>112,5 Ω</b>，ROS 同样是 1,125/1。",
    "电缆输出端的阻抗 \\(Z_s = Z_c^2/Z_e = 75^2/50 =\\) <b>112,5 Ω</b>，"
    "ROS 同样是 \\(1{,}125/1\\)。",
    "§10.4 原文例题 2 后半")

add("把 λ/4 或 λ/2 的同轴电缆段",
    "把 \\(\\lambda/4\\) 或 \\(\\lambda/2\\) 的同轴电缆段",
    "§10.4：λ/4、λ/2 段作滤波器")

add("到 λ/4 处相当于串联 LC 电路（阻抗为零）",
    "到 \\(\\lambda/4\\) 处相当于串联 LC 电路（阻抗为零）",
    "§10.4：开路线特性")

add("到 λ/2 处相当于并联谐振（阻抗无穷大）",
    "到 \\(\\lambda/2\\) 处相当于并联谐振（阻抗无穷大）",
    "§10.4：开路线特性")

add("到 3λ/4 又回到容性并重新为零",
    "到 \\(3\\lambda/4\\) 又回到容性并重新为零",
    "§10.4：开路线特性")

add("正好错开 λ/4：",
    "正好错开 \\(\\lambda/4\\)：",
    "§10.4：闭合线特性")

add("在到达 λ/4 之前就升高，在 λ/4 处为无穷大",
    "在到达 \\(\\lambda/4\\) 之前就升高，在 \\(\\lambda/4\\) 处为无穷大",
    "§10.4：闭合线特性")

add("在 λ/2 处为零。",
    "在 \\(\\lambda/2\\) 处为零。",
    "§10.4：闭合线特性")

add("377 Ω（= 120π，由 µ0 与 ε0 得出；介质阻抗 Z milieu = √(ZL × ZC) = √(L/C)）",
    "377 Ω（\\(= 120\\pi\\)，由 \\(\\mu_0\\) 与 \\(\\varepsilon_0\\) 得出；介质阻抗 "
    "\\(Z_{\\text{milieu}} = \\sqrt{Z_L \\times Z_C} = \\sqrt{\\dfrac{L}{C}}\\)）",
    "§10.4：真空阻抗与介质阻抗")

add("①看到 λ/4 线两端给出阻抗，直接 Zc = √(Ze × Zs)（300 Ω 与 50 Ω ⇒ √15000 ≈ <b>122 Ω</b>）。",
    "①看到 \\(\\lambda/4\\) 线两端给出阻抗，直接 \\(Z_c = \\sqrt{Z_e \\times Z_s}\\)"
    "（300 Ω 与 50 Ω ⇒ \\(\\sqrt{15000} \\approx\\) <b>122 Ω</b>）。",
    "§10.4 tips ①")

add("②看到 λ/2 线，输出阻抗 = 输入阻抗",
    "②看到 \\(\\lambda/2\\) 线，输出阻抗 = 输入阻抗",
    "§10.4 tips ②")

add("③问\"哪一段电缆是 28 MHz 上的 λ/4\"：λ/4 = (300/28)/4 ≈ 2,68 m，"
    "再乘缩短系数 0,66，得约 1,77 m。",
    "③问\"哪一段电缆是 28 MHz 上的 \\(\\lambda/4\\)\"：\\(\\lambda/4 = (300/28)/4 "
    "\\approx 2{,}68\\) m，再乘缩短系数 0,66，得约 1,77 m。",
    "§10.4 tips ③")

add("（图中 λ/4 匹配线，Ze = 300 Ω、Za = 50 Ω）这段四分之一波长线的特性阻抗应是多少？",
    "（图中 \\(\\lambda/4\\) 匹配线，\\(Z_e = 300\\ \\Omega\\)、\\(Z_a = 50\\ \\Omega\\)）"
    "这段四分之一波长线的特性阻抗应是多少？",
    "§10.4 真题（中文题干）参数")

add("（图中 λ/2 线，Ze = 50 Ω、电缆为 75 Ω）输出端的阻抗是多少？",
    "（图中 \\(\\lambda/2\\) 线，\\(Z_e = 50\\ \\Omega\\)、电缆为 75 Ω）输出端的阻抗是多少？",
    "§10.4 真题（中文题干）参数")

# ---------------------------------------------------------------- §11.2
add("FI = HF – FO   （取差频，FO 低于 HF：mélange infradyne，低外差）",
    "\\(\\text{FI} = \\text{HF} - \\text{FO}\\)   "
    "（取差频，FO 低于 HF：mélange infradyne，低外差）",
    "§11.2 展示式：差频（低外差）")

add("FI = FO – HF   （取差频，FO 高于 HF：mélange supradyne，高外差）",
    "\\(\\text{FI} = \\text{FO} - \\text{HF}\\)   （取差频，FO 高于 HF：mélange supradyne，高外差）",
    "§11.2 展示式：差频（高外差）")

add("FI = FO + HF   （取和频：FO 低时为 infradyne，FO 高时为 supradyne）",
    "\\(\\text{FI} = \\text{FO} + \\text{HF}\\)   （取和频：FO 低时为 infradyne，"
    "FO 高时为 supradyne）",
    "§11.2 展示式：和频")

add("当取差频（FI = HF – FO 或 FO – HF）时",
    "当取差频（\\(\\text{FI} = \\text{HF} - \\text{FO}\\) 或 \\(\\text{FO} - \\text{HF}\\)）时",
    "§11.2：差频的两种写法")

add("相反，取和频（FI = HF + FO）时",
    "相反，取和频（\\(\\text{FI} = \\text{HF} + \\text{FO}\\)）时",
    "§11.2：和频")

add("OL 频率 = HF – FI = 18 – 13 = 5 MHz；",
    "OL 频率 \\(= \\text{HF} - \\text{FI} = 18 - 13 = 5\\) MHz；",
    "§11.2 tips ⑤：由 HF 与 FI 求 OL")

# ---------------------------------------------------------------- §11.3
add("FI = | HF – FO |  或  FI = HF + FO",
    "\\(\\text{FI} = |\\text{HF} - \\text{FO}|\\)  或  "
    "\\(\\text{FI} = \\text{HF} + \\text{FO}\\)",
    "§11.3 展示式：两个能给出同一 FI 的频率")

add("Fim = 2·FO – HF   （等价于 Fim = HF ± 2·FI）",
    "\\(\\text{Fim} = 2 \\cdot \\text{FO} - \\text{HF}\\)   "
    "（等价于 \\(\\text{Fim} = \\text{HF} \\pm 2 \\cdot \\text{FI}\\)）",
    "§11.3 展示式：镜像频率")

add("能给出同一 FI 的另一个频率是 2 × 1 MHz – 650 kHz = <b>1350 kHz</b>（这就是镜像频率）。",
    "能给出同一 FI 的另一个频率是 \\(2 \\times 1\\ \\text{MHz} - 650\\ \\text{kHz} =\\) "
    "<b>1350 kHz</b>（这就是镜像频率）。",
    "§11.3 真题算例 1")

add("接收频率可取 1,1 + 0,65 = 1,75 MHz，于是镜像频率 = |2 × 1,1 – 1,75| = <b>450 kHz</b>。",
    "接收频率可取 \\(1{,}1 + 0{,}65 = 1{,}75\\) MHz，于是镜像频率 "
    "\\(= |2 \\times 1{,}1 - 1{,}75| =\\) <b>450 kHz</b>。",
    "§11.3 真题算例 2")

# §11.3 note (verified appendix, 正文副本): prose + two markdown-debris tables
add("得到的那个频率。 原文算例：HF = 14 MHz、FO = 5 MHz、FI = 9 MHz。"
    "若输入 HF 滤波器质量差、放过了 4 MHz，则 4 MHz（Fim）与 5 MHz（FO）混频得到 "
    "9 MHz（4 + 5 = 9），即中频；于是两个信号同时出现在 FI 级，在该级已无法分开。"
    "Fim 由 2·FO 或 2·FI 算出",
    "得到的那个频率。 原文算例：\\(\\text{HF} = 14\\) MHz、\\(\\text{FO} = 5\\) MHz、"
    "\\(\\text{FI} = 9\\) MHz。若输入 HF 滤波器质量差、放过了 4 MHz，则 4 MHz（Fim）"
    "与 5 MHz（FO）混频得到 9 MHz（\\(4 + 5 = 9\\)），即中频；于是两个信号同时出现在 "
    "FI 级，在该级已无法分开。Fim 由 \\(2 \\cdot \\text{FO}\\) 或 \\(2 \\cdot \\text{FI}\\) 算出",
    "§11.3 note 注：原文算例段（锚定正文，避开文末附录副本）")

add("原文算例续（本例如上，低外差且 FI = HF – FO）：Fim = \\|(2 × 5) – 14\\| = "
    "\\|(2 × 9) – 14\\| = 4 MHz。 §11.3b",
    "原文算例续（本例如上，低外差且 \\(\\text{FI} = \\text{HF} - \\text{FO}\\)）："
    "\\(\\text{Fim} = |(2 \\times 5) - 14| = |(2 \\times 9) - 14| = 4\\) MHz。 §11.3b",
    "§11.3 note 注：原文算例续（含 markdown 转义竖线残留）")

add("<p>HF = 接收频率，FO = 本机振荡频率，FI = 中频，Fim = 镜像频率。</p>",
    "<p>\\(\\text{HF}\\) = 接收频率，\\(\\text{FO}\\) = 本机振荡频率，\\(\\text{FI}\\) = 中频，"
    "\\(\\text{Fim}\\) = 镜像频率。</p>",
    "§11.3 note 注：符号对照")

add("<td>\\</td><td>2·FO – HF\\</td><td></td><td>\\</td><td>2·FI – HF\\</td><td></td>",
    "<td></td><td>\\(2 \\cdot \\text{FO} - \\text{HF}\\)</td><td></td><td></td>"
    "<td>\\(2 \\cdot \\text{FI} - \\text{HF}\\)</td><td></td>",
    "§11.3 note 摘要表：被 markdown 竖线拆散的 Fim 单元格（2 处）")

add("<td>FO < HF</td>", "<td>\\(\\text{FO} < \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>FO > HF</td>", "<td>\\(\\text{FO} > \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>FI = HF – FO</td>", "<td>\\(\\text{FI} = \\text{HF} - \\text{FO}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>FI = HF + FO</td>", "<td>\\(\\text{FI} = \\text{HF} + \\text{FO}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>FI = FO – HF</td>", "<td>\\(\\text{FI} = \\text{FO} - \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>2·FO – HF</td>", "<td>\\(2 \\cdot \\text{FO} - \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>2·FO + HF</td>", "<td>\\(2 \\cdot \\text{FO} + \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>2·FI – HF</td>", "<td>\\(2 \\cdot \\text{FI} - \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<td>2·FI + HF</td>", "<td>\\(2 \\cdot \\text{FI} + \\text{HF}\\)</td>",
    "§11.3 note 摘要表 1")
add("<th>FO/HF</th>", "<th>\\(\\text{FO}/\\text{HF}\\)</th>",
    "§11.3 note 章末小结表表头")
add("<th>FI =</th>", "<th>\\(\\text{FI} =\\)</th>",
    "§11.3 note 章末小结表表头")
add("<td>FO<HF</td>", "<td>\\(\\text{FO}<\\text{HF}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>FO>HF</td>", "<td>\\(\\text{FO}>\\text{HF}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>HF+FO</td>", "<td>\\(\\text{HF}+\\text{FO}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>HF–FO</td>", "<td>\\(\\text{HF}-\\text{FO}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>FO+HF</td>", "<td>\\(\\text{FO}+\\text{HF}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>FO–HF</td>", "<td>\\(\\text{FO}-\\text{HF}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>HF<FI</td>", "<td>\\(\\text{HF}<\\text{FI}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>HF>FI</td>", "<td>\\(\\text{HF}>\\text{FI}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>减小 FO</td>", "<td>减小 \\(\\text{FO}\\)</td>",
    "§11.3 note 章末小结表")
add("<td>增大 FO</td>", "<td>增大 \\(\\text{FO}\\)</td>",
    "§11.3 note 章末小结表")

# ---------------------------------------------------------------- §11.4
add("对应功率 P = U²/R = (50 µV)² / 50 Ω = 50 pW。",
    "对应功率 \\(P = U^2/R = (50\\ \\mu\\text{V})^2 / 50\\ \\Omega = 50\\) pW。",
    "§11.4：S9 基准功率算例")

add("<b>S9 = –73 dBm</b>（50 pW 与 1 mW 之比），<b>S0 = –127 dBm</b>（= –73 – 9 × 6）",
    "<b>\\(S9 = -73\\) dBm</b>（50 pW 与 1 mW 之比），<b>\\(S0 = -127\\) dBm</b>"
    "（\\(= -73 - 9 \\times 6\\)）",
    "§11.4：S9 / S0 的 dBm 值")

# ---------------------------------------------------------------- §11.7
add("<div class=\"formula\">P(W) = k · T(K) · B(Hz)　　17 °C 时 "
    "P(dBm) = –174 dBm + 10 log[B(Hz)]</div>",
    "<div class=\"formula\">\\(P\\,(\\text{W}) = k \\cdot T\\,(\\text{K}) \\cdot "
    "B\\,(\\text{Hz})\\)　　17 °C 时 \\(P\\,(\\text{dBm}) = -174\\ \\text{dBm} + "
    "10 \\log[B\\,(\\text{Hz})]\\)</div>",
    "§11.7 展示式：热噪声功率")

add("其中 k = 1,38.10⁻²³，T 为绝对温度（°C + 273），B 为带宽（Hz）。",
    "其中 \\(k = 1{,}38 \\cdot 10^{-23}\\)，T 为绝对温度（\\(\\text{°C} + 273\\)），"
    "B 为带宽（Hz）。",
    "§11.7：k 值与 T 的换算")

# --------------------------------------------- 补漏：正文里零散的算式片段
add("只是第一步，还要再乘 √2：",
    "只是第一步，还要再乘 \\(\\sqrt{2}\\)：",
    "§10.1 tips：√2 系数")

add("PE 介质、D/d = 3,5 时得到 50 Ω。若介质是空气（ε 约为 1），D/d = 5 时 Z ≈ 96 Ω，"
    "D/d = 3,33 时 Z ≈ 72 Ω",
    "PE 介质、\\(D/d = 3{,}5\\) 时得到 50 Ω。若介质是空气（ε 约为 1），"
    "\\(D/d = 5\\) 时 \\(Z \\approx 96\\) Ω，\\(D/d = 3{,}33\\) 时 \\(Z \\approx 72\\) Ω",
    "§10.2：D/d 与 Z 的三种取值")

add("\"圆形同轴 + PE 介质 + D/d = 3,5 ⇒ 50 Ω\"",
    "\"圆形同轴 + PE 介质 + \\(D/d = 3{,}5\\) ⇒ 50 Ω\"",
    "§10.2：原文唯一推导的引用（D/d = 3,5 ⇒ 50 Ω）")

add("产生双边带（DBL = BLI + BLS）",
    "产生双边带（\\(\\text{DBL} = \\text{BLI} + \\text{BLS}\\)）",
    "§11.5 对照表：DBL = BLI + BLS")

add("硬加。 天线匹配／耦合不在 §11.5，而在 §10.3b（boîte de couplage 即耦合盒／匹配盒，"
    "由 π 型或 T 型滤波器构成，插在发射机与馈线之间，既限制反射功率又完成阻抗匹配）"
    "以及 §9（balun 平衡转换器、λ/4 线等 adaptation",
    "硬加。 天线匹配／耦合不在 §11.5，而在 §10.3b（boîte de couplage 即耦合盒／匹配盒，"
    "由 π 型或 T 型滤波器构成，插在发射机与馈线之间，既限制反射功率又完成阻抗匹配）"
    "以及 §9（balun 平衡转换器、\\(\\lambda/4\\) 线等 adaptation",
    "§11.5 note 注：λ/4 匹配线")


def main():
    text = open(TARGET, encoding="utf-8").read()
    problems = []
    out = []
    outside = []
    for i, (old, new, note) in enumerate(P, 1):
        if "$" in new:
            problems.append("#%d $ in new: %s" % (i, old[:80]))
        tm_old, tm_new = ap.tagmultiset(old), ap.tagmultiset(new)
        if tm_old != tm_new:
            problems.append("#%d tag multiset %s -> %s : %s"
                            % (i, tm_old, tm_new, old[:100]))
        if not ap.tag_balanced(new):
            problems.append("#%d new tags not balanced: %s" % (i, new[:100]))
        c = text.count(old)
        if c == 0:
            problems.append("#%d NOT FOUND: %s" % (i, old[:140]))
            continue
        pos = -1
        for _ in range(c):
            pos = text.index(old, pos + 1)
            ln = text.count("\n", 0, pos) + 1
            if not (229 <= ln <= 245 or 6560 <= ln <= 7180):
                outside.append("#%d line %d: %s" % (i, ln, old[:70]))
        text = text.replace(old, new)
        out.append({"old": old, "new": new, "count": c, "note": note})
    print("pairs: %d   problems: %d" % (len(out), len(problems)))
    for p in problems:
        print("  !!", p)
    print("occurrences outside T10/T11 region: %d" % len(outside))
    for p in outside:
        print("  ??", p)
    if problems:
        return 1
    print("delims: \\( %d  \\) %d   \\[ %d  \\] %d   $ %d"
          % (text.count("\\("), text.count("\\)"),
             text.count("\\["), text.count("\\]"), text.count("$")))
    assert text.count("\\(") == text.count("\\)")
    assert text.count("\\[") == text.count("\\]")
    assert "$" not in text
    data = {"section": "T10 §10.1–§10.4 传输线/特性阻抗/驻波与匹配 "
                       "+ T11 §11.1–§11.7 接收机与发射机框图",
            "pairs": out}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
