# -*- coding: utf-8 -*-
# 中文教材正文：区块 W11（§11.4–11.7 与第 12 章：接收机灵敏度、发射机各级、调制与带宽）

SECTIONS = [
    {
        "id": "T114",
        "ref": "11.4",
        "title_zh": "接收机的灵敏度与 S 表",
        "title_fr": "La sensibilité d'un récepteur",
        "body": """<p>灵敏度（sensibilité）用接收机能够正常使用所需的<b>最小输入信号</b>来衡量。一条无线电链路算「好」的条件是：接收机自身的噪声远低于要接收的信号，因此接收机越灵敏，就越能把微弱信号「捞」出来。信号强度习惯用 S 点（points S）表示。</p>
<p>基准点是 <b>S9</b>：接收机输入端（50 Ω 负载）上的电压为 50 µV，对应功率 P = U²/R = (50 µV)² / 50 Ω = 50 pW。相邻两个 S 点之间相差 <b>6 dB</b>。原文给出 30 MHz 以下的 S 表如下：</p>
<table>
<thead><tr><th>S 点</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>9+10 dB</th><th>9+20 dB</th><th>9+30 dB</th></tr></thead>
<tbody>
<tr><td>dB/S9</td><td>-54</td><td>-48</td><td>-42</td><td>-36</td><td>-30</td><td>-24</td><td>-18</td><td>-12</td><td>-6</td><td>0</td><td>+10</td><td>+20</td><td>+30</td></tr>
<tr><td>µV/50Ω</td><td>0,1</td><td>0,2</td><td>0,4</td><td>0,8</td><td>1,5</td><td>3</td><td>6</td><td>12</td><td>25</td><td>50</td><td>160</td><td>500</td><td>1600</td></tr>
</tbody>
</table>
<p>输入信号也可以用 dBm（相对于 1 mW 的分贝数）表示：<b>S9 = –73 dBm</b>（50 pW 与 1 mW 之比），<b>S0 = –127 dBm</b>（= –73 – 9 × 6）。现代接收机的灵敏度常在 S1 甚至 S0 量级，但 S 表的校准往往很随意，未必符合上表。</p>
<p>要提高灵敏度，接收机的每一级（振荡器、放大器）都必须尽可能少产生噪声，也就是尽可能<b>线性</b>（见 §11.7e）。</p>
<div class="tips">本主题在题库中只有一道题，而且是<b>识图题</b>：图中标注的某一级是什么——答案是<b>谐波滤波器（filtre anti-harmonique）</b>，官方题解里也叫 <em>filtre en PI</em>，它属于发射机末级之后的部分。可见识图题并不拘泥于本节标题所写的内容，发射机的框图（§11.5）必须一起掌握。</div>""",
    },
    {
        "id": "T115",
        "ref": "11.5",
        "title_zh": "发射机的框图：从话筒到天线的各级",
        "title_fr": "Synoptique d'un émetteur",
        "body": """<p>发射机（émetteur）的框图（synoptique）<b>从话筒读到天线</b>：信号从左侧的话筒（microphone）走向右侧的天线（antenne）。与接收机一样，中间可以有<b>一次或多次变频</b>（changement de fréquences）。框图里必有的两个要素：</p>
<ul>
<li><b>调制器（modulateur）</b>：它<b>必然包含一个高频振荡器（oscillateur HF）</b>，并按低频（BF）的节奏改变那一路高频信号。改变的到底是幅度、频率还是相位，就决定了调制方式（见第 12 章）。所以识图题问「把 BF 变成 HF 的那一级叫什么」时，答案往往是直接写 <b>oscillateur（振荡器）</b>，因为调制器就是围绕振荡器搭起来的。</li>
<li><b>谐波滤波器（filtre anti-harmonique）</b>：一台发射机<b>必须</b>带一个低通（passe-bas）谐波滤波器，用来避免非必要辐射（rayonnements non essentiels）。题目里它也叫 <em>filtre en PI</em>，位置在末级功放之后、天线之前。</li>
</ul>
<p>发射机与接收机装在同一台机器里就是收发信机（transmetteur，英文 transceiver）。二者共用的部分主要是：</p>
<ul>
<li><b>本机振荡器（oscillateur local）</b>：正因如此，接收频率会跟着发射频率一起移动；为了做到这一点，<b>调制器输出的频率要等于接收机的中频（FI）</b>；</li>
<li><b>天线插座（prise antenne）</b>：共用同一副天线（aérien）；</li>
<li>一套收发切换装置：机械开关（commutateurs）、机电继电器（relais électromécaniques）或开关二极管（diodes de commutation），用来方便地从发射切到接收、再切回来。</li>
</ul>
<p>下表把发射机与相关接收机框图中出现的各级做成中法对照（只列原文与题库中出现的名称）：</p>
<table>
<thead><tr><th>法文名称</th><th>缩写</th><th>中文</th><th>在整机中的作用</th></tr></thead>
<tbody>
<tr><td>microphone</td><td>micro</td><td>话筒</td><td>把话音变成低频（BF）信号，是发射机框图的起点</td></tr>
<tr><td>amplificateur BF / AF</td><td>ampli AF</td><td>音频放大器</td><td>放大低频信号；AM 时可插入压缩器（compresseur de modulation），FM 时可加预加重（préaccentuateur）</td></tr>
<tr><td>oscillateur HF</td><td>VFO / VCXO</td><td>高频振荡器</td><td>产生载波；调制器的核心</td></tr>
<tr><td>modulateur</td><td>—</td><td>调制器</td><td>用 BF 去改变 HF 的幅度、频率或相位</td></tr>
<tr><td>mélangeur équilibré</td><td>—</td><td>平衡混频器</td><td>产生双边带（DBL = BLI + BLS），BLU 发射机的核心</td></tr>
<tr><td>filtre à quartz</td><td>—</td><td>石英晶体滤波器</td><td>从 DBL 中选出要用的那一条边带并限制带宽</td></tr>
<tr><td>multiplicateur de fréquence</td><td>—</td><td>倍频器</td><td>提高频率；调频/调相时频偏与调制指数一并加倍</td></tr>
<tr><td>amplificateur RF</td><td>ampli RF</td><td>射频放大器（功放）</td><td>把射频信号放大到所需的 PEP，是「缺哪一级」这类题出现最多的答案</td></tr>
<tr><td>filtre anti-harmonique</td><td>filtre en PI</td><td>谐波滤波器（低通）</td><td>抑制谐波等非必要辐射，接在天线前面</td></tr>
<tr><td>prise antenne / antenne</td><td>—</td><td>天线插座 / 天线</td><td>框图的终点</td></tr>
</tbody>
</table>
<div class="tips">真题里最典型的三种问法：<br>①「话筒 – 平衡混频器 – 滤波器 – <b>?</b> – 天线」缺什么？→ <b>射频放大器（ampli RF）</b>；<br>②「话筒 – <b>???</b> – 射频功放 – 天线」缺什么？→ <b>振荡器（oscillateur）</b>（官方题解注明：写「调制器 modulateur」本来也可以，只是选项里没有）；<br>③图中标注的那一级是什么？→ <b>射频放大器（ampli RF / amplificateur RF）</b>。<br>官方题解还提醒两个陷阱：若是 BLU 发射机的局部框图，图上那个「滤波器」不一定是谐波滤波器，而多半是与平衡混频器配套的<b>石英晶体滤波器</b>；有些框图里即使画了功放，<b>仍然缺少谐波滤波器</b>。识图时先判断整机是 AM、FM、BLU 还是 CW，再对号入座。</div>
<div class="warn">⚠️ 待核实：本块原文的 §11.5 只提到话筒、调制器（含高频振荡器）、谐波滤波器、天线插座以及收发切换装置，并未出现「缓冲级（étage tampon / buffer）」「激励级（excitateur / driver）」「天线匹配网络（adaptation d'antenne / boîte de couplage）」这些名称；上表因此只收原文与题库中确实出现的级。若考试要求补全这些中间级，须向 ANFR 官方大纲与官方题解核实其法文名称与位置。</div>""",
    },
    {
        "id": "T116",
        "ref": "11.6",
        "title_zh": "电磁兼容（CEM）的基本术语",
        "title_fr": "La Compatibilité Électromagnétique (CEM)",
        "body": """<p>电磁兼容（compatibilité électromagnétique, CEM）是双向的：既是发射机<b>不干扰环境</b>（尤其是别的接收机）的能力，也是接收机<b>不被发射机或环境干扰</b>的能力。</p>
<p>任何电气、机电或电子设备对周围的电磁环境都只有一定程度的抗扰度（immunité）。当干扰超过这个水平，就达到了它的<b>敏感阈值（seuil de susceptibilité）</b>，此时必须采取<b>加固（durcissement）</b>措施来提高抗扰度。站在干扰的「源头」说话叫<b>干扰发射（émission）</b>，站在被干扰的设备（或接收机）说话叫<b>敏感（susceptibilité）</b>。</p>
<p>按传播途径分两类：</p>
<ul>
<li><b>传导干扰（conduite）</b>：通过导体传播——导线、电缆、印制板走线等；</li>
<li><b>辐射干扰（rayonnée）</b>：通过空间电磁场传播。</li>
</ul>""",
    },
    {
        "id": "T117",
        "ref": "11.7",
        "title_zh": "互调、交调与噪声",
        "title_fr": "Intermodulation, transmodulation et bruit",
        "body": """<p><b>互调（intermodulation）</b>的产物一律来自某个<b>非线性</b>级（或器件）上的频率混合——在发射机输出端或在接收机输入端。混合给出基频及其谐波的和与差：除了 A + B、A – B，还有 2B – A、2A – B 这类<b>三阶产物</b>；A 与 B 越接近，这类产物越难滤除。原文例子：14,1 与 14,2 MHz 同时进入一个非线性射频级时，会在 14 MHz 上听到三阶产物。<b>三阶截点（IP3）</b>是输入/输出特性直线与三阶互调产物直线的交点，用 dBm 表示，<b>越大越好</b>。</p>
<p><b>交调（transmodulation）</b>：当邻近有用频率 F 处有一个强信号时，接收机输入级被过载而变得非线性，这个强信号便去「调制」有用信号，于是既听到有用信号本身的调制，又听到多出来的一层调制。</p>
<p><b>噪声</b>：一部分噪声来自热（电子热运动），经天线进入。热噪声功率</p>
<div class="formula">P(W) = k · T(K) · B(Hz)　　17 °C 时 P(dBm) = –174 dBm + 10 log[B(Hz)]</div>
<p>其中 k = 1,38.10⁻²³，T 为绝对温度（°C + 273），B 为带宽（Hz）。原文例子：35 °C、2500 Hz 带宽时为 –139,74 dBm，17 °C 同带宽为 –140 dBm，500 Hz 带宽时约 –147 dBm——可见<b>带宽影响很大、温度影响很小</b>（对业余应用而言）。天线上还要叠加人为的无线电污染、低频段很强的天电噪声，以及主要来自太阳活动、在 VHF 以上较明显的银河噪声。接收机每一级都会附加噪声，<b>第一级的噪声必须尽可能低</b>，这样才能得到低噪声系数，从而<b>提高灵敏度</b>。</p>""",
    },
]

