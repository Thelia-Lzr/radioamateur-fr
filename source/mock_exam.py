"""Build an offline timed exam using the current edited questions and explanations."""
from pathlib import Path
import json
import re

from gen_common import load_questions
from mistake_book import NOTICE, SCRIPT as MISTAKES_SCRIPT
from study_navigation import SCRIPT as NAVIGATION_SCRIPT, sidebar

BASE = Path(__file__).resolve().parent
THEMES = {
    301: '发射类别与使用权限', 302: '呼号与国家前缀', 303: 'Q 简语', 304: '国际字母解释法',
    305: '频段划分与业务地位', 306: '考试、处罚、干扰与带宽', 307: '通联内容、设备与安全',
    308: '天线与波长频率', 309: '匹配、驻波与馈线损耗', 310: '波段分类、分贝与电磁兼容',
    201: '电阻色环', 202: '电阻串并联', 203: '半导体与放大类别', 204: '收发机框图',
    205: '射频各级与音频器件', 206: '基础电学与测量', 207: '交流电',
    208: '电容与电感', 209: '变压器、运放与滤波', 210: '天线、传播与传输线',
}


def build_manifest(document):
    source = {str(q['num']): q for q in load_questions()['questions']}
    questions = []
    section = None
    for match in re.finditer(r'<h3 id="([RT][^"]+)"[^>]*>|<li class="exam-question" data-question="(\d+)"', document):
        if match[1]:
            section = match[1]
            continue
        number = match[2]
        q = source[number]
        kind = 'regulation' if q['themeNum'] >= 300 else 'technique'
        chapter = 'R-' + section[1] if section.startswith('R') else 'T-' + str(int(section[1:3]))
        questions.append({'id':number, 'theme':q['themeNum'], 'kind':kind,
                          'chapter':chapter, 'section':section, 'answer':q['reponse']})
    if len(questions) != 2688 or len({q['id'] for q in questions}) != 2688:
        raise ValueError('Expected 2688 unique questions from the edited textbook')
    modes = {}
    for kind, label, minutes in [('regulation', '法规', 15), ('technique', '技术', 30)]:
        pool = [q for q in questions if q['kind'] == kind]
        modes[kind] = {'label':label, 'seconds':minutes * 60,
                       'themes':sorted({q['theme'] for q in pool}),
                       'chapters':sorted({q['chapter'] for q in pool}, key=lambda c:int(c.split('-')[1]))}
        if len(modes[kind]['themes']) != 10:
            raise ValueError('Expected ten knowledge themes for each exam')
    return {'version':1, 'questions':questions, 'modes':modes,
            'themes':{str(k):v for k,v in THEMES.items()}}


