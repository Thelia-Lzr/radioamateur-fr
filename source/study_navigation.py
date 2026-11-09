"""Shared sidebar and stable fragment navigation, preserving the edited textbook."""
from pathlib import Path
import base64
import html
import re
import struct

from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
STYLE = '<style id="study-navigation-style">' + (BASE / 'study_navigation.css').read_text(encoding='utf-8') + '</style>'
SCRIPT = '<script id="study-navigation-script">' + (BASE / 'study_navigation.js').read_text(encoding='utf-8') + '</script>'


def sidebar(toc='', manual_name='manuel-zh.html', book=False, exam=False):
    navigation = ''
    if toc:
        soup = BeautifulSoup(toc, 'html.parser')
        listing = soup.select_one('.toc > ol')
        for index, item in enumerate(listing.find_all('li', recursive=False)):
            children = item.find('ol', recursive=False)
            if children:
                children.extract()
                group = soup.new_tag('details', attrs={'class': 'toc-chapter'})
                if index == 0:
                    group['open'] = ''
                summary = soup.new_tag('summary')
                for node in list(item.contents):
                    summary.append(node.extract())
                group.append(summary)
                group.append(children)
                item.append(group)
        # Sidebar labels should not be typeset asynchronously by MathJax.
        navigation = '<nav class="toc no-mathjax" aria-label="教材目录"><h2>目录</h2>' + str(listing).replace(r'\(\rho\)', 'ρ') + '</nav>'
    manual_link = html.escape(manual_name, quote=True)
    home = (f'<a href="{manual_link}" data-mistake-link="{manual_link}">返回教材</a>' if book or exam
            else '<a href="#avant-propos">教材首页</a>')
    book_link = ('<span class="sidebar-current" aria-current="page">错题本（<b data-mistake-count>0</b>）</span>' if book
                 else '<a href="mistake-book.html" data-mistake-link="mistake-book.html">打开错题本（<b data-mistake-count>0</b>）</a>')
    exam_link = ('<span class="sidebar-current" aria-current="page">模拟考试</span>' if exam
                 else '<a href="mock-exam.html" data-mistake-link="mock-exam.html">模拟考试</a>')
    return ('<button type="button" class="sidebar-toggle" data-sidebar-toggle aria-controls="study-sidebar" '
            'aria-expanded="true" aria-label="收起目录侧边栏"><span aria-hidden="true">☰</span><span class="sidebar-toggle-label">目录</span></button>'
            '<aside id="study-sidebar" class="study-sidebar" aria-label="学习导航">'
            '<header class="sidebar-header"><strong>学习导航</strong><span>法国业余无线电考试</span></header>'
            '<nav class="sidebar-shortcuts" aria-label="学习页面">' + home + book_link + exam_link + '</nav>'
            + navigation + '</aside><button type="button" class="sidebar-backdrop" data-sidebar-close aria-label="关闭目录侧边栏" tabindex="-1"></button>')


def reserve_image_size(match):
    tag = match[0]
    if re.search(r'\bwidth=', tag):
        return tag
    encoded = re.search(r'src="data:image/png;base64,([^"]+)"', tag)
    if not encoded:
        return tag
    header = base64.b64decode(encoded[1][:32])
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        return tag
    width, height = struct.unpack('>II', header[16:24])
    return tag[:-1] + f' width="{width}" height="{height}">'


def add_study_navigation(document):
    original = re.search(r'<aside id="study-sidebar".*?</aside>', document, re.S)
    previous_toc = re.search(r'<nav class="toc.*?</nav>', original[0], re.S) if original else None
    document = re.sub(r'<style id="study-navigation-style">.*?</style>', '', document, flags=re.S)
    document = re.sub(r'<script id="study-navigation-script">.*?</script>', '', document, flags=re.S)
    document = re.sub(r'<button[^>]*class="sidebar-toggle".*?</button>\s*<aside id="study-sidebar".*?</aside>\s*<button[^>]*class="sidebar-backdrop".*?</button>', '', document, flags=re.S)
    toc = re.search(r'<div class="toc">.*?</div>', document, re.S)
    # Reapplying to an existing sidebar should preserve its chapter listing.
    if not toc:
        toc = previous_toc
    if not toc:
        raise ValueError('Textbook table of contents missing')
    toc_html = toc[0]
    document = document.replace(toc_html, '', 1)
    document = document.replace('</head>', STYLE + '</head>', 1)
    document = re.sub(r'<body(?: data-sidebar-open="(?:true|false)")?>', lambda m: '<body data-sidebar-open="true">' + sidebar(toc_html), document, count=1)
    document = document.replace('</body>', SCRIPT + '</body>', 1)
    return re.sub(r'<img\b[^>]*class="qimg"[^>]*>', reserve_image_size, document)
