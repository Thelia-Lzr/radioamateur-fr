"""Concise study summaries and semantic emphasis for the textbook lessons."""
import html
import json
from pathlib import Path
import re

from bs4 import BeautifulSoup, NavigableString

BASE = Path(__file__).resolve().parent
GUIDE = json.loads((BASE / 'study_guide.json').read_text(encoding='utf-8'))

# Keep useful corrections; discard the duplicated research log and edit requests.
# Empty entries are already explained in the surrounding lesson.
NOTES = {
    'R11': [''],
    'R12a': ['', ''],
    'R12b': ['占用带宽须全部落在允许频段内，且满足对应上限；具体分档见 §R-1.3.b。'],
    'R13': ['边界题中的 14 000 kHz 指 14 MHz。AM 含上下两条边带，载波恰在频段下边界时，下边带会越界。'],
    'R13a': ['独立市电滤波器不属于现行强制随台设备，但电台仍须防止通过供电网络产生干扰；设备要求与功能要求应区分。'],
    'R13b': ['频偏不等于占用带宽。个别旧题混用了两者，先辨认题干、单位与选项；FM 带宽计算见 §12.4。'],
    'R21b': ['低频特例为 2200 m、630 m 和 60 m；“2222 m”是误写。前两者限 1 W PIRE，60 m 限 15 W PIRE。'],
    'R21d': ['安的列斯与圭亚那的 433.750–434.250 MHz 子频段不向业余业务开放；不能把留尼汪的地区条件套用到法国第 2 区。'],
    'R32': ['优先记 PSE（请）、RX（接收机）、TX（发射机）。',
            'TX 通常表示发射机，TRX 才是收发信机；题 36201 的答案键却写 Transceiver，属于题库用词差异。'],
    'R33': [''],
    'R46c': [''],
    'R47a': ['CEPT 短期使用仍须遵守所在地功率表；例如 28.750 MHz 按 28–30 MHz 档取 250 W。'],
    'R47b': ['CEPT 成员身份、欧盟成员身份及是否适用 T/R 61-01 是不同概念，不能仅凭国别前缀推断境外发射权限。'],
    'R52b': ['VLF 为 3–30 kHz，对应波长 100–10 km；“低于 30 kHz”只给出一个边界。'],
    'R52h': [r'参考换算：同一辐射功率用 PIRE 表示时约为 PAR 的 1.64 倍；以对数功率表示时相差 2.14 dB。'],
    'R54': ['频谱分析仪用于观察谐波；热式电流表用于题库中的高频电流测量题。'],
    'T001': ['等式两边作相同运算；除以分数等于乘其倒数，求平方项的未知量要开平方。'],
    'T011': ['电流表须串接，电压表须并接；检流计测小电流，扩大电流量程通常并接分流电阻。'],
    'T015c': ['色环前两环为有效数字、第三环为倍率、第四环为容差；金色容差 5%，银色容差 10%。'],
    'T023g2': ['本节练习重点是串并联等效容量，其次是串联电容的电压分配。'],
    'T034': ['热式电流表的法语为 ampèremètre thermique。检流计内阻按各题数据判断，不能把一题的 10 mΩ 套到另一题的 10 Ω 上。'],
    'T035': ['同一只 50 kΩ/V 的电压表由 10 V 扩至 100 V，应串联 4.5 MΩ；原例的 450 kΩ 少了一位数量级。'],
    'T042': [r'RC 时间常数为 \(\tau=RC\)；若 R 用 kΩ、C 用 µF，结果为 ms。'],
    'T043': ['理想串联谐振阻抗最小、并联谐振阻抗最大；加入损耗后都不再是理想的零或无穷大。'],
    'T044': ['频谱图若未标频率单位，只能写带宽为两端刻度之差，不应自行补上 kHz 或 MHz；电压比与功率比也须分开。'],
    'T051': ['遇到色环题按 §1.5.a 读数；题目挂在哪个章节不改变图中元件的识别方法。'],
    'T066': ['按图数栅极：一个为三极管、两个为四极管、三个为五极管；不同图片的编号顺序可以不同。'],
    'T071': ['A 类工作点在放大区中央，B 类在边缘；C 类只放大部分周期，不能用于要求线性的 AM 或 BLU。'],
    'T074': ['功率增益用 10log(P出/P入)；输入输出阻抗相同，才可直接用 20log(U出/U入)。'],
    'T077': ['中频与镜像问题见 §11.2–§11.3；本节先掌握混频器的和频、差频与非线性产物。',
             '145 MHz 与 150 MHz 的二次非线性产物题，须同时检查 5、145、150、290、295、300 MHz，别漏掉二次谐波。'],
    'T092': ['无线电波段依次为 VLF、LF、MF、HF、VHF、UHF、SHF、EHF；频率每升一档约增十倍，波长反向减小。',
             '地波衰减通常随频率升高而增大；传播距离还取决于地面导电性，示例距离不能作为固定保证。'],
    'T094': ['自由空间半波偶极的平面方向图常呈 8 字形；最大辐射方向垂直振子，沿振子轴线最弱。'],
    'T095': ['地网与振子夹角 90° 时约 36 Ω，120° 时约 52 Ω；题 21177 因选项限制取接近的 50 Ω。含损耗的“50 Ω 纯阻”是另一种条件。'],
    'T098': ['增益以 dBi 给出、所求又是 PIRE 时直接换算；例如 10 W 加 16 dBi 约得 400 W PIRE，不能再重复扣 2.14 dB。'],
    'T0910': [r'LC 谐振须统一单位：25 nH 是 0.025 µH；与 400 pF 配对时，谐振频率约为 50 MHz。'],
    'T102': [r'题 20360、20385 未标介质，题解按空气 \(\varepsilon_r=1\) 计算；不要擅自代入聚乙烯参数。',
             '50 Ω 是功率容量与衰减之间的常用折中；75 Ω 常用于更重视低损耗的视频或广播线路。'],
    'T113': ['镜像抑制靠混频前的射频滤波；两个信号一旦落入同一中频，已不能靠中频滤波分开。'],
    'T115': ['缓冲级用于隔离和匹配，简化框图可能省略；天线匹配盒的原理见 §10.3。'],
    'T123': [r'AM 双边带带宽 \(B=2f_{\mathrm{音频,max}}\)；最高调制频率 3 kHz 时，占用带宽为 6 kHz。'],
    'T124': [r'窄带近似只适用于调制指数远小于 1 的情形，此时 \(B\approx2f_{\mathrm{音频,max}}\)；一般计算仍用卡森规则。'],
    'T126': ['各类调制的频谱宽度和法定占用带宽上限是不同问题；法定分档见 §R-1.3.b。'],
}