SECTIONS += [
    {
        "id": "T121",
        "ref": "12.1",
        "title_zh": "各类调制方式的表示：时域图与频谱图",
        "title_fr": "Schématisation des différents types de modulation",
        "body": """<p>一个正弦信号由三个量描述：<b>幅度、频率、相位</b>。要用电波传送信息（话音、图像、计算机数据……），就得按信息的节奏去改变其中一个量——这就叫调制（modulation）。</p>
<p>有两种表示法：<b>oscillogramme</b>（示波器上显示的「随时间的波形」）与 <b>spectrogramme</b>（频谱分析仪上显示的「随频率的分布」）。因此测量发射<b>占用带宽（bande occupée）</b>用的仪器是<b>频谱分析仪（analyseur de spectre）</b>。</p>
<table>
<thead><tr><th>调制方式</th><th>时域特征</th><th>频谱（频域）特征</th></tr></thead>
<tbody>
<tr><td>调幅 AM</td><td>高频的幅度按 BF 变化，BF 形成虚线包络</td><td>载波居中，两侧各一条边带，即 HF + BF 与 HF – BF</td></tr>
<tr><td>单边带 BLU / SSB</td><td>与 AM 同源，但去掉载波和一条边带</td><td>BF 谱整体平移到载波的一侧；BLS 从 200 Hz 到 3 kHz；BLI 的谱是反的</td></tr>
<tr><td>电报 CW</td><td>高频的通断（tout ou rien）</td><td>最窄；是最简化的调幅</td></tr>
<tr><td>调频 FM</td><td>频率按 BF 变化，BF 最大时频率最高</td><td>占用带宽 = 2 × 频偏（excursion）</td></tr>
<tr><td>调相 PM</td><td>相位随 BF 变化，波形与 FM 极像</td><td>与 FM 同属角调制，解调电路相同</td></tr>
<tr><td>数字模式 MGM</td><td>FSK、PSK、QAM 等</td><td>由每秒状态变化数（Baud）与状态数（valence）决定</td></tr>
</tbody>
</table>
<ul>
<li><b>频偏（excursion，也叫 swing）</b>是中心频率与两个极值频率之一之间的差；<b>占用带宽是频偏的两倍</b>，也就是两个极值频率之间的间隔。</li>
<li><b>调相</b>的时域波形与调频极为相似，人的耳朵分不出 FM 与 PM，但计算机（声卡及其数字处理）和 DSP 分得出。</li>
<li><b>数字模式</b>（MGM，Machine Generated Modulation）也逃不出这套分类：CW 是 2 状态（通/断）的数字调幅；FSK（Frequency Shift Keying）用一路副载波去调频；PSK（Phase Shift Keying）调相位，可以取 2 个状态（0 与 π，即 2-PSK）、4 个状态（0、π/2、π、3π/2，即 4-PSK）甚至更多；在 BLU 发射机上发 AFSK 就等于调 FSK。</li>
<li><b>QAM（正交调幅）</b>把调幅与调相结合起来，最多可有 256 个状态（即 16²），每个状态对应一种幅度加相位的组合。它使调制与解调更复杂（有干扰或衰落时尤甚），但提高了比特率：比特率（bps）= 每秒状态变化数（以 Baud 计，决定占用带宽）× 信号可取的状态数。首字母为 D 的这一类发射（Wi-Fi 等系统即属此类）自 2012 年起对法国业余爱好者开放（3 类操作员除外）。</li>
<li>别把频谱图上「载波两侧的两条边带」跟时域图上包络的上下两半混为一谈。</li>
</ul>""",
    },
    {
        "id": "T122",
        "ref": "12.2",
        "title_zh": "调制器与解调器：按调制方式对号入座",
        "title_fr": "Les modulateurs et les démodulateurs",
        "body": """<p>考试大纲对调制器、解调器的要求很有限：只要知道<b>各级的名称</b>，以及按调制方式所画的<b>框图（synoptique）</b>即可，细节见后面各节。</p>
<table>
<thead><tr><th>调制方式</th><th>调制（发射）方框图</th><th>解调（接收）方框图</th></tr></thead>
<tbody>
<tr><td>AM 调幅</td><td>一个普通混频器：HF 与 BF 相混，载波保留</td><td>包络检波（détecteur d'enveloppe）：二极管 + RC 低通</td></tr>
<tr><td>BLU / SSB</td><td>本机振荡器（OL）+ 平衡混频器（mélangeur équilibré）+ 石英晶体滤波器（filtre à quartz）</td><td>BFO + AM 检波，合称乘积检波器（détecteur de produit）</td></tr>
<tr><td>FM / PM</td><td>电抗振荡器（oscillateur à réactance）：变容二极管（Varicap）或电容式话筒 + LC 回路</td><td>鉴频器（discriminateur，即 FM 解调器）</td></tr>
<tr><td>CW 电报</td><td>载波通断键控</td><td>与 BLU 相同：BFO + 检波 = 乘积检波器</td></tr>
</tbody>
</table>
<p>识图题常见的问法：</p>
<ul>
<li>「把 BF 变成 HF 的那一级叫什么？」——选项里往往没有「调制器」这个词，应选 <b>oscillateur（振荡器）</b>，因为调制器都是围绕振荡器构成的；</li>
<li>图上有 <b>鉴频器</b>，或限幅器 + 去加重（désaccentuateur）→ 能收 <b>FM</b>；</li>
<li>图上是 <b>OL + 平衡混频器 + 石英晶体滤波器</b> → 产生 <b>BLU</b>；</li>
<li>图上出现 <b>BFO</b>，其后的检波级就叫 <b>détecteur de produit（乘积检波器）</b> → BLU 或 CW。</li>
</ul>
<div class="tips">判断发射类别的通用办法：只看「混频器是不是平衡的」还不够，还要看它后面<b>有没有石英晶体滤波器</b>——普通混频器（载波保留）产生的是 AM，平衡混频器（载波被抑制）产生的 DBL 只有经过石英晶体滤波器选出单一边带之后才成为 BLU。</div>""",
    },
    {
        "id": "T123",
        "ref": "12.3",
        "title_zh": "调幅（AM）：调制深度、包络与功率",
        "title_fr": "La Modulation d'Amplitude",
        "body": """<p>调幅（modulation d'amplitude, AM）无论是发射还是接收都是最容易实现的调制方式：最早的无线电广播、最早的业余无线电电话通信用的都是它。但由于性能不佳，业余爱好者现在几乎不再使用，只还在模拟电视里见到。</p>
<p><b>解调（détection）也叫包络检波（détecteur d'enveloppe）</b>：一支二极管后面跟一个 RC 低通电路，用来滤掉高频。送到音频放大器（amplificateur AF）的低频电平由电位器 R 的滑动点调节。检波二极管可以用<b>锗（germanium）</b>管：它的导通阈值（0,3 volt）比硅管低，所以在信号谷底处包络还原得更好。检波二极管常做成小玻璃管，内有一根金属尖。</p>
<p><b>自动增益控制（contrôle automatique de gain, CAG）</b>是一个「无论输入高频信号强弱，都给出相同低频电平」的装置。更准确地说，CAG 作用于输入端 RF 级和/或 FI 级的增益，使它们在强信号下不饱和，输出信号不被削波；最终受影响的确实是低频电平。CAG 的控制电压从检波级经电阻 R 取回，电平由 RF Gain 电位器设定；这个电压去调整一个双栅 FET 的 FI 级（或其它 RF 级）的增益，同时它就是接收机 <b>S 表</b>所指示的电压。</p>
<p><b>产生 AM 的两种办法</b>：改变末级功放的供电电压，或者用一只 MOS-FET 把 HF 与 BF 混合起来。</p>
<p><b>时域波形与 PEP。</b>AM 信号高频部分的<b>峰值 B 就是包络峰值功率（PEP）</b>——发射机不可能输出比它更大的功率，核定最大允许功率时用的就是它。没有 BF 时，高频信号的幅度应为 B/2；被 BF（图中虚线即「BF 包络」）调制之后，高频信号在 B/2 上下摆动，从 a 变到 A，变化量为 b。如果 BF 相对 B 是居中的，就有</p>
<div class="formula">b = A – a　　B = A + a</div>
<p>功率计读到的平均功率是 PEP 的一半。如果 BF 包络越过 B（图上第 3 区）或掉到 0 以下（第 4 区），就是<b>过调制</b>：一部分低频信号没有被发射出去，因而产生失真。最理想的调制状态是 b 尽可能大，同时包络又不越过 0 和 B 这两个界限。</p>
<p><b>调制深度（taux de modulation）K</b>用百分数表示：</p>
<div class="formula">K(%) = (A – a) / (A + a) = b / B</div>
<p>用 A、a 计算的前提是 BF 包络相对载波峰值 B 居中，并且始终落在 0 与 B 之间（用 B 与 b 更直观，用 A 与 a 更好测）。为了避免过调制并优化调制深度，可以在 AF 放大器与调制器之间插入一个<b>压缩器（compresseur de modulation）</b>：把从话筒来的低频信号的尖峰压小一些，同时把谷底抬高一些。</p>
<p>原文例题：在第 2 区测得 A = 4,2 V、a = 1,8 V，求调制深度。</p>
<div class="formula">K = (A – a)/(A + a) = (4,2 – 1,8)/(4,2 + 1,8) = 2,4/6 = 0,4 = 40%（2,4 V 与 6 V 即 b 与 B）</div>
<p><b>占用带宽。</b>AM 的频谱是「载波 + 两条边带」：调制的过程就是把 HF 与 BF 相混，得到 HF + BF 与 HF – BF。因此当最高调制频率为 fm 时，AM 占用带宽等于 <b>2 × fm</b>；话音通信取低频谱上限 3 kHz 时约为 6 kHz 量级。法规对各类发射占用带宽的法定上限见法规章节，须以 ANFR 官方文件为准。</p>
<div class="warn">⚠️ 待核实：本块原文只说明了 AM 的频谱是「载波 + 两条边带（HF ± BF）」，并<b>没有写出「AM 带宽 = 2 × 最高调制频率」这个公式</b>。上式是按原文的频谱说明推得的，考试若涉及占带宽度计算，请对照官方大纲与官方题解核实取用的调制频率上限。</div>""",
    },
    {
        "id": "T124",
        "ref": "12.4",
        "title_zh": "调频（FM）与调相（PM）：鉴频器、频偏与卡森规则",
        "title_fr": "La Modulation de Fréquence",
        "body": """<p>调频（modulation de fréquence, FM）与调相（modulation de phase, PM）都是<b>角调制</b>，特性非常接近——近到解调电路完全相同，所以我们嘴里说的是 FM，实际上常常是 PM。人的耳朵分不出 FM 与 PM，但计算机（以及它的声卡）和 DSP 分得出来。就时域波形看，PM 相对载波有 −90° 或 +90° 的相移（取决于调制信号的正负）。FM 改变的是载波在单位时间内的周期数（也就是频率）：没有 BF 时，FM 与 PM 都与载波同相。</p>
<p><b>解调：鉴频器（discriminateur）</b>把待解调信号的频率变化变成低频电压的变化。要注意一个与 AM 截然不同的特点：当输入端同时存在两个信号时，<b>只有最强的那个会被解调</b>，而不像 AM（以及 BLU）那样两个信号都会被检出来。常见的实现：</p>
<ul>
<li><b>斜率检波器（détecteur de pente）</b>：一个滤波器的谐振频率被特意偏离载波频率，使 FM 信号落在滤波器裙边最线性的一段（通常位于谐振频率以下），于是调频就被滤波器的传递函数变成调压。</li>
<li><b>Travis 鉴频器</b>：原理同斜率检波器，但线性更好。它用两个振荡回路分别针对两个极值频偏（平衡变换器）。当待解调频率接近 FI – δF 时，A 点的电压高于 B 点。</li>
<li><b>Foster-Seeley 鉴频器</b>：靠输出振荡回路中电容 C 引入的相移来解<b>调相</b>（PM）。</li>
<li><b>现代鉴频器用 PLL 环</b>：把 FM 信号与 VCO 来的高频信号相比较，经过一个低通滤波器，输出信号既是低频输出，又去控制 VCO 的频率。</li>
</ul>
<p>鉴频器在输入端没有信号时自己会输出噪声。为了压掉这种「沙沙声」，机内设<b>静噪（squelch，也叫 silencieux）</b>：在没有高频（或高频电平太低）时切断 FI 之后某一 AF 级的供电。此外，FI 输出端的<b>限幅器（limiteur）</b>把 FM 或 PM 信号上因寄生干扰而来的幅度变化削平，保护鉴频器不被扰动。</p>
<p><b>调频调制器</b>是一个<b>电抗振荡器（oscillateur à réactance）</b>，把低频的变化变成频率（或相位）的变化：图中的电抗由一个电容式话筒配 LC 回路产生，或由一只<b>变容二极管（Varicap）</b>产生。若采用 PLL 环，频偏和中心频率可以很方便地由 VXO 和可编程分频器调整；低频是经过一个截止频率很低（小于 10 Hz）的低通滤波器之后才注入的。</p>
<p><b>调制指数与带宽。</b><b>调制指数（indice de modulation）m</b>等于频偏除以最高调制频率：</p>
<div class="formula">m = 频偏 (Hz) / BF maxi (Hz)</div>
<p><b>卡森规则（règle de Carson）</b>用来估算调频信号<b>98% 调制功率</b>所占据的带宽：</p>
<div class="formula">B = 2 (m + 1) · BF maxi</div>
<p>当调制指数降到 1 以下（即 NBFM，窄带调频）时，带宽就偏离卡森公式而向 AM 的带宽（两条边带的宽度）靠拢，信噪比（S/B）明显下降，传输质量变差（尤其是高音部分发噪）。为降低这种噪声、提高信噪比，可以在调制器之前加一个<b>预加重器（préaccentuateur）</b>把高音提升；接收端的 FM 解调器则由<b>限幅器 + 鉴频器 + 去加重器（désaccentuateur）</b>组成，去加重把低频还原成发射前的样子。</p>
<p>信号经过<b>倍频器（multiplicateur de fréquence）</b>后，频偏和调制指数都会随之改变：一个 FM 信号经过二倍频器，频偏和调制指数都加倍（频偏加倍，而调制频率不变）。</p>
<p>原文例题：一个发在 144 MHz 的 FM 信号，频偏为 7,5 kHz，低频谱覆盖 300 到 3000 Hz，求调制指数。</p>
<div class="formula">m = 频偏 / BF maxi = 7,5 kHz / 3000 Hz = 7,5 / 3 = 2,5</div>
<div class="note"><b>本节编号提示：</b>本卷原文的对应关系是 §12.3 = 调幅（AM）、§12.4 = 调频（FM/PM）、§12.5 = 电报（CW）、§12.6 = 单边带（BLU）。复习时按「内容」而不是按小节号对号入座。</div>
<div class="warn">⚠️ 待核实：原文说调制指数小于 1（NBFM）时带宽「偏离卡森规则而接近 AM 的带宽」，但没有给出此时应使用的替换公式；考试中窄带 FM 的带宽取值须对照官方大纲与官方题解核实。</div>""",
    },
    {
        "id": "T125",
        "ref": "12.5",
        "title_zh": "电报（CW）：载波通断键控的几种做法",
        "title_fr": "La manipulation pour coupure de porteuse (CW)",
        "body": """<p>CW 即「载波通断键控」（manipulation pour coupure de porteuse），英文 Continuous Waves，法文译作 ondes entretenues（等幅波）。这个说法源自 1910 年代：当时的发射技术从产生<b>阻尼波（onde amortie）</b>的火花隙（éclateur）——阻尼波覆盖的频率范围非常宽——过渡到产生纯净得多的<b>等幅波</b>的振荡器。正是等幅波技术推动了 20 世纪初无线电报（TSF）的发展。</p>
<p>键控（调制）可以在不同位置断开供电来实现：振荡器、中频级、末级功放；也可以在两级之间断开连接来实现。</p>
<ul>
<li>断开<b>振荡器</b>的供电会损害振荡器的稳定性，接收端会听到「吱叫声」（piaulements）；</li>
<li>在<b>两级之间</b>键控则会使后级的负载阻抗发生很大变化，接收端会听到「咔嗒声」（claquements）。</li>
</ul>
<p>CW 的解调方式与 BLU 相同（见下一节，即用 BFO）。</p>""",
    },
    {
        "id": "T126",
        "ref": "12.6",
        "title_zh": "单边带（BLU/SSB）与各类发射的占用带宽",
        "title_fr": "La Bande Latérale Unique (BLU)",
        "body": """<p><b>BLU 是调幅的一种形式。</b>AM 的载波不携带任何低频信息，低频信号出现在载波频率的两侧：BF 与载波相混，得到「载波 + BF」与「载波 – BF」，也就是说同一份信息在两条边带里各出现一次。为减小占用频谱和发射功率，只保留其中一条：<b>BLI = LSB</b>（lower side band，下边带），<b>BLS = USB</b>（upper side band，上边带）。注意：这两条边带不是 AM 时域图上包络的上下两半。</p>
<p><b>频谱。</b>在 BLS 中，发射出去的低频谱从 200 Hz 延伸到 3 kHz；在 BLI 中低频谱是<b>反转的</b>（高低音对调），解调时必须把它「翻回来」，否则听起来完全无法理解。BLU 只是把低频谱整体搬移到更高的频率上。</p>
<p><b>功率关系。</b>当 K = 100%（最好情况）时，载波电压是每条边带电压的两倍：载波占发射功率的 <b>2/3</b>，两条边带占其余部分。原文例子：发射 150 W 且 K = 100% 时，载波占 100 W，每条边带占 25 W——所以边带功率最好时也比载波功率低 <b>6 dB</b>（即四分之一）。这就是 BLU 要抑制载波、只发一条边带的理由。</p>
<p><b>怎样产生 BLU。</b><b>平衡混频器（mélangeur équilibré）</b>先产生双边带 DBL（BLI + BLS），再由<b>石英晶体滤波器（filtre à quartz）</b>滤出想要的那条边带。没有低频信号时输出变压器是平衡的，也就没有高频输出；有低频信号时平衡被打破，高频（DBL）就通过。二极管环形混频器（4 引脚封装，内含 4 只二极管和变压器）把两路输入电压相乘，输出只有 f1 + f2 与 f1 – f2，二极管用肖特基（Schottky）型；它的三个缺点是：噪声系数带来约 10 dB 的损耗、需要在一路输入上给一个强信号（例如本机振荡器）、必须按厂家规定的阻抗（通常是 50 Ω）加载。滤波器必须很陡：当低频谱取 200 Hz 到 3000 Hz 时，BLI 与 BLS 之间只相隔 400 Hz，相邻信号要被压到 –60 dB。</p>
<p><b>解调。</b>解调 CW 与 BLU 的器件叫 <b>BFO（拍频振荡器）</b>：一个频率接近待解调信号的固定振荡器，用来把发射时被抑制掉的载波恢复出来，以产生 AM 或产生可听的 CW 音；BFO 的混频器后面接一个 AM 检波，整体就叫<b>乘积检波器（détecteur de produit）</b>。CW 中，FI 与 BFO 之差给出可听音（约 800 Hz）；BLU 中，BFO 频率等于被抑制载波的频率（没恢复在正确频率上时对方声音会明显变调，但仍能听懂）。收发信机显示的是<b>载波频率</b>：原文例子里 CW 是 7,030 MHz、BLI 是 7,200 MHz（被抑制载波的频率），这意味着<b>BLU 在显示频率上其实没有任何发射</b>，而 CW 的发射正发生在显示频率上。</p>
<p><b>直接变换接收机（conversion directe）</b>：本机振荡器频率接近接收频率，混频器输出就是调制信号本身，没有 FI 级，也就没有镜像频率问题；但它需要增益至少 100 dB 的 AF 放大器，而且只能解调幅度类调制（AM、BLU），角调制（FM、PM）要先用 I-Q 解调器和声卡作数字处理。</p>
<p><b>各类发射的占用带宽小结</b>（数字取自本块原文，原文没给的已在表中注明）：</p>
<table>
<thead><tr><th>发射类别</th><th>频谱构成</th><th>占用带宽</th></tr></thead>
<tbody>
<tr><td>CW 电报</td><td>载波的通与断</td><td>最窄（原文未给具体数值）</td></tr>
<tr><td>AM 调幅</td><td>载波 + 两条边带（HF ± BF）</td><td>约为最高调制频率的两倍（原文未直接写出该公式）</td></tr>
<tr><td>BLU / SSB</td><td>只有一条边带：低频谱 200 Hz 到 3 kHz 整体平移</td><td>一条边带的宽度（200 Hz 到 3 kHz）；与相邻边带相隔 400 Hz</td></tr>
<tr><td>FM 调频</td><td>以载波为中心的连续谱</td><td>B = 2(m + 1) · BF maxi（卡森规则，含 98% 功率）；频偏低时约等于 2 × 频偏</td></tr>
</tbody>
</table>
<div class="warn">⚠️ 待核实：本块原文并未给出各类发射占用带宽的<b>法定上限</b>（那属于法规章节的内容），上表只比较各项的构成关系；另外 CW 与 AM 的带宽数值在原文中也没有明确写出，考试请以官方大纲与官方题解为准。</div>""",
    },
]

