#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Annexes du manuel : tactique d'examen, formules, code Q, alphabet, vocabulaire,
# index des signets, liste des points a verifier.
import html, os, csv, collections

BASE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s, quote=False)


# ------------------------------------------------------------------ code Q
QCODE = [
    ("QRA", "Quel est le nom de votre station ?", "你台站的名称是什么？",
     "Le nom de ma station est…", "我台站的名称是……"),
    ("QRG", "Voulez-vous m'indiquer ma fréquence exacte ?", "请告诉我我的准确频率（或……的准确频率）",
     "Votre fréquence exacte est de … kHz (ou MHz)", "你的准确频率是……kHz（或 MHz）"),
    ("QRH", "Ma fréquence varie-t-elle ?", "我的频率在变化吗？",
     "Votre fréquence varie", "你的频率在变化"),
    ("QRK", "Quelle est l'intelligibilité de mes signaux ?", "我的信号可懂度如何（1–5）？",
     "L'intelligibilité est : 1 mauvaise ; 2 médiocre ; 3 assez bonne ; 4 bonne ; 5 excellente",
     "可懂度：1 差；2 较差；3 尚可；4 好；5 极好"),
    ("QRL", "Êtes-vous occupé ?", "你忙吗（频率被占用）？",
     "Je suis occupé. Prière de ne pas brouiller", "我很忙，请勿干扰"),
    ("QRM", "Êtes-vous brouillé ?", "你受到人工干扰吗（1–5）？",
     "Je suis brouillé : 1 nullement ; 2 faiblement ; 3 modérément ; 4 fortement ; 5 très fortement",
     "受干扰程度：1 无；2 轻微；3 中等；4 严重；5 极严重"),
    ("QRN", "Êtes-vous troublé par des parasites ?", "你受到天电/自然噪声干扰吗（1–5）？",
     "Je suis troublé par des parasites : 1 nullement ; … 5 très fortement",
     "受噪声干扰程度：1 无；……5 极严重"),
    ("QRO", "Dois-je augmenter la puissance d'émission ?", "要我增大发射功率吗？",
     "Augmentez la puissance d'émission", "增大发射功率"),
    ("QRP", "Dois-je diminuer la puissance d'émission ?", "要我减小发射功率吗？",
     "Diminuez la puissance d'émission", "减小发射功率"),
    ("QRT", "Dois-je cesser la transmission ?", "要我停止发射吗？",
     "Cessez la transmission", "停止发射"),
    ("QRU", "Avez-vous quelque chose pour moi ?", "有给我的报文吗？",
     "Je n'ai rien pour vous", "没有给你的报文"),
    ("QRV", "Êtes-vous prêt ?", "你准备好了吗？",
     "Je suis prêt", "我准备好了"),
    ("QRX", "À quel moment me rappellerez-vous ?", "你什么时候再呼叫我？",
     "Je vous rappellerai à … h (sur … kHz ou MHz)", "我将在……时（在……kHz/MHz 上）再呼叫你"),
    ("QRZ", "Par qui suis-je appelé ?", "谁在呼叫我？",
     "Vous êtes appelé par … sur … kHz (ou MHz)", "你正被……在……kHz（或 MHz）上呼叫"),
    ("QSA", "Quelle est la force de mes signaux ?", "我的信号强度如何（1–5）？",
     "La force est : 1 à peine perceptible ; 2 faible ; 3 assez bonne ; 4 bonne ; 5 très bonne",
     "信号强度：1 几乎听不到；2 弱；3 尚可；4 好；5 很好"),
    ("QSB", "La force de mes signaux varie-t-elle ?", "我的信号强度在衰落吗？",
     "La force de vos signaux varie", "你的信号强度在衰落"),
    ("QSL", "Pouvez-vous me donner accusé de réception ?", "你能给我收妥确认吗？",
     "Je vous donne accusé de réception", "我给你收妥确认"),
    ("QSO", "Pouvez-vous communiquer avec … directement ?", "你能与……直接（或经中继）通信吗？",
     "Je puis communiquer avec … directement (ou par …)", "我能与……直接（或经……）通信"),
    ("QSP", "Voulez-vous retransmettre à … gratuitement ?", "你愿意免费转发给……吗？",
     "Je peux retransmettre à … gratuitement", "我愿免费转发给……"),
    ("QSY", "Dois-je passer à la transmission sur une autre fréquence ?", "要我换到其他频率发射吗？",
     "Passez sur une autre fréquence (ou sur … kHz/MHz)", "请换到其他频率（或……kHz/MHz）发射"),
    ("QTH", "Quelle est votre position en latitude et longitude ?", "你的地理位置（经纬度）在哪里？",
     "Ma position est … latitude … longitude", "我的位置是……纬度……经度"),
    ("QTR", "Quelle est l'heure exacte ?", "准确时间是多少？",
     "L'heure exacte est …", "准确时间是……"),
]

