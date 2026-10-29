#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Avant-propos du manuel (redige par l'assembleur, pas par un bloc).
import html, collections


def esc(s):
    return html.escape(s, quote=False)


def power_table():
    return """
<table class="facts">
<thead><tr><th>发射功率上限</th><th>频段范围</th></tr></thead>
<tbody>
<tr><td><b>500 W</b>（在发射机输出端测量）</td><td>479 kHz ～ 28 MHz（含短波 HF 各段）</td></tr>
<tr><td><b>250 W</b>（在发射机输出端测量）</td><td>28 ～ 30 MHz</td></tr>
<tr><td><b>120 W</b>（在发射机输出端测量）</td><td>30 MHz 以上（VHF/UHF/SHF）</td></tr>
<tr><td><b>1 W PIRE</b> 最大</td><td>479 kHz 以下</td></tr>
<tr><td><b>15 W PIRE</b> 最大</td><td>5,3515 – 5,3665 MHz（60 米段）</td></tr>
</tbody></table>
<p class="small">注：表中「发射机输出端测量」的例外只有上面两行（479 kHz 以下与 60 米段），
其余按发射机输出功率计。以上出自 F6KGL《COURS》开篇对现行单一等级（原 2 类）证书的说明；
具体频段划分与脚注见 §R-2.1。</p>
"""


def render(by_id, units):
    o = []
    A = o.append
    A('<hr>')
    A('<h2 id="avant-propos">写在前面：这本教材怎么用</h2>')

    A('<h3>1. 适用对象</h3>')
    A('<p>本教材写给<b>中文母语、有无线电基础、法语约 B1</b>的人。'
      '如果你持有中国 A 类操作证（30–3000 MHz、25 W），那么你的短板很清楚：</p>')
    A('<ul>'
      '<li><b>短波（HF）几乎全新</b>：法国证书开放 1,8 MHz 到 76 GHz 的绝大部分业余频段，'
      '其中 1,8–30 MHz 的短波段是考试的大头，传播、天线尺寸、业务地位这些概念都要重新学。</li>'
      '<li><b>法国法规从零开始</b>：频段划分、业务地位（primaire / secondaire / à égalité de droit）、'
      '发射类别代码、呼号体系、Q 简语、国际字母解释法，都是必须背的硬知识。</li>'
      '<li><b>术语要看懂法语</b>：考试是法语机考，术语的中法对照比概念本身更容易成为障碍。</li>'
      '</ul>')

    A('<h3>2. 考试速览（务必记住）</h3>')
    A('<table class="facts"><tbody>')
    A('<tr><td>考试形式</td><td>两卷机考选择题，<b>每卷 20 题</b>，每题只有一个正确答案</td></tr>')
    A('<tr><td>时长</td><td>法规卷（Réglementation）<b>15 分钟</b>；技术卷（Technique）<b>30 分钟</b></td></tr>')
    A('<tr><td>及格线</td><td>每卷满分 20 分，<b>各需 10/20</b>；两卷都过才拿到证书与呼号</td></tr>')
    A('<tr><td>计分（自 2021 年 3 月 2 日部令起）</td>'
      '<td>答对 <b>1 分</b>；<b>答错和空着都是 0 分，没有倒扣</b></td></tr>')
    A('<tr><td>成绩保留</td><td>只过一卷时，已过那卷的成绩<b>保留 1 年</b>，一年内只需补考另一卷</td></tr>')
    A('<tr><td>未过后的重考</td><td>需等 <b>2 个月</b>才能重考该卷，ANFR 要 <b>1 个月</b>后才接受新的预约</td></tr>')
    A('<tr><td>考试大纲</td><td>2000 年 9 月 21 日部令附件 1（<i>arrêté du 21/09/2000</i>，2021 年 3 月 2 日修订）</td></tr>')
    A('<tr><td>证书等级</td><td>自 2021 年起<b>只有一级</b>，等效 CEPT/HAREC，可在多数欧洲国家免手续操作</td></tr>')
    A('<tr><td>开考前的 5 分钟</td><td>可以先领草稿纸，把公式、dB 换算表、电阻色环码抄下来放在眼前</td></tr>')
    A('</tbody></table>')
    A('<p class="small">以上数值均能在 F6KGL《COURS》的开篇（Introduction）中找到出处；'
      '2021 年之前的旧规则是「答对 3 分、答错倒扣 1 分、满分 60」，与现在不同，'
      '网上很多旧资料仍在传播旧规则，注意甄别。</p>')

    A('<h3>3. 新证书给你什么（与中国 A 类的对比）</h3>')
    A(power_table())
    A('<p>也就是说：拿到法国证书后，你的操作范围从「VHF/UHF 25 W」扩展到'
      '「短波全段 + 500 W（短波段）」，并可申请一个 <code>F</code> 开头的法国呼号。'
      '这也是为什么技术卷里短波传播、天线、传输线的内容占比很高。</p>')

    A('<h3>4. 本教材的结构与编号</h3>')
    A('<p>全书严格沿用 F6KGL《COURS》的章节编号体系，与 Exam\'1 题库中每道题的 '
      '<code>cours</code> 字段（形如 <code>#R21b</code>、<code>#T023g2</code>）一一对应：</p>')
    A('<ul>'
      '<li><code>R</code> = 法规部分（Réglementation）：R-1 ～ R-4 是法规本体，'
      'R-5 是「法规卷里的技术常识」。</li>'
      '<li><code>T</code> = 技术部分（Technique）：第 0 ～ 12 章。</li>'
      '<li>编号规则：<code>R</code> + 章号 + 节号 + 小段字母（如 <b>R21b</b> = §R-2.1 的第 b 小段）；'
      '<code>T</code> + 两位章号 + 节号 + 小段字母（如 <b>T023g2</b> = §2.3 的 g2 小段）。</li>'
      '</ul>')
    A('<p>每个小节标题右侧的橙色 <code>#R21b</code> 标签就是该节在题库里对应的锚点。'
      '每节末尾的<b>「高频考点」</b>框里，是从题库中挑出的、贴在该锚点下的法语真题（含中文译文），'
      '答案默认折叠，建议先自测。</p>')

    A('<h3>5. 章节权重：先读哪里</h3>')
    A('<p>下面是本题库 2692 道真题在各节中的分布（只列前 40，完整清单见附录 F）。'
      '题量越大，说明考得越多，值得反复读。</p>')
    A('<table><thead><tr><th>节</th><th>题量</th><th>占比</th><th>说明</th></tr></thead><tbody>')
    tot = sum(u['nq'] for u in units) or 1
    order = sorted(units, key=lambda u: -u['nq'])[:40]
    for u in order:
        A('<tr><td><a href="#%s">§%s</a></td><td>%d</td><td>%.1f%%</td><td class="small">%s</td></tr>'
          % (u['id'], esc(u['ref']), u['nq'], 100.0 * u['nq'] / tot, esc(u['title_fr'][:60])))
    A('</tbody></table>')
    A('<p class="small">注意：题库里大量题目挂在 <code>#R21b</code>（245 道）和 '
      '<code>#R32a</code>（125 道）等少数锚点上，说明<b>频段表和 Q 简语是最"划算"的背诵点</b>。</p>')
    return '\n'.join(o)
