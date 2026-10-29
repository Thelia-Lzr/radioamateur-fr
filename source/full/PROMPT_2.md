# 子任务说明书（第 2 批 · 分块撰写）

本文件对**任意部分 K** 都适用：若你被指定为第 K 部分（K = 1…6），则

- 输入：`/home/thelia/Documents/radioamateur-fr/source/full/in2_K.json`
- 输出：`/home/thelia/Documents/radioamateur-fr/source/full/out_part2_K.json`

**只读写这两个文件，不要动其它任何文件。** 用 `cat` 读完本文件后严格照做。

---

## 1. 背景

我们在为一位中文母语者做**法国业余无线电操作员证书**（CEPT/HAREC 级）的**中文备考材料**。
学习者法语约 B1，有无线电基础，持中国 A 类操作证（只熟 VHF/UHF，不熟短波）。
现在要把一批法国考试真题做「**中译 + 中文原理讲解**」（一趟完成两项）。

## 2. 输入格式

`in2_K.json` 是一个 JSON 数组，每条字段：

```json
{"num":"20321","theme_fr":"…","theme_zh":"交流电",
 "stem_fr":"法语题干","options":["选项1","选项2","选项3","选项4"],
 "ans_idx":2,"ans_fr":"正确答案","commentaire_fr":"官方注释(可能为空串)","anchor":"T022d"}
```

正确答案**以 `ans_idx` / `ans_fr` 为准**，不要自己重新判断对错（即使你觉得官方答案可疑，
也照它翻译，可在讲解里注明疑点）。

## 3. 输出格式

`out_part2_K.json`：一个 JSON 对象，**只含本部分的 num**（字符串键），值为：

```json
{"20321":{
  "stem_zh":"题干中译",
  "ans_zh":"答案(ans_fr)中译",
  "com_zh":"commentaire_fr 的中译；原文为空串则这里也必须是空串 \"\"",
  "explain":"中文原理讲解"}}
```

不要输出其它字段（不要 theme、options、anchor、num 副本）。

## 4. 翻译规则

1. **法语小数点逗号改成点**：`1240,000` → `1240.000`；`1,5` → `1.5`
2. **法语千位分隔点原样保留**：`14.000 kHz` 保持 `14.000 kHz`
3. **数字、单位、频率、呼号、波段名、公式原样保留**：`430 à 440 MHz` → `430 至 440 MHz`；
   `F4ABC` 不译；`23 cm` → `23 厘米`；乘号写 `×`；`µF / nF / pF / kΩ / MHz / dB / PAR / PIRE` 等原样
4. 题干全大写，中译时改回正常中文标点（，、？、：），不要保留大写腔调
5. 法规术语按考试语境：`partagée à égalité de droit`=平等使用权；`statut secondaire`=次要业务；
   `précaire et révocable`=临时且可撤销；`arrêté`=部令；`PIRE`=等效全向辐射功率；
   `PAR`=有效辐射功率；`balun / symétriseur`=平衡-不平衡变换器（巴伦）
6. **不许编造**。看不懂或信息不足（尤其只给了图的题）就照字面译，并在该字段末尾加
   `（⚠️待核）`，不要猜数字、不要补原文没有的参数
7. 常用电路术语对照：
   `résistance de charge`=负载电阻；`de contre-réaction`=负反馈；`d'équilibrage`=平衡电阻；
   `CAG`=自动增益控制（CAG）；`détecteur de produit`=乘积检波器；`circuit bouchon`=并联谐振回路；
   `filtre passe-bas`=低通滤波器；`passe-haut`=高通滤波器；`taux de sélectivité`=选择性系数；
   `TDH / taux de distorsion`=谐波失真率；`shunt`=分流电阻；`galvanomètre`=检流计；
   `pulsation`=角频率；`montage base commune`=共基极组态；`courant de repos`=静态电流

## 5. 讲解规则（重点，必须讲原理，不是背答案）