# 该块真题的中文翻译，键为题号：{"题号": ("中文题目", "正确选项的中文")}
QT = {
    # T114 §11.4
    "21326": ("图中标注的这一级是什么？", "谐波滤波器（filtre anti-harmonique，也叫 filtre en PI）"),
    # T115 §11.5
    "20215": ("图中标注的这一级是什么？", "射频放大器（ampli RF）"),
    "20436": ("图中标注的这一级是什么？", "射频放大器（amplificateur RF）"),
    "20569": ("发射机框图为：话筒 – 平衡混频器 – 滤波器 – ? – 天线，缺的是哪一级？", "射频放大器（amplificateur RF）"),
    "20889": ("框图中缺的是哪一级？话筒 – ??? – 射频功放 – 天线", "振荡器（oscillateur）"),
    # T117 §11.7
    "20599": ("互调（intermodulation）的来源是什么？", "幅度失真（distorsion d'amplitude，即非线性级造成的失真）"),
    "20880": ("接收机采用低噪声系数（facteur de bruit faible）有什么好处？", "提高灵敏度（augmente la sensibilité）"),
    # T121 §12.1
    "20218": ("图中表示的是哪种调制方式？", "CW（载波通断键控的电报）"),
    "20354": ("这是哪种调制方式？", "调频（FM）"),
    "20854": ("测量发射时占用带宽（bande occupée）用哪种仪器？", "频谱分析仪（analyseur de spectre）"),
    "21212": ("这是哪种调制方式？", "调频（FM）"),
    # T122 §12.2
    "20372": ("图中标注的这一级叫什么？", "振荡器（oscillateur，调制器就是围绕它构成的）"),
    "21216": ("这个接收机能接收哪一种调制？", "调频（FM，因为图中有鉴频器 discriminateur）"),
    "21219": ("这个调制器能产生哪一类发射？", "单边带（BLU，即本机振荡器 + 平衡混频器 + 石英晶体滤波器）"),
    "21420": ("图中标注的这一级叫什么？", "乘积检波器（détecteur de produit，即 BFO 混频后再作 AM 检波）"),
    # T123 §12.3
    "20221": ("该框图表示的是哪种设备？", "外差式 AM 接收机（un récepteur hétérodyne AM；hétérodyne 即有中频 FI 的）"),
    "20229": ("（图）调制波形的最大电压为 10 V、最小电压为 5 V，求调制深度（taux de modulation）。", "33 %"),
    "20231": ("在外差式接收机中，CAG（自动增益控制）这一功能起什么作用？", "取代手动的话音（音频）电平控制，即由 CAG 自动控制增益"),
    "20332": ("这个电路产生的是哪种调制？", "调幅（modulation d'amplitude；图上是普通混频器，不是后接石英晶体滤波器的平衡混频器）"),
    # T124 §12.4
    "20225": ("框图中的接收机是哪种类型？", "FM 接收机（récepteur FM，因为有鉴频器）"),
    "20226": ("图中「放大器 + 振荡器」的电路表示什么？", "调频调制器（modulateur de fréquence，即电抗振荡器）"),
    "20308": ("框图中缺的是哪一级？", "倍频器（multiplicateur de fréquence）"),
    "20554": ("一张很复杂的框图（约占一整页、约 8 个单元，其中有倍频器、VCXO、低通滤波器，像是 PLL 环路；没有天线也没有扬声器），缺的是哪个元件？", "低通滤波器（filtre passe-bas）"),
    # T126 §12.6
    "20209": ("图中标注的这一级是什么？", "乘积检波器（détecteur de produit；乘积检波器总是与 BFO 配套）"),
    "20340": ("一张 BLU 接收机的框图，标注为 ? 的那一级（BFO 的位置）是什么？", "拍频振荡器（BFO）"),
    "20561": ("用平衡混频器构成的电路可以调制出什么？", "单边带（bande latérale unique，BLU；平衡混频器先产生 DBL，再经石英晶体滤波器取出一个边带）"),
    "20753": ("下面哪一组对应关系是正确的？", "BLI = LSB（下边带 = lower side band）"),
}