ALPHABET = [("A", "ALFA"), ("B", "BRAVO"), ("C", "CHARLIE"), ("D", "DELTA"),
            ("E", "ECHO"), ("F", "FOX-TROT"), ("G", "GOLF"), ("H", "HOTEL"),
            ("I", "INDIA"), ("J", "JULIETT"), ("K", "KILO"), ("L", "LIMA"),
            ("M", "MIKE"), ("N", "NOVEMBER"), ("O", "OSCAR"), ("P", "PAPA"),
            ("Q", "QUEBEC"), ("R", "ROMEO"), ("S", "SIERRA"), ("T", "TANGO"),
            ("U", "UNIFORM"), ("V", "VICTOR"), ("W", "WHISKEY"), ("X", "X-RAY"),
            ("Y", "YANKEE"), ("Z", "ZOULOU (zulu)")]


def appendix_tactique():
    o = []
    A = o.append
    A('<h3 id="annexe-a">附录 A　考试战术</h3>')
    A('<h4>A.1　时间怎么分</h4>')
    A('<table><thead><tr><th>卷</th><th>题数</th><th>时长</th><th>每题可用时间</th>'
      '<th>及格</th></tr></thead><tbody>')
    A('<tr><td>法规卷（Réglementation）</td><td>20</td><td>15 分钟</td><td><b>约 45 秒</b></td><td>10/20</td></tr>')
    A('<tr><td>技术卷（Technique）</td><td>20</td><td>30 分钟</td><td><b>约 90 秒</b></td><td>10/20</td></tr>')
    A('</tbody></table>')
    A('<p>法规卷只有 15 分钟、平均 45 秒一题，所以<b>法规部分必须靠"秒答"的背诵题拿分</b>'
      '（Q 简语、字母解释法、频段限值、呼号前缀）。技术卷时间宽裕，计算题慢慢算都够。</p>')
    A('<h4>A.2　最重要的规则：绝不空题</h4>')
    A('<p>自 2021 年 3 月 2 日部令起（2021 年 6 月 7 日在考点生效）：'
      '<b>答对 1 分，答错 0 分，不答也是 0 分，没有倒扣</b>。'
      '所以——<b>每一题都必须给出一个答案</b>，空着等于白白放弃 25% 的期望分。</p>')
    A('<p>F6KGL 教材里给出的估算：如果你有把握答对 7 题，剩下 13 题完全靠猜（四选一，期望 1/4），'
      '则 7 + 13 × 0,25 = <b>10,25 分</b>，刚好及格。但为了稳当，'
      '建议把目标定在<b>有把握 13 题（65%）</b>。</p>')
    A('<h4>A.3　猜也有讲究：优先选第 3 个选项</h4>')
    A('<p>把本题库 2692 道真题的正确答案位置统计一遍，结果并不均匀：</p>')
    A('<table><thead><tr><th>选项位置</th><th>题数</th><th>占比</th></tr></thead><tbody>')
    A('<tr><td>第 1 个选项</td><td>703</td><td>26,1%</td></tr>')
    A('<tr><td>第 2 个选项</td><td>669</td><td>24,9%</td></tr>')
    A('<tr><td><b>第 3 个选项</b></td><td><b>748</b></td><td><b>27,8%</b></td></tr>')
    A('<tr><td>第 4 个选项</td><td>572</td><td>21,2%</td></tr>')
    A('</tbody></table>')
    A('<p>也就是说，纯瞎猜时，<b>固定选第 3 个选项的期望略高于其他位置</b>（27,8% 对 21,2%），'
      '差距约 1,3 分/卷。这是题库本身的分布特征，不是官方规则，只能作为最后手段。</p>')
    A('<div class="tips"><b>更实用的蒙题法（按优先级）：</b>'
      '<ol><li>先排除明显离谱的选项（单位不对、数量级不对、把 kHz 写成 MHz 的）；</li>'
      '<li>题干里出现具体数字（如 <code>430 à 440 MHz</code>）时，往往正确选项与它同量级；</li>'
      '<li>看到"其他国家的规则"（如 144–148 MHz、50,2–51,2 MHz）多半是陷阱选项；</li>'
      '<li>实在不会，统一填第 3 个选项，不要每题换着猜。</li></ol></div>')
    A('<h4>A.4　开考前的 5 分钟：草稿纸清单</h4>')
    A('<p>按 F6KGL 教材的说法，正式计时开始前大约有 <b>5 分钟</b>可以把公式抄到考点发的草稿纸上'
      '（草稿纸由考点提供，考完不能带出考场）。建议照下面的顺序抄，写最可能忘的：</p>')
    A('<div class="formula">1) 欧姆定律三角形：U = R·I，I = U/R，R = U/I\n'
      '2) 功率：P = U·I = R·I² = U²/R\n'
      '3) 电阻并联：1/R = 1/R1 + 1/R2；两电阻 R = R1·R2/(R1+R2)\n'
      '4) 波长：λ(m) = 300 / f(MHz)　半波振子 L = 150/f　四分之一波长 L = 75/f\n'
      '5) 容抗 Xc = 1/(2πfC)　感抗 Xl = 2πfL　谐振 f = 1/(2π√(LC))\n'
      '6) 分贝：G(dB) = 10 log(Ps/Pe)；3 dB ≈ ×2，10 dB = ×10，6 dB ≈ ×4\n'
      '7) 驻波：ρ = (Umax−Umin)/(Umax+Umin)；ROS = (1+ρ)/(1−ρ)；P réfléchie = P émise·ρ²\n'
      '8) 变压器：N = ns/np = Us/Up = Ip/Is\n'
      '9) 电阻色环：黑0 棕1 红2 橙3 黄4 绿5 蓝6 紫7 灰8 白9（金 ±5%，银 ±10%）\n'
      '10) 频段限值表（1 区，尤其 3,5–3,8 / 7,0–7,2 / 14,0–14,35 / 21,0–21,45 / 28,0–29,7 MHz，\n'
      '    以及 50–52、144–146、430–440、1240–1300 MHz——完整对照表见 §R-2.1.b）</div>')
    A('<h4>A.5　考试当天</h4>')
    A('<ul>'
      '<li>带<b>准考证（convocation）、身份证件、不可编程计算器、铅笔</b>；草稿纸由考点提供。</li>'
      '<li>现在的考试<b>没有最低年龄限制</b>（自 2000 年 9 月 21 日部令起）。</li>'
      '<li>考位由 ANFR 的地区无线电通信服务中心（SRR）安排，需要电话预约；'
      '预约到考试一般要等约一个月，想指定日期请早约。</li>'
      '<li>除补考外，考试<b>先考法规、紧接着考技术，两卷之间没有休息</b>。</li>'
      '<li>两卷的结果<b>要到全部考完才一并公布</b>，考完法规后不要因为自我感觉差而影响技术卷的发挥。</li>'
      '<li>考试过程中如果设备出问题或题目有争议，<b>立即举手告诉监考</b>——只有监考可以暂停计时；'
      '计时结束后任何异议都不受理。</li>'
      '<li>当场知道结果。通过后 ANFR 会在下一周寄出证书和呼号申请表（也可在 '
      '<code>teleservice-amateurs.anfr.fr</code> 在线办理），'
      '<b>只有收到呼号通知（notification de l\'indicatif d\'appel）才能开始发射</b>。</li>'
      '<li>某一卷没过：需等 <b>2 个月</b>才能重考该卷，ANFR 要 <b>1 个月</b>后才接受重新预约。</li>'
      '<li>如持有 IPP ≥ 70% 的残疾认定，考试时间<b>triple</b>（法规 45 分钟、技术 1 小时 30 分），'
      '必要时可在住所应考，具体向考点咨询。</li>'
      '</ul>')
    A('<h4>A.6　题库里观察到的出题规律</h4>')
    A('<ul>'
      '<li><b>题量高度集中</b>：<code>#R21b</code>（频段划分）245 题、<code>#R32a</code>（Q 简语）125 题、'
      '<code>#R47b</code>（呼号国别）118 题、<code>#R12a</code>（发射类别）116 题、'
      '<code>#R31</code>（字母解释法）102 题——这 5 个锚点占了全题库的约 26%，'
      '而且全是<b>背了就得分</b>的题，性价比最高。</li>'
      '<li><b>带图的题很多</b>：2692 题中有约 560 题以 <code>*</code> 开头或在题干中提到 <code>SCHEMA</code>'
      '（电路图/框图），技术卷里尤其集中。看这类题时先找"问的是什么量"，再去找图上的标注。</li>'
      '<li><b>同一个题干反复出现</b>：例如 "RESISTANCE EQUIVALENTE"（21 次）、'
      '"CAPACITE EQUIVALENTE"（13 次）、"VALEUR DE LA RESISTANCE"（11 次）、'
      '"NOM DE L\'ETAGE"/"ETAGE REPERE PAR ?"（共 17 次）——'
      '这些是"同一题干 + 不同数据"的变体题，练熟一种就整类都会了。</li>'
      '<li><b>反向题</b>：<code>QUELLE EST L\'AFFIRMATION FAUSSE ?</code>（错误的说法是哪个）出现 15 次，'
      '"正确说法"11 次。看到 FAUSSE 要立刻警觉，别顺手选对的那个。</li>'
      '<li><b>干扰项有固定套路</b>：把别的频段的限值（如 50,2–51,2 MHz 的旧规定、'
      '区域 2 的 144–148 MHz）、别的功率档（10 W / 100 W / 120 W / 250 W 反复出现）、'
      '或者把 "précaire et révocable" 与 "à égalité de droit" 对调。'
      '答"业务地位"类题时务必先看清问的是哪个频段。</li>'
      '<li><b>约 65% 的题（1748 道）带官方注释（<code>commentaire</code>）</b>，'
      '里面常常直接点出陷阱所在（如"注意不要混淆界限与带宽"、"注意不要与圭亚那 FY 混淆"）。'
      '本教材每道示例题的答案里都附了这条注释，做题时一定要看。</li>'
      '<li><b>小数点陷阱</b>：法语用逗号作小数点、用空格作千位分隔（<code>28,000 à 29,700 MHz</code>）。'
      '题干里的 <code>28,000</code> 是 28 MHz，不是 28000。</li>'
      '</ul>')
    return '\n'.join(o)


