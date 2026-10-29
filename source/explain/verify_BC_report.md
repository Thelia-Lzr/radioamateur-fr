# 看图核对报告：分块 B / C 共 38 条

核对方式：逐条用 `vision_analyze` 读取 `/home/thelia/Documents/radioamateur-fr/source/Exam1/questions/<题号>.png`（多张一批），
再与 `part_B.json` / `part_C.json` 的讲解逐句比对。答案侧另与 `Exam1/questions/questions.json` 的
`reponse`（0 基）与 `commentaire`（官方注释）对照，确认讲解给出的结论就是标准答案。
部分图（频谱横轴、波形串长、扬声器/话筒符号）做了裁剪放大二次判读。

**合计 38 条：符合 33 条，已改 5 条（20150、20308、20310、20320、20332）。**
图片均清晰可辨，没有看不清或无法判断的题；下面 5 条是图面事实与讲解不符，其余 33 条图面数据与讲解一致。

---

## 一、逐题清单

| 题号 | 图面关键内容（照实转录） | 结论 |
|---|---|---|
| 20127 | 标题 Impédance à la résonance ?；串联 RLC：电感 16 µH — 电容 400 nF — 电阻（方框）8 Ω | 符合（串联谐振 Z=R=8 Ω，与选项 1 一致） |
| 20128 | Facteur de Qualité ?；L=32 mH、R=8 kΩ、C=200 pF（C 与 L+R 两路并联） | 符合（Q=√(32000/200)/8=1.58，与官方一致） |
| 20129 | Facteur de Qualité ?；L=20 µH、R=2,5 Ω、C=500 pF | 符合（Q=0.2/0.0025=80，与选项 3 一致） |
| 20130 | Bande passante = ?；并联 LC：L=10 µH、C=10 pF，旁注 Q=150 | 符合（F=159/√100=16 MHz、B=107 kHz，与选项 3 一致） |
| 20134 | Facteur de sélectivité ?；纵轴 0 dB / −3 dB / −60 dB，横轴 3550、3590、3600、3610、3650；峰在 3600 的 0 dB，−60 dB 处为 3550 与 3650 | 符合（(3650−3550)/(3610−3590)=100/20=5，与选项 4 一致） |
| 20150 | 标题 Taux de distorsion de l'harmonique 3；三根谱线高 10 V、4 V、2 V，横轴刻度只有 **0,5 / 1,0 / 1,5**（未注单位） | **已改**：原讲解把横轴读成 5/10/15 MHz，与图面刻度不符 |
| 20151 | 三根谱线高 10 V、4 V、3 V，横轴刻度 **5 MHz / 10 MHz / 15 MHz** | 符合（4/10=40%、3/10=30%、√(0.4²+0.3²)=50%，与选项 4 一致） |
| 20153 | 混频器圆圈内画 X，左输入 Entrée = 650 kHz，下方 OL = 1,1 MHz，右输出无标注 | 符合（1750 与 450 kHz，取差频 450 kHz＝选项 2） |
| 20154 | 同一混频器符号，Entrée = 650 kHz，OL = 1 MHz，输出无标注 | 符合（1650 与 350 kHz，取 350 kHz＝选项 3） |
| 20155 | 纯文字：amplificateur RF à distorsion quadratique，F1=145 MHz、F2=150 MHz | 符合（六项 5/145/150/290/295/300＝选项 2） |
| 20157 | 三角形放大器符号，标注 Ampli RF à distorsion quadratique，输入 50 MHz 与 55 MHz | 符合（105、5、100、110、50、55＝选项 1） |
| 20158 | 纯文字：mélange du 3ème ordre，F1=145 MHz、F2=150 MHz | 符合（2F1−F2=140 MHz＝选项 4） |
| 20159 | 纯文字：mélange du 3ème ordre，F1=145 MHz、F2=160 MHz | 符合（2F2−F1=175 MHz＝选项 3） |
| 20186 | 纯文字（无图）：Au centre d'une antenne doublet demi onde, quelles sont les valeurs de U et de I ? | 符合（中心 U 最小、I 最大＝选项 2；讲解也点出「最小而非严格为零」） |
| 20187 | 四个小图：半波天线外框，内画一实线一虚线正弦（反相）。图 1 标 U（实）与 I（虚）；图 2 标 −U 与 I；图 3、图 4 标 I 与 U（U、I 对调） | 符合（取第 1 图＝选项 1，单半周且端点 U 最大、I 最小） |
| 20188 | 传输线左端 10 W，右端接八木天线，旁注 16 dBi | 符合（10×40=400 W PIRE＝选项 4） |
| 20191 | 图题 Affaiblissement linéique ?；粗横条左端 40 W、右端 10 W，上方双箭头标 30 mètres | 符合（−6 dB / 30 m = 0,2 dB/m＝选项 4） |
| 20194 | 图题 Affaiblissement linéique ?；粗横条左端 20 V、右端 5 V，上方标 30 mètres | 符合（电压比→12 dB / 30 m = 0,4 dB/m＝选项 3） |
| 20195 | 纯文字：Quelle est l'impédance de cette ligne coaxiale ? C = 20 pF/m et L = 50 nH/m | 符合（√(L/C)=50 Ω＝选项 1） |
| 20196 | 图题 Quel est le ROS ?；双线传输线上方 Pr = 1 W（箭头向左），下方 Pi = 4 W（箭头向右） | 符合（k=0.5→ROS=3＝选项 3） |
| 20197 | 图题 Quel est le ROS ?；线左端 Ze = 50 Ω，右端接天线 Za = 75 Ω | 符合（75/50=1,5＝选项 4） |
| 20198 | 图题 Quelle est la puissance réfléchie ?；方框内 50 W，线右端接天线，线下方 ROS = 2 | 符合（k=1/3、Pr=50/9≈5,5 W＝选项 3） |
| 20199 | 图题 Quelle doit être l'impédance de la ligne quart d'onde…；Longueur du câble = lambda/4，左端 Ze = 300 Ω、右端 Za = 50 Ω | 符合（√(300×50)≈122 Ω＝选项 3） |
| 20204 | 天线 → RF → Mél(OL 在下) → FI → Dét. → **?** → HP（HP 仅文字）；CAG 由 RF 右出、接到 Dét. 上方 | 符合（? 在检波后、喇叭前＝amplificateur AF＝选项 1） |
| 20205 | 天线 → **?** → Mél(OL 在下) → Ampli FI → Dét. → AF → HP；CAG 由 Ampli FI/Dét. 节点回接 ? | 符合（? 为 ampli RF＝选项 4；讲解也注明「premier ampli」不够精确） |
| 20207 | 天线 → RF → Mél(VFO 在下) → FI → Mél(OL 在下) → **?** → Démodul. → AF → HP | 符合（第二中频放大 ampli FI＝选项 1） |
| 20208 | 天线 → RF → Mél(VFO) → FI → Mél(OL) → FI → Démodul. → AF → HP，无 ? 框 | 符合（双变频接收机＝选项 3） |
| 20215 | 话筒（圆圈+黑方块）→ AF → Mod（下方圆圈 OL）→ **?** → 天线 | 符合（ampli RF＝选项 4） |
| 20218 | 时域波形：等幅等频载波三段断续出现，前两段短、第三段明显最长（摩尔斯 U），段间为零电平 | 符合（CW＝选项 3；讲解「一串短、一串短、一串长」经放大复核无误） |
| 20221 | 天线 → RF → Mél(VFO 在下) → FI → Détection → AF → HP，无 ? 框 | 符合（超外差 AM 接收机＝选项 1） |
| 20229 | 图题 Quel est le taux de modulation ?；框内调幅波，上方虚线 10 V、下方虚线 5 V，横轴 t | 符合（(10−5)/(10+5)=33%＝选项 2） |
| 20308 | 扬声器符号（喇叭口朝左）→ Ampli BF → Préaccentuateur → VCXO →（长回线）**?** → Mél.(OL 在下) → Ampli RF → 天线，旁边写 Modulation de fréquence | **已改**：图上输入端是扬声器 HP，原讲解写「图上有话筒」 |
| 20310 | 天线 → RF → Détecteur d'enveloppe（方框内只有文字，未画二极管+RC）→ AF → HP | **已改**：原讲解把「二极管加 RC」当作图面内容 |
| 20313 | 图题 Résistance équivalente ?；30 Ω 与 15 Ω 两方框上下叠放，左端互连、右端互连＝并联，下方双箭头标 Req = ? | 符合（积比和 450/45=10 Ω＝选项 1） |
| 20315 | 图题 Quelle est la puissance minimum pour la résistance ?；单一 33 Ω 方框，下方箭头标 12 V | 符合（144/33≈4,36 W→取 5 W＝选项 4） |
| 20316 | 图题 Taux de distorsion de l'harmonique 3；三根谱线 F=10 V、2F=2 V、3F=1,5 V | 符合（1,5/10=15%＝选项 3；2 V 为干扰量） |
| 20320 | 图上无器件符号，只有编号说法表：1) un drain、2) une source、3) un collecteur、4) une base、5) un émetteur、6) une gâchette、7) une porte、8) une anode | **已改**：原讲解说「图上按编号画出各种器件的符号」并让人「认准符号形状」，与图不符，且未给出编号答案 |
| 20325 | 天线 → RF → Mél(VFO 在下) → **?** → Démod. → AF → HP | 符合（? 夹在混频器与解调器之间＝amplificateur FI＝选项 2） |
| 20326 | 图题 Quelle est la puissance réfléchie ?；方框内 9 W，线右端接天线，线下方 ROS = 2 | 符合（k=1/3、9×0.11≈1 W＝选项 4） |
| 20332 | Micro → Ampli AF → Mél.(OL 在下) → 右端引出线标 ?（无载波、无平衡混频器、无石英滤波器） | **已改**：原讲解说「图上是一个简单的单管混频器」，图上只是方框图，未画晶体管 |
| 20340 | 天线 → RF → Mél(VFO 在下) → FI → Mélangeur de produit → AF → HP，**?** 框接在 Mélangeur de produit 下方 | 符合（BFO＝选项 4；讲解也点出与乘积检波器成对出现） |
| 20353 | 图题 Calculer l'intensité I；75 Ω 与 175 Ω 两方框首尾相接（串联），中间箭头标 I，下方长箭头标 UT = 25 V | 符合（250 Ω→100 mA＝选项 3） |
| 20355 | 图题 Quelle est la valeur équivalente ?；两只线圈首尾相接（串联），左 12 µH、右 8 µH，无耦合点/耦合箭头 | 符合（12+8=20 µH＝选项 2；讲解已指出官方注释把「串联」误写成并联） |
| 20360 | 图题 Quelle est l'impédance du câble ?；同轴截面，芯线（斜线填充）标 d = 3 mm，外导体标 D = 10 mm | 符合（138·log(10/3)≈72 Ω＝选项 4） |
| 20361 | 天线 → **?** → mélangeur → détecteur → AF → 扬声器符号；CAG 由 mélangeur 下方接回 détecteur，无 OL/VFO、无 FI | 符合（? 在天线与混频器之间＝filtre＝选项 4） |
| 20362 | Micro → Ampli Audio → modulateur d'amplitude → Ampli FI → Mélangeur（下方 OL）→ **?** → 天线 | 符合（ampli RF＝选项 1；讲解也指出 filtre réjecteur 同样说得通） |
| 20372 | 三个方框：AF → **?** → RF | 符合（oscillateur＝选项 4） |

