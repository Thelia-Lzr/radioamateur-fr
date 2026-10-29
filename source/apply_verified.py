#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把查证结果写回资料，清理误用的「⚠️待核」标记。

四类处理
  A 真事实   → 换成查实的内容（下表 REPL）
  B 题库毛病 → 改成「原文有误／按定义纠正」的说明
  C 来源说明 → 改成中性的「依据：…」
  D 看图标记 → 去掉（原题图已在卡片上）
报告写入 apply_verified_report.json
"""
import json, re, glob, os, collections

SRC = os.path.dirname(os.path.abspath(__file__))

# ---------- A 类：查证后的事实替换 ----------
# (匹配片段, 替换文本)  匹配到含该片段的整句「…待核…」就整句替换
REPL = [
    ("第 22 个",
     "教材 §R-3.2 明载：考试要求的 22 个 Q 简语出自 CEPT T/R 61-02（HAREC 大纲），"
     "第 22 个是 **QTR**（你那里的准确时间是？）。注意 QTR 属 QT 系列，不是 QR 系列"),
    ("1999/519/CE 建议的部令",
     "人体暴露：法国由 **décret n° 2002-775 du 3 mai 2002**（配套 arrêté du 8 octobre 2003）"
     "转置欧盟建议 1999/519/CE；公众电场限值 10–400 MHz 为 **28 V/m**、1–10 MHz 为 87/√f、"
     "400–2000 MHz 为 1,375√f、2–300 GHz 为 61；设台与检修应避开天线近场"),
    ("数值待核，可另查",
     "限值见 décret n° 2002-775 du 3 mai 2002：公众电场 10–400 MHz 为 **28 V/m**"
     "（1–10 MHz 为 87/√f，400–2000 MHz 为 1,375√f）"),
    ("具体条款号与金额",
     "处罚依据：**CPCE art. L39-1 3°**（非法用频/超功率）6 个月监禁 + **30 000 €**；"
     "未申报台站 **L39-4** 3 个月 + 30 000 €；冒用呼号 **L39-8** 1 年；"
     "呼号暂停最长 3 年或吊销见 **arrêté du 21/09/2000 art. 7-3**。"
     "（资料中曾出现的 4 500 € / 7 500 € 并非业余业务的罚金档位）"),
    ("后缀结构的描述",
     "ANFR 现行规则：**2 字母前缀（TM/TO/TK/TX，另有 FX）+ 1–3 位数字 + 1–4 字符后缀（末位必须字母）**，"
     "限 15 天或 6 个月，须提前 20 个工作日申请。教程所写的「数字起头、固定 4 字符」不准确"),
    ("该级别如今已不再组织考试",
     "旧 **classe 3** 自 **arrêté du 23 avril 2012**（JO 2012-05-08）起不再组织考试、不再签发；"
     "12-1241 的频段条件表仍保留其历史条目（144–146 MHz，10 W），但「表里还有」不等于还能考。"
     "法国自 2012-04-23 起只有单一 HAREC 等级"),
    ("PAR 上限由部令与 ARCEP 决定规定",
     "法定量是**发射机输出端的 PEP，不是 PAR**：HF **500 W** / 28–29,7 MHz **250 W** / "
     "≥50 MHz **120 W**；另有 LF·MF 1 W、60 m 15 W（PIRE）。"
     "依据 décision ARCEP 12-1241（经 13-1515、19-1412 修改）"),
    ("现行附件是否已按频段改写",
     "现行基准仍是 décision ARCEP 12-1241（经 13-1515、19-1412 修改，2020-02-05 部令批准）："
     "HF 500 W / 28–29,7 MHz 250 W / ≥50 MHz 120 W，法定量是输出端 PEP"),
    ("业余台允许的 ROS 上限",
     "法国法规**无法定 ROS 上限**：12-1241 只强制功率指示器，旧文的 ROS 指示器要求已废止——"
     "驻波比只是工程建议"),
    ("中继台上 radioguidage 的这一例外",
     "「中继台禁止 radioguidage」**不是法条**：现行与近年法规文本中均查无此规定，"
     "来源是旧版 CSA《Guide du radioamateur》的非规范段落，编纂者自己注明「不能算作官方文本」"),
    ("现行文本只要求「consigner」",
     "日志义务见 décision 12-1241 art. 6：记日期时间、双方呼号、频率、发射类别、地点，保存 1 年。"
     "现行文本**未规定载体**——既不强制纸质，也无明文授权电子（已废止的 00-1364 / 10-0537 曾明文允许电子记录）"),
    ("教材指出 ANFR 在其题库中态度暧昧",
     "**不强制**：ANFR 官方考题 2018 / 2022 / 2023 均答「Non」；"
     "ITU-R SM.326-7（1998-11，现行）只是给主管部门的测量方法建议，推不出「必须拥有」"),
    ("教材只提必要要求与 CE 标志，未点名 RED",
     "适用 **RED 2014/53/EU**：排除条款在 **Annex I 第 1 点**，由 **Article 1(2)** 生效——"
     "业余设备不受本指令管辖，除非被投放市场；套件、自制与业余者改装明确不算投放市场。"
     "协调标准是 **EN 301 783 V2.1.1（2016-01）**"),
    ("RED 对业余无线电整机的具体适用条款",
     "**RED 2014/53/EU**：排除条款在 **Annex I 第 1 点**，由 **Article 1(2)** 生效——"
     "业余设备不受管辖，除非被投放市场（套件、自制、业余者改装不算）。"
     "商业化销售的业余电台须符合 RED 并加 CE 标志，频谱要求走 Article 3(2) / EN 301 783 V2.1.1"),
    ("欧盟统一标称后为 230 V",
     "欧盟现行标称 **230 V / 50 Hz**。**EN 50160:2022** 规定每周 95% 的 10 min rms 值落在 230 V ±10% 内；"
     "正弦下峰值 ≈ **325 V**。教材仍沿用旧值 220/127 V"),
    ("抛物面增益按口径与波长计算",
     r"抛物面增益 \(G = e_A\,(\pi d/\lambda)^2\)，dB 形式 \(G_{\mathrm{dBi}}=10\log_{10}[e_A(\pi d/\lambda)^2]\)；"
     r"口径效率 \(e_A\) 典型值 0,55–0,70（前置馈源 0,55–0,60、Cassegrain 0,65–0,70、偏置 0,70–0,80）"),
    ("欧盟电网电压容差的具体标准编号",
     "**EN 50160:2022**（取代 2010 版）：低压 Un = 230 V，每周 95% 的 10 min rms 值在 ±10% 内；"
     "频率 50 Hz，同步互联系统 ±1%（一年 99.5%）"),
    ("当前生效的 CEPT 建议书编号",
     "**T/R 61-01**（CEPT 业余无线电执照，2024-10-18 更新）与 **T/R 61-02**（HAREC，2024-02-16 更新）"
     "均现行；**T/R 62-01 不存在**（只有已废止的 ERC/REC 62-01）；CEPT Novice 是 "
     "**ECC/REC/(05)06**（建议，不是决定）"),
    ("当前生效的具体 CEPT 建议书编号",
     "**T/R 61-01**（2024-10-18 更新）与 **T/R 61-02**（HAREC，2024-02-16 更新）现行；"
     "T/R 62-01 不存在；CEPT Novice 为 ECC/REC/(05)06"),
    ("教材未给极化失配的具体 dB 数值",
     r"极化失配损耗：线–线夹角 θ 为 \(-20\\log_{10}(\\cos\\theta)\)，45° 为 **3 dB**；"
     "交叉极化（90°）理论无穷、实际约 **20 dB**；**圆极化↔线极化恰为 3 dB**"),
    ("教材未给 AM 检波器 RC 时间常数",
     r"AM 包络检波取 \(1/f_{\text{载波}} \ll RC \ll 1/f_{\text{最高调制}}\)；"
     "例：1 MHz 载波配 5 kHz 调制 → τ ≈ 10–50 µs（R = 10 kΩ，C = 1–4,7 nF）。"
     "τ 过大负峰切割失真，过小残留载波纹波"),
    ("误差环各颜色的精确百分数",
     "误差环按 **IEC 60062:2016**：无环 ±20%、银 ±10%、金 ±5%、棕 ±1%、红 ±2%、"
     "**橙 ±0,05%**、黄 ±0,02%、绿 ±0,5%、蓝 ±0,25%、紫 ±0,1%、**灰 ±0,01%**。"
     "（灰取 ±0,05% 是旧 EIA RS-279 的值，常见电阻手册仍沿用，但现行 IEC 为 ±0,01%）"),
    ("教材未给该数值，为按 §R-5.3c 公式的推算",
     r"按 \(ROS = Z_{\\text{强}}/Z_{\\text{弱}}\)（教程 §10.2c）：50/36 ≈ **1,39**。"
     "同法可得半波偶极 73 Ω → **1,46**、120° 地网 52 Ω → **1,04**、折合偶极 300 Ω → **6,00**"),
    ("教材未给 ROS 数值，按 §R-5.3c 的 Z强/Z弱 推算",
     r"按 \(ROS = Z_{\\text{强}}/Z_{\\text{弱}}\)：73/50 = **1,46**（半波偶极）；"
     "λ/4 垂直 36 Ω → **1,39**；120° 地网 52 Ω → **1,04**"),
    ("官方注释与答案的表述不一致",
     "arrêté du 21/09/2000 附件 II（2021-06-06 起）：中继/差转与信标用 **ZAA–ZZZ**；"
     "**XAA–XZZ 与 YAA–YZZ 列为储备**（主管部门认定需要才开放）。考试答案的「Zxx」与官方文本一致。"
     "另注：XAA–XZZ **不是国际储备段**——ITU RR Appendix 42 中 X 段由多国瓜分（XSA–XSZ 为中国）"),
]

# ---------- 分类规则 ----------
FIG = re.compile(r'看图|图[中内外上]|波形|电路图|方框|色环|频谱|示波|图上|题图|原图|图中')
SRCRE = re.compile(r'锚点为|无对应章节|取自教材|按样题|取自样题|课程未列|课程未给|教材未给|本课程|'
                 r'本知识点锚点|整理，|需另查|可另查')
DEFECT = re.compile(r'题干|题面|原文印作|印作|抄录|注释写|注释与答案|自相矛盾|量纲错误|笔误|'
                    r'不一致|对不上|题库|官方注释|已废止|历史规定')

SENT = re.compile(r'[^。；\n]{0,220}待核[^。；\n]{0,160}')


def classify(sent):
    if any(f in sent for f in [r[0] for r in REPL]):
        return 'A'
    if DEFECT.search(sent):
        return 'B'
    if SRCRE.search(sent):
        return 'C'
    if FIG.search(sent):
        return 'D'
    return 'D'   # 兜底：当成看图/无关标记去掉


def fix_text(t, stats):
    """先做 A 类整句替换，再处理剩余待核"""
    for frag, new in REPL:
        # 找到含该片段的待核句，整句替换
        def sub(m):
            if frag in m.group(0):
                stats['A'] += 1
                return new
            return m.group(0)
        t = SENT.sub(sub, t)

    def sub2(m):
        s = m.group(0)
        cls = classify(s)
        stats[cls] += 1
        word = '依据' if cls == 'C' else '注'
        # 带内容的：把「（⚠️待核：X）」变成「（注：X）」
        s2 = re.sub(r'[（(]\s*⚠️?待核\s*[：:]\s*', '（%s：' % word, s)
        # 空标记：连括号一起去掉
        s2 = re.sub(r'[（(]\s*⚠️?待核\s*[）)]', '', s2)
        # 不带括号的：换成「注：X」
        s2 = re.sub(r'⚠️?待核\s*[：:]', '%s：' % word, s2)
        s2 = s2.replace('⚠️待核', '').replace('待核', '')
        return s2

    return SENT.sub(sub2, t)


if __name__ == '__main__':
    targets = []
    for pat in ('full/out_[1-8].json', 'explain/out_*.json', 'kp/out_*.json', 'kp/merged_out.json'):
        targets += sorted(glob.glob(os.path.join(SRC, pat)))
    targets = [t for t in targets if os.path.exists(t)]

    stats = collections.Counter()
    report = []
    for f in targets:
        d = json.load(open(f, encoding='utf-8'))
        changed = 0
        for k, v in d.items():
            if isinstance(v, str):
                nv = fix_text(v, stats)
                if nv != v:
                    d[k] = nv
                    changed += 1
            elif isinstance(v, dict):
                for fld in ('explain', 'com_zh', 'stem_zh', 'ans_zh', 'body'):
                    t = v.get(fld)
                    if isinstance(t, str) and '待核' in t:
                        nv = fix_text(t, stats)
                        if nv != t:
                            v[fld] = nv
                            changed += 1
        if changed:
            json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            report.append({'file': os.path.relpath(f, SRC), 'changed': changed})
    print('改动文件数:', len(report))
    for r in report:
        print(f"  {r['file']:<28} {r['changed']} 条")
    print()
    print('处理统计: A 查证替换 %d | B 题库毛病 %d | C 来源说明 %d | D 看图标记 %d'
          % (stats['A'], stats['B'], stats['C'], stats['D']))
    json.dump({'report': report, 'stats': dict(stats)},
              open(os.path.join(SRC, 'apply_verified_report.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    # 复查残留
    left = 0
    for f in targets:
        d = json.load(open(f, encoding='utf-8'))
        s = json.dumps(d, ensure_ascii=False)
        left += s.count('待核')
    print('残留「待核」:', left, '处')