def appendix_formules():
    o = []
    A = o.append
    A('<h3 id="annexe-b">附录 B　公式与换算速查</h3>')
    A('<p class="small">下表公式均摘自 F6KGL《COURS》正文（括号内为出处小节），'
      '变量与单位按原文。除特别说明外，频率用 MHz、长度用 m。</p>')
    A('<table><thead><tr><th>用途</th><th>公式</th><th>出处</th></tr></thead><tbody>')
    rows = [
        ('欧姆定律', 'U = R · I　（即 I = U/R，R = U/I）', '§1.2'),
        ('电功率', 'P = U · I = R · I² = U² / R', '§1.2'),
        ('电阻串联', 'Rt = R1 + R2 + …', '§1.7'),
        ('电阻并联', '1/Rt = 1/R1 + 1/R2 + …；两电阻时 Rt = R1·R2 / (R1+R2)', '§1.7'),
        ('电容并联 / 串联', '并联相加 Ct = C1 + C2；串联按倒数相加（与电阻相反）', '§2.3'),
        ('线圈串联 / 并联', '串联相加；并联用得少（互感会影响结果）', '§2.3'),
        ('容抗', 'Z<sub>C</sub> = X<sub>C</sub> = 1 / (2πfC)', '§2.3f1'),
        ('感抗', 'Z<sub>L</sub> = X<sub>L</sub> = 2πfL', '§2.3f1'),
        ('阻抗（RLC 串联）', 'Z = √(R² + (X<sub>L</sub> − X<sub>C</sub>)²)', '§2.5'),
        ('谐振条件 / 谐振频率', 'X<sub>L</sub> = X<sub>C</sub> 即 ωL = 1/(ωC)；'
         'f = 1 / (2π√(LC))（汤姆孙公式）', '§4.3 / §4.6'),
        ('谐振回路简化式', 'C(pF) = 25 330 / f²(MHz)；L(µH) = 25 330 / f²(MHz)', '§4.6'),
        ('品质因数 Q', 'Q = Z / R = 1 / cos φ；对线圈 Q = 2πfL / R；对电容 Q = 1 / (2πfCR)', '§2.3e'),
        ('交流电与周期', 'f = 1 / T；周期 T = 1 / f', '§2.1'),
        ('分贝（功率比）', 'G(dB) = 10 log(Ps / Pe)；Ps = Pe × 10^(dB/10)', '§4.1'),
        ('常用 dB 值', '0 dB = ×1；3 dB ≈ ×2；6 dB ≈ ×4；7 dB ≈ ×5；9 dB ≈ ×8；10 dB = ×10', '§4.1'),
        ('变压器变比', 'N = ns / np（N>1 升压）；Us/Up = ns/np；Is/Ip = np/ns', '§3.1'),
        ('波长与频率', 'λ(m) = 300 / f(MHz)；λ(m) · f(Hz) = 300 000 000 m/s', '§9.1'),
        ('半波振子（偶极）总长', 'L(m) = 150 / f(MHz)　（实际再缩短约 5%）', '§9.4'),
        ('四分之一波长垂直天线', 'L(m) = 75 / f(MHz)　（实际再缩短约 5%）', '§9.5'),
        ('反射系数', 'ρ = Ur/Ue = (Umax − Umin)/(Umax + Umin) = √(Pr/Pe)', '§10.3'),
        ('驻波比 / 百分比', 'ROS = (1 + ρ)/(1 − ρ)；反算 ρ = (ROS − 1)/(ROS + 1)；TOS(%) = 100·ρ', '§10.3'),
        ('反射功率', 'P réfléchie = P émise · ρ²', '§10.3'),
        ('AM 占用带宽', '带宽 = 2 × 最高调制频率（如话音 300–3000 Hz → 6 kHz）', '§12.3'),
        ('AM 功率分配（100% 调制）', '载波占 2/3，两个边带各占 1/6（边带比载波低 6 dB）', '§12.3'),
    ]
    for u, f, s in rows:
        A('<tr><td>%s</td><td><code>%s</code></td><td class="small">%s</td></tr>' % (u, f, s))
    A('</tbody></table>')
    A('<div class="tips"><b>记住三条"考试友好"的换算：</b>'
      '① 波长用 300/f，天线长度用 150/f（半波）与 75/f（1/4 波）；'
      '② 分贝是"×2 就是 3 dB、×10 就是 10 dB"，10 W→2 W 就是 −7 dB；'
      '③ ROS 2/1 对应 ρ = 1/3、反射功率 = 11%（约 −9,5 dB），ROS 1,5/1 对应约 4%。</div>')
    return '\n'.join(o)


