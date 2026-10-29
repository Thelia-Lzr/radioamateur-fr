#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次 7 第 5 盘：K104 / K105 补足，最后校验"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_7.json')
D = json.load(open(OUT, encoding='utf-8'))

# ---- K104 补：充放电时间常数 ----
D["K104"]["body"] = D["K104"]["body"].replace(
 "## 法国/欧盟视角",
 r"""## 充放电的时间常数
电容经电阻充电/放电时，同章给出时间常数 \\(T(s)=R(\Omega)\cdot C(F)\\)（简化式 \\(T(\text{ms})=R(\text{k}\Omega)\cdot C(\mu F)\\)）。充电时每个 T 走完剩余差额的约 2/3：1T 到 **63,21 %**（约 2/3）E，2T 到 8/9，3T 到 26/27，**5T 视为充满**（> 99 %）。放电时每过 T 只剩 1/3，5T 后残余不足 1 %。例：100 µF 经 8 kΩ 放电，T = 800 ms，放电完毕需 5T = **4 s**。电感对应的时间常数是 \\(T=L/R\\)，突然断电会产生数十倍的反向电压（楞次定律）。

## 法国/欧盟视角"""
)

# ---- K105 补：判据与量级 ----
D["K105"]["body"] = D["K105"]["body"].replace(
 "## 法国/欧盟视角",
 r"""## 判据与量级自检
1. 先看清"串联还是并联"：串联谐振 Z = R（很小），**并联（bouchon）谐振 Z = L/(RC)（很大）**；
2. 单位一律按简化式配好：**µH / pF / kΩ**，混用单位是最主要的失分点；
3. 若只给 L、C、Q 而不给 R，可用 \\(R=\sqrt{L/C}/Q\\) 反推，或用 \\(Z_{bouchon}=Q\sqrt{L/C}\\)；
4. 答案的"数量级"要合理：µH 与 pF 级元件配几欧姆损耗，并联谐振阻抗应是几十至几百 kΩ；若算出几十 Ω，几乎一定是把串联与并联搞反了。
另外教材提醒：**元件永远不完美**，线圈与电容都带有电阻分量（图中用虚线表示），所以谐振阻抗不会真的是零或无穷大。

## 法国/欧盟视角"""
)

json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

ok = True
for k in sorted(D):
    v = D[k]
    assert set(v.keys()) == {'title_fr', 'title_zh', 'front', 'body'}
    n = sum(1 for c in v['body'] if '\u4e00' <= c <= '\u9fff')
    flag = '' if 400 <= n <= 800 else '  <<< 超范围'
    if flag:
        ok = False
    print(k, '汉字', n, '| title_zh', len(v['title_zh']), '| front', len(v['front']), flag)
print('全部在 400~800:', ok)
print('知识点数:', len(D))
print('待核标记:', sum(v['body'].count('⚠️待核') for v in D.values()))
for k, v in D.items():
    if '⚠️待核' in v['body']:
        print('   ', k)
