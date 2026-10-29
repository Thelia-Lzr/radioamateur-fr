# -*- coding: utf-8 -*-
import json, os, re

OUT = "out_8.json"

cards = {}

cards["K106"] = {
 "title_fr": "Facteur Q des circuits bouchon et série",
 "title_zh": "谐振电路的品质因数 Q",
 "front": "串联和并联（bouchon）谐振电路里，怎样由 L、C、R 算出谐振时的品质因数 Q？并联谐振阻抗又怎么算？",
 "body": r"""## Q 的两个来源
- 由谐振曲线：\(Q=f_0/B\)，B 是 −3 dB 带宽（电压降到 0,707 倍的那对频率之差）。
- 由元件值：谐振时 \(X_L=X_C=\sqrt{L/C}\)（Thomson 关系的变形），于是串联电路 \(Q=X_L/R\)，并联（bouchon）电路 \(Q=Z_{\text{bouchon}}/X_L\)，两个式子化简后完全相同。

## 法国考题的简化公式
L 取 µH、C 取 pF 时，\(\sqrt{L(\mu H)/C(pF)}\) 的数值恰好等于以 kΩ 为单位的 \(\sqrt{L/C}\)（因为 \(\sqrt{10^{-6}/10^{-12}}=10^{3}\)），所以教材直接用：

\[ Q=\frac{\sqrt{L(\mu H)/C(pF)}}{R(\mathrm{k}\Omega)}\qquad Z_{\text{bouchon}}(\mathrm{k}\Omega)=\sqrt{L(\mu H)/C(pF)}\times Q \]

并联阻抗还有一个等价写法：\(Z_{\text{bouchon}}(\mathrm{k}\Omega)=\dfrac{L(\mu H)}{R(\mathrm{k}\Omega)\times C(pF)}\)，也就是 \(Z_{\text{bouchon}}=X_L^2/R\)。它与 R、Q 的关系是
\[ Z_{\text{bouchon}}=R_{\text{parallèle}}=R_{\text{série}}\cdot Q^2 \]
串联损耗（由 R 体现）折算到并联后会与电路本身的并联电阻并联，拉低总电阻与 Q，这是实践中 Q 上不去的原因之一。

## 怎么测量
串联：用示波器量谐振时 L、C 两端电压与发生器电压之比，商即 Q，所以 Q 又叫 coefficient de surtension：谐振时元件上的电压可达电源电压的 Q 倍。
并联：用 ondemètre à absorption（靠被测电路的吸收造成自身读数下陷 dip）或 grid-dip（自带振荡器，被测电路谐振时自身电流骤降）找电压峰 \(f_0\)，再找电压降到 0,707 倍的两个频率，频差即 B，由 \(Q=f_0/B\) 得 Q。趋肤效应（effet de peau）使 R 随频率升高，所以“Q 正比于谐振频率”只是近似。

## 判据与陷阱
- Q 只有个位数（例如 1,6 左右）说明选频极差，实际电路不可用。
- 谐振时 \(Z=R\)：串联是最小值 R，并联是最大值 \(R_p\)，既不是 0 也不是 ∞。
- 单位必须成套：只有 µH、pF 配 kΩ 才直接出答案，用 H 与 F 会差 \(10^9\)。
"""
}