def appendix_qcode():
    o = []
    A = o.append
    A('<h3 id="annexe-c">附录 C　Q 简语速查表（考试必背的 22 个）</h3>')
    A('<p>考试只考 <b>22 个</b> Q 缩写（出自 CEPT 建议 T/R 61-02 / HAREC 大纲）。'
      '规则：<b>带问号 = 提问，不带问号 = 回答或通知</b>，后面可以再跟补充信息。</p>')
    A('<table><thead><tr><th>编码</th><th>用作提问（法语）</th><th>用作回答 / 通知</th>'
      '<th>中文含义</th></tr></thead><tbody>')
    for code, qf, qz, rf, rz in QCODE:
        A('<tr><td><b>%s</b></td><td class="fr">%s</td><td class="fr">%s</td>'
          '<td>%s → %s</td></tr>' % (code, esc(qf), esc(rf), esc(qz), esc(rz)))
    A('</tbody></table>')
    A('<div class="warn">⚠️ <b>考试以 UIT 的定义为准，不是业余界的习惯用法！</b>'
      '教材明确提醒：在业余无线电日常通话中，<b>QRK 和 QSA 的含义被互换了</b>'
      '（业余界用 QRK 表示信号强度、QSA 表示可懂度，与 UIT 定义相反），'
      'QRA、QSO、QSP、QTH 的日常含义也比 UIT 定义更窄。'
      '<b>考试按 UIT 定义答</b>。</div>')
    A('<p class="small">补充记忆法：带 1–5 评价的五个码是 <b>QRK</b>（可懂度）、'
      '<b>QRM</b>（人为干扰）、<b>QRN</b>（天电噪声）、<b>QSA</b>（信号强度）；'
      '其中"1 = 否 / 最差，5 = 是 / 最好"。例如没有受到干扰答 <code>QRM 1</code>，'
      '信号很强答 <code>QSA 5</code>。</p>')
    A('<h4>相关：RST 报告码</h4>')
    A('<p>RST = <b>R</b>eadibility（可懂度 1–5）/ <b>S</b>trength（强度，现代即 S 表读数 1–9）/ '
      '<b>T</b>one（音调，仅 CW 用）。不是 CW 通信时省略 T。</p>')
    return '\n'.join(o)


