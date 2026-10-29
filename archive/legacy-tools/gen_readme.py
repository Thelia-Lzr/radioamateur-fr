#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ecrit ../README.md avec les statistiques reelles des fichiers produits.
import csv, json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..'))
sys.path.insert(0, BASE)
from gen_common import load_questions, questions_by_anchor     # noqa: E402


def size(p):
    try:
        return '%.1f KB' % (os.path.getsize(p) / 1024.0)
    except OSError:
        return '（缺失）'


def main():
    plan = json.load(open(os.path.join(BASE, 'plan.json'), encoding='utf-8'))
    units = plan['units']
    idx = questions_by_anchor()
    qs = load_questions()['questions']
    nsec = len(units)
    nanch = len([a for a in idx if a])
    nq = sum(u['nq'] for u in units)
    ntrans = 0
    for name in ('W1', 'W2', 'W3', 'W4', 'W4b', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11'):
        p = os.path.join(BASE, 'content_%s.py' % name)
        if os.path.exists(p):
            sys.path.insert(0, BASE)
            import importlib
            try:
                ntrans += len(getattr(importlib.import_module('content_' + name), 'QT', {}))
            except Exception:
                pass
    nvocab = 0
    vpath = os.path.join(ROOT, 'vocabulaire.csv')
    if os.path.exists(vpath):
        with open(vpath, encoding='utf-8') as f:
            nvocab = max(0, sum(1 for _ in f) - 1)
    html_path = os.path.join(ROOT, 'manuel-zh.html')
    doc = open(html_path, encoding='utf-8').read() if os.path.exists(html_path) else ''
    nwarn = doc.count('class="warn"')

    txt = f"""# 法国业余无线电操作员证书（CEPT/HAREC）中文备考教材

为一位置身法国、母语中文、法语约 B1、已持中国 A 类操作证（30–3000 MHz、25 W）
的学习者整理的一套备考材料。全部内容以法国 F6KGL 的官方备考教材《COURS》
（2025 年 11 月版）为事实来源，用中文讲解，关键术语中法对照，
并与 2692 道法国考试真题（Exam'1 题库）逐题对应。

## 1. 文件清单

| 文件 | 大小 | 说明 |
|---|---|---|
| `manuel-zh.html` | {size(html_path)} | **主体教材**。单文件、自包含（CSS 内联，不联网、不依赖任何外部资源）。顶部有可点击目录；正文按 F6KGL 章节编号组织，共 **{nsec} 节**，覆盖题库里用到的 **{nanch} 个锚点**；每节末尾有「高频考点」框，内含 {ntrans} 道真题的法语原题、中文译文与答案（答案折叠，可自测）。附录含考试战术、公式速查、Q 简语表、国际字母解释法、高频词汇、锚点索引与待核实清单。 |
| `vocabulaire.csv` | {size(vpath)} | **Anki 可导入词表**，共 **{nvocab} 条**，按频次降序。6 列：`Français,中文,词性/类别,频次,所属主题,备注`。 |
| `README.md` | 本文件 | 使用说明、来源与许可、免责声明。 |
| `source/` | — | 素材与生成脚本（见下）。 |

## 2. 来源与许可

- **教材正文**：F6KGL《COURS de préparation au certificat d'opérateur du service amateur》
  2025 年 11 月版，作者 F6KGL / F5KFF 无线电俱乐部，
  **许可：Creative Commons BY-NC-SA 4.0**（署名 — 非商业性使用 — 相同方式共享）。
  本教材是它的中文改写，因此同样以 **CC BY-NC-SA 4.0** 发布：
  **不得用于商业用途**，转载或再改编时必须署名原作者并采用相同许可。
  原文：<http://f6kgl.free.fr/COURS.html>
- **题库**：Exam'1 —— 法国业余无线电考试模拟软件，由 F4JTV 在 GitHub 上以 Python3 +
  PyQt5 重写维护的开源项目（原版由 F5AXG 等人编写）。
  本教材所用的 `questions.json`（2692 题）与其中的题号、注释均出自该项目。
  仓库：<https://github.com/F4JTV/Exam1>
- **法规原文**：法国的考试大纲与频段划分来自 *arrêté du 21 septembre 2000*（附件 1，
  2021 年 3 月 2 日修订）、ARCEP 决定 12-1241（经 13-1515、19-1412 修改）与 ANFR 的
  TNRBF 频谱划分表。本教材只是二手整理，**不具备法律效力**。

## 3. 怎么配合 EXAM1 用

题库与教材是**同一套锚点体系**：`questions.json` 里每道题的 `cours` 字段形如
`http://f6kgl.free.fr/COURS.html#R21b`，井号后的 `R21b` 就是锚点。教材每节标题右侧
都标了同样的编号，附录 F 还给了完整的「锚点 ↔ 小节 ↔ 题量」索引表。

**用法一：顺着教材读。**
按目录顺序读（法规 R-1 → R-5，技术 0 → 12）。每节末尾的「高频考点」先自己答，
再展开答案——答案下面还有 Exam'1 题库自带的法语注释（`commentaire`），
它经常直接点出这道题的陷阱。

**用法二：哪里错得多补哪里。**
用 Exam'1 做题（`python3 Exam1/main.py`），把做错的题记下 `num`，在
`questions.json` 里查出它的 `cours` 锚点，再用附录 F 跳到教材对应小节。

**用法三：按题量分配精力。**
教材开头有「章节权重」表。备考时间有限时，优先吃透这几个锚点：
`#R21b`（频段划分，245 题）、`#R32a`（Q 简语，125 题）、`#R47b`（呼号国别，118 题）、
`#R12a`（发射类别，116 题）、`#R31`（字母解释法，102 题）——这五个加起来约占全题库的四分之一，
而且全部是「背了就得分」的题。

**用法四：模拟与自测。**
Exam'1 自带「按章练习」「系列练习」「模拟考试」三种模式。
模拟考试时按真实节奏练：法规卷 15 分钟、技术卷 30 分钟，
**每卷 20 题、10/20 及格、答错不倒扣（所以绝不能空题）**。

## 4. 素材与脚本

`source/` 目录：

| 文件 | 作用 |
|---|---|
| `cours.txt` / `cours_utf8.html` | F6KGL 教材原文（法文） |
| `Exam1/` | Exam'1 项目（含 `questions/questions.json`，2692 题） |
| `vocab_freq.txt` | 词频表 |
| `gen_common.py` | 公共函数：解析锚点、清洗 PDF 转文本、按锚点取题 |
| `make_plan.py` | 把教材切分为 {nsec} 个撰写单元，选出每节的示例题，生成 `plan.json` 与 `work/` |
| `SPEC_REDACTION.md` | 撰写规范 |
| `content_*.py` | 各分块的中文正文与真题译文 |
| `content_front.py` / `content_back.py` | 前言与附录 |
| `build_vocab.py` / `gen_vocab.py` | 词表候选提取与合并 |
| `gen_manuel.py` | 生成 `manuel-zh.html` |
| `gen_readme.py` | 生成本文件 |

重新生成：

```bash
cd source
python3 make_plan.py      # 只在素材变动时需要
python3 gen_vocab.py
python3 gen_manuel.py
python3 gen_readme.py
```

## 5. 免责声明

- 本教材是**学习辅助材料，不是官方文件**，与 ANFR（Agence Nationale des Fréquences）、
  Arcep、ARCOM 及任何官方机构无关。
- 教材内容以 F6KGL《COURS》2025 年 11 月版为准；**法规随时可能修订**，
  `manuel-zh.html` 附录 G 汇总了正文中标注「⚠️ 待核实」的全部条目。
- 报考、缴费、呼号申请、频段与功率限制等，**一律以 ANFR 官方文件与现行
  *arrêté* 为准**：<https://www.anfr.fr/>
- 题库中的题目来自 Exam'1 开源项目，官方题库可能已有增减；
  考试成绩以官方为准。
- 报告中若出现任何数字/法条与官方文件不一致，请以官方文件为准，并欢迎指出以便修订。

---

生成时间：{datetime.date.today().isoformat()}　·　正文 {nsec} 节　·　
覆盖真题 {nq} 道／{len(qs)} 道　·　词表 {nvocab} 条　·　待核实标记 {nwarn} 处
"""
    out = os.path.join(ROOT, 'README.md')
    open(out, 'w', encoding='utf-8').write(txt)
    print('-> %s (%s)' % (out, size(out)))


if __name__ == '__main__':
    main()
