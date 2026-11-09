"""Add persistent manual marks and build a standalone retry page from delivered exercises."""
from pathlib import Path
import html
import re
from manual_quiz import QUIZ_SCRIPT
from study_navigation import SCRIPT as NAVIGATION_SCRIPT, add_study_navigation, sidebar

BASE = Path(__file__).resolve().parent
BUTTON = '<button type="button" data-action="mistake" aria-pressed="false">标记错题</button>'
STYLE = '''<style id="mistake-book-style">
.mistake-toolbar { display:flex; flex-wrap:wrap; align-items:center; gap:.8rem; background:#edf4fb; border:1px solid #b9c6d2; border-radius:8px; padding:.8rem 1rem; margin:1rem 0; }
.mistake-toolbar a,.mistake-toolbar button { font:inherit; color:#14508c; }
.quiz-controls [data-action="mistake"][aria-pressed="true"] { background:#fff0cf; border-color:#9a6500; color:#714900; }
.mistake-notice { padding:.7rem; background:#fff0cf; }[hidden] { display:none !important; }
</style>'''
NOTICE = '<p class="mistake-notice" data-mistake-storage hidden>浏览器未能保存标记。当前页面仍可标记；请通过页面内的错题本／返回教材链接携带标记，关闭页面后可能丢失。</p>'
SCRIPT = '<script id="quiz-mistakes-script">' + (BASE / 'quiz_mistakes.js').read_text(encoding='utf-8') + '</script>'


def add_mistake_features(document):
    if 'id="quiz-mistakes-script"' in document:
        raise ValueError('Mistake controls already added')
    # render_question supplies the button to new drafts; older edited manuals need it inserted.
    document = re.sub(r'(<div class="quiz-controls">)(?!\s*<button[^>]*data-action="mistake")',
                      lambda m:m[0]+'\n'+BUTTON, document)
    document = document.replace('</h1>', '</h1>' + NOTICE, 1)
    document = document.replace('</head>',STYLE+'</head>',1)
    return document.replace('<script id="manual-quiz-script">',SCRIPT+'<script id="manual-quiz-script">',1)


def build_mistake_book(document, manual_name="manuel-zh.html"):
    sidebar_html = sidebar(manual_name=manual_name, book=True)
    manual_name = html.escape(manual_name, quote=True)
    questions = re.findall(r'<li class="exam-question"[^>]*>.*?</details>\s*</li>', document, re.S)
    if len(questions) != 2688:
        raise ValueError(f'Expected 2688 questions, got {len(questions)}')
    head = document[:document.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>错题本 · 法国业余无线电考试</title>',head)
    # Reuse the textbook's styles and MathJax configuration for identical question rendering.
    return (head + f'</head><body data-sidebar-open="true" data-mistake-book data-manual-page="{manual_name}">' + sidebar_html + '<main><h1>错题本</h1>'
            '<nav class="mistake-toolbar" aria-label="错题本操作">'
            '<span>已标记 <b data-mistake-count>0</b> 道</span>'
            '<button type="button" id="mistake-retry">刷新错题列表／全部重做</button></nav>'
            '<p>每次打开均从未作答状态开始。点击“移出错题本”取消标记；本轮题目保留，刷新列表后移除。</p>'
            '<p>标记保存在当前浏览器。直接打开本地文件时，请使用左侧侧边栏在教材和错题本之间切换，以同步标记并返回先前阅读位置。</p>'
            + NOTICE + '<p id="mistake-empty">错题本暂无题目。返回教材，点击“标记错题”后再从教材打开错题本。</p>'
            '<p id="mistake-missing" class="mistake-notice" hidden></p>'
            '<div class="exam"><ol id="mistake-questions"></ol></div>'
            '<template id="mistake-bank"><ol>'+ '\n'.join(questions)+'</ol></template></main>'
            + SCRIPT + '<script id="manual-quiz-script">'+QUIZ_SCRIPT+'</script>' + NAVIGATION_SCRIPT + '</body></html>')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build the retry page from the current edited manual.')
    parser.add_argument('--manual', type=Path, default=BASE.parent / 'manuel-zh.html')
    args = parser.parse_args()
    document = args.manual.read_text(encoding='utf-8')
    if 'id="quiz-mistakes-script"' not in document:
        document = add_mistake_features(document)
    else:
        document = re.sub(r'<script id="quiz-mistakes-script">.*?</script>', lambda m:SCRIPT, document, flags=re.S)
    document = re.sub(r'<script id="manual-quiz-script">.*?</script>', lambda m:'<script id="manual-quiz-script">'+QUIZ_SCRIPT+'</script>', document, flags=re.S)
    document = add_study_navigation(document)
    args.manual.write_text(document,encoding='utf-8')
    output = args.manual.parent / 'mistake-book.html'
    output.write_text(build_mistake_book(document, args.manual.name),encoding='utf-8')
    print(f'已生成 {output}')
    from mock_exam import build_mock_exam
    exam_output = args.manual.with_name('mock-exam.html')
    exam_output.write_text(build_mock_exam(document, args.manual.name), encoding='utf-8')
    print(f'已生成 {exam_output}')