def build_mock_exam(document, manual_name='manuel-zh.html'):
    manifest = build_manifest(document)
    questions = re.findall(r'<li class="exam-question"[^>]*>.*?</details>\s*</li>', document, re.S)
    head = document[:document.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>模拟考试 · 法国业余无线电考试</title>', head)
    style = '<style id="mock-exam-style">' + (BASE / 'mock_exam.css').read_text(encoding='utf-8') + '</style>'
    scripts = ''.join('<script>' + (BASE / filename).read_text(encoding='utf-8') + '</script>'
                      for filename in ['mock_exam_sampling.js', 'mock_exam.js'])
    body = '''<main>
<h1>模拟考试</h1>
<p class="lead">法国单一等级 · CEPT/HAREC</p>
<p id="exam-storage-notice" class="mistake-notice" hidden>浏览器无法保存考试进度，请保持本页打开。倒计时仍会正常运行。</p>
<p id="exam-message" role="status" aria-live="polite"></p>
<section id="exam-setup" aria-label="选择考试科目">
<p>法规和技术可分别练习。每科 20 道单选题，答对得 1 分，答错或未答得 0 分，10/20 及格。</p>
<div class="exam-mode-grid">
<article><h2>法规</h2><p>Réglementation</p><p><b>20 题 · 15 分钟</b></p><button type="button" data-exam-start="regulation">开始法规考试</button></article>
<article><h2>技术</h2><p>Technique</p><p><b>20 题 · 30 分钟</b></p><button type="button" data-exam-start="technique">开始技术考试</button></article>
</div>
<p class="exam-setup-note">每卷覆盖 10 类知识点，每类抽 2 题，并覆盖教材中有题目的各大章。覆盖式抽题用于均衡复习，不代表正式考试固定按此比例抽题。</p>
<p class="exam-setup-note">开始后持续计时，刷新或离开页面不会暂停；到时自动交卷。考试中显示法语题干、选项和原题图，提交后查看翻译、全部对错及解析。</p>
</section>
<section id="exam-running" hidden aria-label="模拟考试作答">
<div class="exam-session-toolbar"><strong id="exam-mode-label"></strong>
<div class="exam-clock"><span>剩余 <b id="exam-remaining" role="timer" aria-live="off">00:00</b></span><span>已用 <b id="exam-elapsed">00:00</b></span></div><progress id="exam-time-progress" max="900" value="900" aria-label="剩余考试时间"></progress>
<span id="exam-progress"></span><button type="button" data-exam-submit>提交试卷</button></div>
<nav id="exam-question-map" aria-label="选择试题"></nav>
<details id="exam-recap"><summary>答题总览</summary><table><thead><tr><th>题号</th><th>你的答案</th></tr></thead><tbody id="exam-recap-body"></tbody></table></details>
<div id="exam-question-host" class="exam"></div>
<div class="exam-paging"><button type="button" id="exam-previous">上一题</button><button type="button" id="exam-clear">清除本题选择</button><button type="button" id="exam-next">下一题</button></div>
<p class="small">点击选项或按 1–4 作答；左右方向键切换题目。可通过上方题号返回修改答案。</p>
<section id="exam-submit-check" class="exam-submit-check" hidden aria-label="确认提交">
<p id="exam-submit-summary"></p><button type="button" id="exam-confirm-submit">确认提交并查看结果</button><button type="button" id="exam-continue">继续作答</button></section>
</section>
<section id="exam-results" hidden aria-label="考试结果">
<div id="exam-score" class="exam-score" tabindex="-1"></div>
<p id="exam-coverage"></p>
<details id="exam-theme-results"><summary>各知识点得分</summary><table><thead><tr><th>知识点</th><th>得分</th><th>未答</th></tr></thead><tbody id="exam-theme-scores"></tbody></table></details>
<div class="exam-result-actions"><button type="button" id="exam-restart">再考同一科</button><button type="button" id="exam-change-mode">选择其他科目</button></div>
<nav id="exam-review-filters" aria-label="筛选考试题目"><button type="button" data-exam-filter="all" aria-pressed="true">全部</button><button type="button" data-exam-filter="wrong" aria-pressed="false">错题／未答</button><button type="button" data-exam-filter="right" aria-pressed="false">对题</button></nav>
<p id="exam-review-empty" hidden>没有符合筛选条件的题目。</p>
<div class="exam"><ol id="exam-review-list"></ol></div>
</section>
'''
    encoded = json.dumps(manifest, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return (head + style + '</head><body data-sidebar-open="true" data-mock-exam>'
            + sidebar(manual_name=manual_name, exam=True) + body + NOTICE + '</main>'
            '<template id="mock-exam-bank"><ol>' + '\n'.join(questions) + '</ol></template>'
            '<script id="mock-exam-data" type="application/json">' + encoded + '</script>'
            + MISTAKES_SCRIPT + NAVIGATION_SCRIPT + scripts + '</body></html>')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build an offline timed mock exam from the edited textbook.')
    parser.add_argument('--manual', type=Path, default=BASE.parent / 'manuel-zh.html')
    args = parser.parse_args()
    output = args.manual.with_name('mock-exam.html')
    output.write_text(build_mock_exam(args.manual.read_text(encoding='utf-8'), args.manual.name), encoding='utf-8')
    print(f'已生成 {output}')