def appendix_alphabet():
    o = []
    A = o.append
    A('<h3 id="annexe-d">附录 D　国际字母解释法（table d\'épellation internationale）</h3>')
    A('<p>即法语里的字母拼读表，出自 <i>arrêté du 21/09/2000</i> 附件 I，'
      '也就是无线电规则（RR）的附录 A14，1956 年由 UIT 通过。'
      '<b>用的是英文拼写与英文读音</b>，只有一个例外：法语文本里 Z 写作 <b>Zoulou</b>，'
      '而国际/欧洲文本写作 <b>Zulu</b>。</p>')
    A('<table><thead><tr><th>字母</th><th>读法</th><th>字母</th><th>读法</th>'
      '<th>字母</th><th>读法</th></tr></thead><tbody>')
    for i in range(0, 26, 3):
        row = ALPHABET[i:i + 3]
        cells = ''.join('<td><b>%s</b></td><td class="fr">%s</td>' % (l, w) for l, w in row)
        A('<tr>%s</tr>' % cells)
    A('</tbody></table>')
    A('<div class="tips">例题：<code>F5PTC</code> 怎么拼？答：'
      '<b>Foxtrot 5 Papa Tango Charlie</b>。'
      '注意 A 在法语文本里写作 <b>ALFA</b>（不是 Alpha），J 写作 <b>JULIETT</b>（双 T），'
      'X 写作 <b>X-RAY</b>，这三处最容易写错。</div>')
    return '\n'.join(o)