cards["K107"] = {
 "title_fr": "Bande passante à −3 dB et facteur Q",
 "title_zh": "通带宽度与 Q 的关系",
 "front": "已知 L、C、R 或已知谐振频率与带宽，怎样求出 −3 dB 带宽 B？B 与 Q 是什么关系？",
 "body": r"""## 一条主线
\[ B=\frac{f_0}{Q}\qquad\Longleftrightarrow\qquad Q=\frac{f_0}{B} \]
B 是 −3 dB 带宽。Q 越高，曲线越窄、两侧裙边越陡、对邻频的抑制越好，但也越容易受元件漂移与温度影响。

## 两步计算法
1. 谐振频率：\(f_0=1/(2\pi\sqrt{LC})\)。L 取 µH、C 取 pF 时，法国教材写成 \(f_0(\mathrm{MHz})=159/\sqrt{L(\mu H)\times C(pF)}\)（159≈1000/2π）。
2. 品质因数：\(Q=\sqrt{L(\mu H)/C(pF)}/R(\mathrm{k}\Omega)\)，或题目直接给出 Q。
3. 带宽：\(B=f_0/Q\)，单位随 \(f_0\)。

自检算例（数值与考题无关）：L=50 µH、C=200 pF，乘积 10000、开方 100，得 \(f_0\approx1,59\ \mathrm{MHz}\)；\(\sqrt{50/200}=0,5\)，若 R=5 Ω（即 0,005 kΩ）则 Q=100，于是 \(B\approx15,9\ \mathrm{kHz}\)。三步交叉验证可以抓出量级错误。

## 题型分流
- 给 L、C、R：先算 f0，再算 Q，再算 B。
- 给 f0 与 B：一步 \(Q=f_0/B\)。
- 给 L、C 与 Q：直接 \(B=f_0/Q\)，注意 kHz 与 MHz 的换算（6000 kHz 与 6 MHz 是同一个数）。

## 多节滤波器与观测
两节以上同频或轻微错开的 LC：整条曲线不再由单个 Q 描述，改用带宽加 taux de sélectivité（形状因数）。带宽也可以定义在 −6、−13 甚至 −60 dB 上。观测工具是 analyseur de spectre（横轴频率、纵轴电压或 dBm），或者 wobulateur 加示波器扫频，效果等同频谱仪。放大器的通带同样服从这个倒数关系，这就是 HF 功放调谐必须调准的原因。

## 判据
本节真正要背的只有两条：\(f_0=159/\sqrt{L(\mu H)\cdot C(pF)}\) 与 \(B=f_0/Q\)，其余都能现场推。算出 f0 后先看数量级落在哪个频段，再回头选答案。
"""
}

cards["K108"] = {
 "title_fr": "R et Z à la résonance à partir de L, C, Q",
 "title_zh": "由 L、C、Q 求 R 与 Z",
 "front": "已知 L、C 和品质因数 Q，串联谐振的 R 与并联（bouchon）谐振的阻抗 Z 分别怎么算？单位怎么处理？",
 "body": r"""## 由 L、C、Q 反推 R 或 Z
谐振时感抗与容抗相等并互相抵消，\(X_L=X_C=\sqrt{L/C}\)，电路只剩电阻：
- 串联：\(Z_{\text{rés}}=R=\sqrt{L/C}/Q\)
- 并联（bouchon）：\(Z_{\text{rés}}=R_p=\sqrt{L/C}\times Q\)

法国简化式（L 取 µH、C 取 pF、结果以 kΩ 计）：\(R(\mathrm{k}\Omega)=\sqrt{L(\mu H)/C(pF)}/Q\)，\(Z(\mathrm{k}\Omega)=\sqrt{L(\mu H)/C(pF)}\times Q\)。
判据：题目问 R，或画的是串联 LC → 除；问 Z、写“阻抗”、画 bouchon（并联谐振）→ 乘。算出 kΩ 后按选项换成 Ω（1 kΩ=1000 Ω），选项里常同时摆出 Ω 与 kΩ 两种形式互相干扰。

## 频谱曲线怎么读
- 分析仪横轴频率、纵轴电压或 dBm。dBm 是相对 1 mW 的分贝数（在给定阻抗下，通常 50 Ω）：0 dBm=1 mW，30 dBm=1 W，39 dBm≈8 W，26 dBm≈0,4 W。
- 求“低于峰值 x dB 处的带宽”：把峰值电平减 x dB 得到门限，再读曲线在门限上的两个边频之差。
- 纵轴是电压时，功率比 n 对应电压比 \(\sqrt{n}\)：−13 dB 即功率比 1/20、电压比 1/4,45（约峰值电压的 0,223 倍）。
- 由峰值电压与峰值功率还能反推阻抗：\(Z=U^2/P\)。

## 多节滤波器的选择性
一节 LC 的曲线由 Q 决定；多节时改用 taux de sélectivité（形状因数）S，即同一条曲线在两个电平上的带宽之比，常以百分比表示（例如 −60 dB 与 −6 dB 带宽之比）。带宽本身也可以定义在任意电平上。

## 法国特色与判据
µH/pF→kΩ 的简化式、159 常数，以及“39 dBm≈8 W”这类换算，是法国备考的固定工具；dB 与比值的换算表（3 dB=×2、6 dB=×4、10 dB=×10、13 dB=×20、20 dB=×100）也必须背。频谱分析仪同时是 ANFR 监测频谱、排查干扰的常用仪器，法国把这项监测作为频率管理的日常工作。
"""
}