STUDY_CSS = """
/* Study emphasis is separate from quiz right/wrong colors. */
.exam-key { color:#773b8a; font-weight:750; }
.chapter-summary, .section-summary { border:1px solid #ded1e5;
  border-left:4px solid #89529b; border-radius:5px; background:#faf5fc;
  padding:.65rem .9rem; margin:.9rem 0 1.2rem; font-size:.94rem; }
.chapter-summary { background:#f3edf7; }
.summary-title { margin:0 0 .25rem; font-weight:700; color:#633273; }
.section-summary p:last-child { margin-bottom:0; }
.chapter-summary ul { margin:.2rem 0 .1rem 1.2rem; }
.study-note { font-size:.92rem; border-left:3px solid #c4b3cc;
  padding:.35rem .7rem; color:#4d4551; background:#f8f5fa; }
.study-note-label { color:#633273; font-weight:650; }
@media print { .exam-key { color:#633273; } }
"""

SECTION = re.compile(r'(?P<heading><h3 id="(?P<id>[RT][^\"]+)"[^>]*>.*?</h3>)'
                     r'(?P<body>.*?)(?=<div class="exam">)', re.S)
AUDIT_LABELS = ('已核实', '本节未涉及', '题库／原文有误')


def emphasize(fragment, keywords):
    soup = BeautifulSoup(fragment, 'html.parser')
    count = 0
    # Existing editorial emphasis should also use the same colored treatment.
    for bold in soup.find_all(['b', 'strong']):
        bold.name = 'strong'
        bold['class'] = list(dict.fromkeys(bold.get('class', []) + ['exam-key']))
        count += 1
    terms = sorted({t for t in keywords if len(t) >= 2}, key=len, reverse=True)
    pieces = []
    for term in terms:
        left = r'(?<![A-Za-z0-9_])' if re.match(r'[A-Za-z0-9]', term) else ''
        right = r'(?![A-Za-z0-9_])' if re.search(r'[A-Za-z0-9]$', term) else ''
        pieces.append(left + re.escape(term) + right)
    if not pieces:
        return str(soup), count
    pattern = re.compile('|'.join(pieces))
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        if any(p.name in ('script', 'style', 'code', 'strong') or
               'fr' in p.get('class', []) for p in node.parents if p.name):
            continue
        # Preserve every LaTeX expression verbatim; emphasize its concept name.
        chunks = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])', str(node), flags=re.S)
        output = []
        for index, chunk in enumerate(chunks):
            if index % 2:
                output.append(NavigableString(chunk))
                continue
            pos = 0
            for match in pattern.finditer(chunk):
                output.append(NavigableString(chunk[pos:match.start()]))
                key = soup.new_tag('strong', attrs={'class': 'exam-key'})
                key.string = match[0]
                output.append(key)
                pos = match.end()
                count += 1
            output.append(NavigableString(chunk[pos:]))
        node.replace_with(*output)
    for bold in soup.find_all('b'):
        if len(bold.contents) == 1 and getattr(bold.contents[0], 'name', None) == 'strong':
            bold.unwrap()
    return str(soup), count