def appendix_vocab():
    path = os.path.abspath(os.path.join(BASE, '..', 'data', 'vocabulaire.csv'))
    if not os.path.exists(path):
        return ''
    rows = list(csv.reader(open(path, encoding='utf-8')))
    if not rows:
        return ''
    head, body = rows[0], rows[1:]
    o = []
    A = o.append
    A('<h3 id="annexe-e">附录 E　高频词汇表（前 150 条）</h3>')
    A('<p>完整词表（约 %d 条，含中文释义、词性、频次、所属主题、备注）见同目录下的 '
      '<code>data/vocabulaire.csv</code>，可直接导入 Anki。下表是频次最高的 150 条，'
      '背不下来时至少把它们过一遍。</p>' % len(body))
    A('<table><thead><tr><th>法语</th><th>中文</th><th>类别</th><th>频次</th></tr></thead><tbody>')
    for r in body[:150]:
        if len(r) < 5:
            continue
        A('<tr><td class="fr"><b>%s</b></td><td>%s</td><td class="small">%s</td><td>%s</td></tr>'
          % (esc(r[0]), esc(r[1]), esc(r[2]), esc(r[3])))
    A('</tbody></table>')
    return '\n'.join(o)


def appendix_index(by_id, units):
    o = []
    A = o.append
    A('<h3 id="annexe-f">附录 F　锚点索引：题号 ↔ 教材小节</h3>')
    A('<p>下表把题库里出现过的全部锚点（<code>#R21b</code> 之类）按题量排序，'
      '并给出它在本教材中的位置与法语原文章节名。'
      '在 <code>Exam1</code> 里做题时，可用它直接跳到对应讲解。</p>')
    A('<table class="anchindex"><thead><tr><th>锚点</th><th>题量</th><th>教材小节</th>'
      '<th>法语章节</th></tr></thead><tbody>')
    # tous les signets, y compris ceux absorbes dans une unite
    from gen_common import questions_by_anchor
    idx = questions_by_anchor()
    owner = {}
    for u in units:
        for a in (u.get('anchors') or []):
            owner[a] = u
        owner.setdefault(u['id'], u)
    for a, qs in sorted(idx.items(), key=lambda x: -len(x[1])):
        if not a:
            continue
        u = owner.get(a)
        if u is None:
            continue
        A('<tr><td><code>#%s</code></td><td>%d</td>'
          '<td><a href="#%s">§%s</a></td><td class="small">%s</td></tr>'
          % (a, len(qs),
             owner.get(a, u)['id'] if a in owner else u['id'],
             esc(u['ref']), esc(u['title_fr'][:60])))
    A('</tbody></table>')
    return '\n'.join(o)