1. **先给结论**（一句话直接点明为什么是这个答案）
2. **能推就推**，把计算过程写出来。常用关系：
   \[\lambda(\text{m})=\frac{300}{f(\text{MHz})}\]，\[U=RI,\quad P=UI=RI^2=\frac{U^2}{R}\]
   串联电容 \[\frac{1}{C_T}=\sum\frac{1}{C_i}\]（n 只相同电容串联 \(C_T=C/n\)）；
   并联电阻 \[\frac{1}{R_T}=\sum\frac{1}{R_i}\]（两只 \(R_T=R_1R_2/(R_1+R_2)\)，n 只相同 \(R_T=R/n\)）；
   谐振 \[f=\frac{1}{2\pi\sqrt{LC}}\]（简化式 \(f(\text{MHz})=159/\sqrt{L(\mu H)\cdot C(pF)}\)）；
   分贝 \[\text{dB}=10\log_{10}(P_1/P_2)\]（+3 dB=×2，−3 dB=÷2，+10 dB=×10，−10 dB=÷10，+6 dB(电压/电流)=×2）；
   阻抗匹配 \(Z=\sqrt{Z_1Z_2}\)；RC 截止频率 \(f=1/(2\pi RC)\)（简化式 \(f(\text{Hz})=159/(R(\text{k}\Omega)\cdot C(\mu F))\)）
3. **点破干扰项**：说明另外几个选项错在哪（最常见错法：漏乘或漏除 2、√2 与 2 混用、
   把有效值当峰值、串并联搞反、单位数量级差 1000、公式用错）
4. **法规/规范题讲"为什么"**：例如分贝损耗为何可直接相加（对数→乘性→加性）；
   为什么标准功率电阻要取**上一档**（否则电阻过载烧毁）
5. **Q 简语/字母解释法类题给记忆钩子**（如 `QSL`=收据、"确认"；`QRZ`=谁在呼叫我）
6. **需要看图的题**（题干出现 `DESSIN / SCHEMA / SYNOPTIQUE / FIGURE / oscilloscope / 图` 等）：
   讲解开头写「**此题需看图**」，然后讲**看图方法**：从哪端读起（天线→RF→混频→FI→检波→AF），
   每个方框的作用，如何用题干文字描述反推出缺失的那一级
7. **长度 80～250 个汉字**（公式符号不计入），每条都要落在这个区间
8. **公式必须写成 `\( ... \)`（行内）或 `\[ ... \]`（独立行）**。
   **绝对不要用 `$...$`**（会被校验判为错误）。LaTeX 里不要用法语重音字母，
   峰峰值写 `U_{pp}`、`U_{càc}` 请写成 `U_{pp}`
9. 讲解里**不要**写"我""本助手""以上""下面"这类元话术，直接讲原理

### 讲解风格示例（第 20321 条）

> 输入：`stem_fr: "TENSION CRETE A CRETE D'UNE TENSION DE 12 VOLTS EFFICACES"`，
> `ans_fr: "34 volts"`，`commentaire_fr: "Umax = 12 V x 1,414 = 17 V (arrondi) ; Ucàc = Umax x 2 = 17 x 2 = 34 volts"`

```json
"20321":{
 "stem_zh":"有效值为 12 V 的交流电压，其峰峰值是多少？",
 "ans_zh":"34 V",
 "com_zh":"Umax = 12 V × 1.414 = 17 V（取整）；峰峰值 = Umax × 2 = 17 × 2 = 34 V",
 "explain":"先分清三个量：峰值 \(U_{max}\)、有效值 \(U_{eff}\)、峰峰值 \(U_{pp}\)。正弦波 \(U_{max}=\sqrt{2}\,U_{eff}\approx1.414\times12\approx17\) V；峰峰值是正峰到负峰的距离，\(U_{pp}=2U_{max}=34\) V。干扰项 24 V 是 12×2，把有效值当成峰值乘了 2；17 V 只是峰值；8.5 V 是 12/1.414，方向反了。记住链条：有效值 ×1.414 得峰值，峰值 ×2 得峰峰值。"}
```

## 6. 写盘方式（重要）

- 用 python 脚本写文件：`json.dump(obj, f, ensure_ascii=False, indent=1)`，
  中文直接写中文字符，**不要** `\uXXXX` 转义
- **分两次写盘**：先写前一半条目 → `json.load` 校验键数 → 再读回、补齐后一半 → 写回 →
  再 `json.load` 校验，并 `assert` 键集合与输入 num 集合**完全相等**（不缺不多）
- 允许用 `python3 - <<'EOF'` 的 heredoc 方式写脚本

## 7. 完成后回报

1. 输出文件路径与键数（应等于输入条数）
2. 带 `（⚠️待核）` 的题号清单（没有就说没有）
3. 你认为**最难讲清原理**的 1～3 个主题/题号
4. 任何你不确定的地方