def clean_audit_nodes(soup, section, strict):
    found = []
    for node in soup.select('div.note, div.warn'):
        label = node.find(['b', 'strong'], recursive=False)
        if (label and any(t in label.get_text() for t in AUDIT_LABELS)) or re.match(
                r'^⚠️?\s*待核实', node.get_text(strip=True)):
            found.append(node)
    replacements = NOTES.get(section, [])
    if strict and len(found) != len(replacements):
        raise ValueError(f'Audit block mismatch in {section}: {len(found)}/{len(replacements)}')
    for index, node in enumerate(found):
        text = replacements[index] if index < len(replacements) else ''
        if text:
            replacement = BeautifulSoup('<p class="study-note"><span class="study-note-label">易错提醒：</span>'
                                         + html.escape(text) + '</p>', 'html.parser')
            node.replace_with(replacement)
        else:
            node.decompose()
    for node in soup.select('.src'):
        node.decompose()
    # Correct the main statement so it no longer conflicts with the old audit note.
    if section == 'R46c':
        for text in list(soup.find_all(string=True)):
            if '后接 4 个字符' in text:
                text.replace_with(str(text).replace('后接 4 个字符', '后接 1 至 4 个字符'))
    return len(found)


def polish_document(document, strict=False):
    if 'id="manual-study-style"' in document:
        raise ValueError('Study summaries are already applied; refusing to duplicate them.')
    stats = {'sections': 0, 'chapters': 0, 'audit_blocks': 0, 'emphasis': 0}

    def section(match):
        sid = match['id']
        guide = GUIDE['sections'][sid]
        soup = BeautifulSoup(match['body'], 'html.parser')
        stats['audit_blocks'] += clean_audit_nodes(soup, sid, strict)
        body, count = emphasize(str(soup), guide['keywords'])
        summary, _ = emphasize(html.escape(guide['summary']), guide['keywords'])
        stats['emphasis'] += count
        stats['sections'] += 1
        return (match['heading'] + f'\n<div class="lesson-body" data-section="{sid}">{body}</div>\n'
                f'<aside class="section-summary" data-section="{sid}" aria-label="本节考点">'
                f'<p class="summary-title">本节考点</p><p>{summary}</p></aside>\n')

    document = SECTION.sub(section, document)
    if stats['sections'] != len(GUIDE['sections']):
        raise ValueError(f'Missing lesson summaries: {stats["sections"]}')

    def chapter(match):
        cid = match['id']
        keywords = [term for sid, entry in GUIDE['sections'].items()
                    if (sid.startswith('R' + cid[2:]) if cid.startswith('R-') else
                        sid.startswith('T' + cid[2:].zfill(2))) for term in entry['keywords']]
        items = ''.join('<li>' + emphasize(html.escape(point), keywords)[0] + '</li>'
                        for point in GUIDE['chapters'][cid])
        stats['chapters'] += 1
        return match[0] + f'\n<aside class="chapter-summary" data-chapter="{cid}" aria-label="本章重点">' \
            + '<p class="summary-title">本章重点</p><ul>' + items + '</ul></aside>'

    document = re.sub(r'<h2 id="chap-(?P<id>[^\"]+)">.*?</h2>', chapter, document)
    # Remove the duplicated appendix provenance note; retain a short useful appendix.
    document = re.sub(r'<div class="note"><b>✅ 已核实</b>.*?</div>', '', document, flags=re.S)
    appendix = ('<h3 id="annexe-g">附录 G　易错概念速查</h3>'
                '<ul><li>频偏与占用带宽不同；频段边界要容纳完整发射频谱。</li>'
                '<li>PAR 与 PIRE 的参考天线不同；算辐射功率前先扣馈线损耗。</li>'
                '<li>串联电阻同电流、并联电阻同电压；电容的等效串并联规则相反。</li>'
                '<li>镜像在混频前抑制，谐波在发射功放后过滤。</li>'
                '<li>题库有个别单位或答案用词差异，相关处已保留简短易错提醒。</li></ul>')
    document, annex_count = re.subn(r'<h3 id="annexe-g">.*?(?=</main>)', appendix, document, flags=re.S)
    if annex_count != 1:
        raise ValueError('Missing appendix G')
    document = document.replace('待核事项核对结果', '易错概念速查').replace('待核实清单', '易错概念速查')
    # Remove repeated editorial directions from explanations, preserving uncertainties
    # and any substantive qualification about a malformed question.
    document = re.sub(r'(?:按|参照)(?:教材)?\s*§[A-Za-z0-9.、/–\-]+\s*核对[。；]?', '', document)
    for redundant in (
            '⚠️该分工容易记混，请与教材 §R22b 核对后记忆。',
            '注：3 类的模式与频段权限请与教材 §R42a 的权限表核对。',
            '若名单有更新，请按教材 §R47c 的现行列表核对。',
            '并与教材 §R52e 核对。',
            '教材 §T074a 核对。',
            '夹角这一项的读数请按教材 §9.5／§9.10f 核对。'):
        document = document.replace(redundant, '')
    document = document.replace('</head>', '<style id="manual-study-style">' + STUDY_CSS + '</style></head>', 1)
    return document, stats


if __name__ == '__main__':
    target = BASE.parent / 'manuel-zh.html'
    result, stats = polish_document(target.read_text(encoding='utf-8'), strict=True)
    target.write_text(result, encoding='utf-8')
    print(json.dumps(stats, ensure_ascii=False))