---

## 二、被改的 5 条：原讲解的问题与新讲解要点

### 20150（原讲解：把横轴读成 5/10/15 MHz）
- 图面事实：横轴刻度逐字为 `0,5` `1,0` `1,5`（三点，且**没有** MHz/kHz 单位），三根谱线高 10 V、4 V、2 V。
  放大 3 倍裁剪复核确认不是 5/10/15。官方注释也用 `F1 (0,5)`、`F3 (1,5)` 指代。
- 问题：原讲解写「5 MHz 处为 10 V（基波），10 MHz 处 4 V，15 MHz 处 2 V」，比图面刻度大了十倍；
  同批 20151 的图才是 5/10/15 MHz，属两条题串图。答题结论（20%）本身没错。
- 新讲解要点：照实给出谱线高度 10/4/2 V 与刻度 0,5、1,0、1,5（并注明题图未注单位），
  仍按 \(TDH_3=2/10=20\%\) 推，保留 40%（二次谐波）陷阱与「分母是基波」的要点。

### 20308（原讲解：说图上有话筒）
- 图面事实：链路最左端画的是**扬声器**（喇叭锥形符号，口朝左），随后 Ampli BF → Préaccentuateur → VCXO；
  `?` 框夹在 VCXO 与 Mél. 之间，Mél. 下方接 OL，末尾 Ampli RF → 天线，另有文字 Modulation de fréquence。
  官方注释专门提醒「把 HP 当话筒用只是 bricolage」，即图上确实是喇叭而非话筒。
