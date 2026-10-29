# 写作规范（所有分块撰写子任务必读）

## 1. 背景与目标

我们要为一位**中文母语者**做一份**法国业余无线电操作员证书**
（certificat d'opérateur du service amateur，CEPT/HAREC 级）的**中文备考教材**。
学习者法语约 B1，有无线电基础，持有中国 A 类操作证（只有 VHF/UHF，**不熟短波**）。

教材内容以法国最权威的免费备考教材 **F6KGL《COURS》**（2025 年 11 月版，
CC BY-NC-SA 4.0）为唯一事实来源，用中文讲解，关键术语中法对照。

最终 HTML 由我（主协调者）统一生成；你只负责**你分到的那一段**的正文内容。

## 2. 你要读的文件

| 文件 | 内容 |
|---|---|
| `source/work/cours_W<块>.txt` | **你负责的原文**：F6KGL 教材该行段的法文原文（PDF 转文本后已按段落整理，每行一段，标题行以 `###` 开头） |
| `source/work/block_W<块>.json` | 你负责的**单元清单**：每个单元含 `id`、`ref`（如 `R-2.1.b`）、`nq`（该主题真题数量）、`depth`（详细程度）、`anchors`（题库锚点）、`questions`（需要你翻译的真题） |

**只依据 `cours_W<块>.txt` 的实际内容写作。** 原文没写的数字、频率、法条编号一律不许编。
法条编号（如「附件 1」「arrêté du 21/09/00」「décision 12-1241」）只在原文出现时才能引用。

## 3. 输出文件与格式

写到 `source/content_W<块>.py`（UTF-8，只写这一个文件，不要动别的文件）：

```python
# -*- coding: utf-8 -*-
# 中文教材正文：区块 W1

SECTIONS = [
    {
        "id": "R12a",              # 必须与 block json 的 id 完全一致
        "ref": "R-1.2.a",          # 原文编号（教材 § 号）
        "title_zh": "发射类别：三字符表示法",
        "title_fr": "Les classes d'émission",
        "body": """<p>正文 HTML…</p>""",
    },
    # …该块所有单元，顺序按 block json
]

# 该块真题的中文翻译，键为题号：{"题号": ("中文题目", "正确选项的中文")}
QT = {
    "20204": ("图中标注的这一级是？", "音频放大器（amplificateur AF）"),
}
```

**必须覆盖 block json 里列出的每一个 `id`，一个都不能少，顺序保持一致。**
`QT` 必须覆盖 block json 里出现的**每一个题号**。

## 4. 篇幅与详细程度（按 `depth`）

| depth | 题量 | 要求 |
|---|---|---|
| 1 | ≥20 题 | **重点章节**：700–1500 字，完整讲解 + 公式 + 表格，把考试要点讲透 |
| 2 | 8–19 题 | 中等：250–600 字，讲清概念与关键结论，可用要点列表 |
| 3 | <8 题 | 简写：100–300 字，只列要点（可用 `<ul>`），不必展开推导 |

## 5. 写作风格

- **中文讲解**，简体中文。术语首次出现用「中文（法文）」格式，例如
  「天线（antenne）」「有效辐射功率（puissance apparente rayonnée, PAR）」
  「临时且可撤销的（précaire et révocable）」。法文用**半角括号**，法文里的重音符号照写。
- 面向**已懂 VHF/UHF、但不熟 HF 短波与法国法规**的读者：
  短波/法规处多解释，纯电路基础处可提速。
- 凡是中国考试/实践里没有的概念（如业务地位 primaire / secondaire / à égalité de droit、
  HAREC、indicatif、carnet de station），必须解释清楚。
- 数字、单位、频率一定要**照抄原文**，写成原文的写法（如 `7,000 – 7,200 kHz`、
  `500 W`、`120 W`）。法语用逗号做小数点，可在中文里保留原样并加注。
- 公式用 `<code>` 或 `<div class="formula">`，等宽字体。
- **不要**写任何"我"、"本助手"、"以下"之类的元话术；直接写教材正文。

## 6. body 里允许的 HTML

只允许这些标签：`<p> <ul> <ol> <li> <table> <thead> <tbody> <tr> <th> <td> <b> <code> <em> <br>`，
以及这些带 class 的容器：

- `<div class="formula">…</div>` — 公式块（等宽）
- `<div class="note">…</div>` — 提示框
- `<div class="warn">⚠️ 待核实：…</div>` — **原文没讲清或你没把握的，必须用它标出**，
  写明"哪里不确定、需要向 ANFR 官方文件核实"。宁可标待核实，也**绝不编造数字或法条**。
- `<div class="tips">…</div>` — 考试提醒

不要写 `<h1>/<h2>/<h3>`（标题由生成器负责），不要写 `<html>/<body>`，
不要写内联 `style=`，不要写 `<script>`。

## 7. 质量红线

1. 不准编造频率、功率、时限、罚款金额、法条编号。原文没有就写「原文未给出」或标待核实。
2. 不准把中国法规套到法国（例如不要把中国的功率限值写成法国的）。
3. 法国功率限制、频段划分、呼号前缀等数字必须能在 `cours_W<块>.txt` 里找到出处。
4. 如果原文本身自相矛盾或明显是 PDF 转文本的错乱（比如数字粘在一起），标 `<div class="warn">`。

## 8. 自检（必须做）

```bash
cd /home/thelia/Documents/radioamateur-fr/source
python3 -c "
import json, content_W1 as m
plan = json.load(open('work/block_W1.json'))
ids = [u['id'] for u in plan['units']]
assert [s['id'] for s in m.SECTIONS] == ids, '单元不一致'
nums = [q['num'] for u in plan['units'] for q in u['questions']]
missing = [n for n in nums if n not in m.QT]
assert not missing, missing
for s in m.SECTIONS:
    assert s['body'].strip() and 'class=\"' not in s['body'].replace('class=\"formula','').replace('class=\"note','').replace('class=\"warn','').replace('class=\"tips','')
print('OK', len(m.SECTIONS), 'unites,', len(m.QT), 'traductions')
"
```

（把 `W1` 换成你的块号。）必须跑到输出 `OK`。

## 9. 汇报格式（回复中给出）

1. 生成的文件路径 + 大小
2. 单元数量，每个单元的 `id` 与中文标题
3. 你标了「⚠️ 待核实」的地方（逐条）
4. 翻译真题数量