def appendix_warns(warns):
    o = []
    A = o.append
    A('<h3 id="annexe-g">附录 G　待核实事项汇总</h3>')
    A('<p>下面这些地方，F6KGL 教材原文没有写清楚、或者不同资料之间有出入，'
      '本教材没有替它补数字，而是就地标了「⚠️ 待核实」。'
      '如果你要用的正是这些内容，请以 ANFR 官方文件与现行 <i>arrêté</i> 为准。</p>')
    if not warns:
        A('<p>（本次生成未收集到待核实条目。）</p>')
    else:
        A('<ol>')
        seen = set()
        for ref, w in warns:
            k = (ref, w)
            if k in seen:
                continue
            seen.add(k)
            A('<li><b>§%s</b>：%s</li>' % (esc(ref), esc(w)))
        A('</ol>')
    A('<p class="small">生成时间：2026-10-01。法规随时可能修订，'
      '考试前请核对 ANFR 公布的现行大纲与频段表。</p>')
    return '\n'.join(o)


def render(by_id, units, warns, qt):
    o = ['<hr>', '<h2 id="annexes">附录</h2>']
    o.append(appendix_tactique())
    o.append(appendix_formules())
    o.append(appendix_qcode())
    o.append(appendix_alphabet())
    o.append(appendix_vocab())
    o.append(appendix_index(by_id, units))
    o.append(appendix_warns(warns))
    return '\n'.join(o)