- 问题：原讲解第一句「图上有话筒、预加重网络与 VCXO」，话筒一项与图不符；
  另外没有点出 `?` 的具体位置（VCXO 与 Mél. 之间）。
- 新讲解要点：改正为扬声器 HP，写出完整链路与 `?` 位置，保留「FM 发射机 + 其余三选项只属接收机 + 缺倍频器」的推理。

### 20310（原讲解：把「二极管加 RC」当成图面内容）
- 图面事实：链路上只有三个方框：天线 → RF → **Détecteur d'enveloppe**（框内只有这两行文字）→ AF → HP；
  放大裁剪确认框内没有画二极管、电阻、电容。
- 问题：「图上解调级是二极管加 RC 的包络检波器」把原理性描述写成了图面内容（图上并无该电路）。
- 新讲解要点：改为「标着 Détecteur d'enveloppe 的方框，原理上就是二极管加 RC」，结论（只能收 AM）不变。

### 20320（原讲解：说图上画了器件符号）
- 图面事实：图上**没有任何器件符号**，只有一张编号说法表：
  1) un drain，2) une source，3) un collecteur，4) une base，5) un émetteur，6) une gâchette，7) une porte，8) une anode。
  标准答案为「3, 4 et 5」，即 collecteur、base、émetteur。