cards["K109"] = {
 "title_fr": "Amplificateur opérationnel en inverseur",
 "title_zh": "运放反相放大器",
 "front": "运放接成反相放大器（inverseur）时，电压增益与输出电压怎样用 R1、R2 表示？为什么增益带负号？",
 "body": r"""## 反相放大器的基本关系
信号经 R1 送到反相输入端 N，R2 从 N 接回输出 S 构成负反馈，同相输入端 P 接参考电位（双电源时即地）。理想运放输入阻抗无穷，故 \(I_{e^-}=0\)，于是
\[ I_{R1}=I_{R2}=\frac{U_E}{R_1} \]
负反馈把 N 拉到与 P 相同的电位：双电源、P 接地时 \(U_N=U_P=0\)（masse virtuelle，虚地）。由此得到
\[ G=\frac{U_S}{U_E}=-\frac{R_2}{R_1}\qquad U_S=-U_E\times\frac{R_2}{R_1} \]
负号表示输出与输入反相 180°。算例（数值自拟）：R2=100 kΩ、R1=10 kΩ，则 G=−10，输入 0,2 V 时输出 −2 V。反过来求反馈电阻：\(R_2=-G\times R_1\)。注意这里的增益是**乘系数**而不是分贝值，法国教材特别强调不要写成 dB。

## 电路限制
- 需双电源（如 ±5 V）。若用单电源（12 V 对地）供电，P 点要由电阻分压给出中点电压，虚地电位随之改变，此时 \(U_N\approx U_P\ne0\)。
- 电流不放大：\(I_E=I_{R1}=I_{R2}=I_S\)；输出幅度受电源轨限制，不可能超过供电电压。
- 反相输入端的等效输入阻抗约等于 R1，并不是无穷大，这一点与同相接法不同。

## 判据
- 题面出现 R1 在输入端、R2 接回输出、问 gain 或 VS：一律用 \(G=-R_2/R_1\) 与 \(U_S=-U_E R_2/R_1\)。
- 三个量给两个求第三个，可用教材的三角法（类似欧姆定律三角），但 R2 那一支要带负号。
- 最常见失分点是输出符号和数量级，先算比值再乘输入电压。

## 法国/欧盟视角
这类“montage fondamental”属法国考纲 §8.2 的元件级内容，考接线关系与符号，不要求记集成块型号。整机层面在欧盟受 RED 2014/53/EU 约束（CE 标记、EMC 与频谱使用要求），在法国由 ANFR 负责频率使用。⚠️待核：RED 对业余无线电整机的具体适用条款。
"""
}

def main():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
        old.update(cards)
        data = old
    else:
        data = cards
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    # validate
    with open(OUT, encoding="utf-8") as f:
        chk = json.load(f)
    print("keys:", len(chk), sorted(chk))
    for k in sorted(cards):
        b = cards[k]["body"]
        han = len(re.findall(r"[\u4e00-\u9fff]", b))
        print(k, "han=", han, "len=", len(b), "front=", len(cards[k]["front"]),
              "title_zh=", cards[k]["title_zh"])

main()