- 问题：原讲解写「图上按编号画出各种器件的符号与电极」「认准符号形状再取它标出的编号即可」，
  与图（纯文字编号表）不符；而且通篇没有给出实际编号 3、4、5，等于没把图面事实落到答案上。
- 新讲解要点：照实说明是编号说法表，直接给出 base/collecteur/émetteur 对应 3、4、5，
  再点出 drain/source/porte 属 FET、gâchette/anode 属晶闸管。

### 20332（原讲解：说图上是「简单的单管混频器」）
- 图面事实：方框图 Micro → **Ampli AF** → **Mél.**（下方 OL）→ 右端引出线标 `?`；
  图上没有任何晶体管符号，也没有载波抑制结构或石英滤波器。
- 问题：「图上是一个简单的单管混频器」是图上没有的器件级细节；
  官方注释的判断依据是「simple mélangeur（非平衡混频器）而非平衡混频器 + 石英滤波器」。
- 新讲解要点：改按方框图叙述（Micro → Ampli AF → Mél. → ?），仍推出「音频与载波直接混频→载波加双边带=调幅」，
  并保留 BLU 需要平衡混频器 + 石英滤波器的对比。

---

## 三、图片判读说明

- 38 张图全部存在且清晰可读，**没有一条**属于看不清或无法判断。
- 三处做了裁剪放大二次判读，以免误判：
  1. `20150` 横轴（3× 放大）→ 确认是 `0,5` `1,0` `1,5`，无单位；
  2. `20218` 波形（2× 放大）→ 确认前两串短、第三串最长、幅度相同（摩尔斯 U），原讲解无误；
  3. `20308` 输入端与 `20310` 解调框（3× 放大）→ 确认输入端为扬声器符号、解调框内只有文字。
- 另注（不改动，仅备查）：20186、20155、20158、20159、20195 的 PNG 实际只含题干文字、无图形，讲解正文已按题干数据展开，故仍判「符合」。

## 四、产出文件

- `/home/thelia/Documents/radioamateur-fr/source/explain/verify_BC_corrections.py`（FIX 5 条）
- `/home/thelia/Documents/radioamateur-fr/source/explain/verify_BC_corrections.json`（校验脚本导出）
- `/home/thelia/Documents/radioamateur-fr/source/explain/verify_BC_report.md`（本文件）
