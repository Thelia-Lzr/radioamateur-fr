# -*- coding: utf-8 -*-
# 中文教材正文：区块 W3

SECTIONS = [
    {
        "id": "R31",
        "ref": "R-3.1",
        "title_zh": "国际字母解释法（呼号拼读表）",
        "title_fr": "Table d'épellation internationale",
        "body": """<p><b>国际字母解释法</b>（table d'épellation internationale）是通联，尤其是短波弱信号条件下交换呼号（indicatif）的基本工具。法语教材把这张表列在 21/09/00 部令（arrêté du 21/09/00）附件 I 中；它同时也是《无线电规则》（RR）附录 A14 的内容，由国际电信联盟（UIT）于 1956 年通过。在这之前，字母的拼读词早在 1927 年华盛顿会议上就已确定，当时用的是城市或国家名（A 用 Amsterdam、B 用 Baltimore、C 用 Canada 等），旧表中只有 Q 的 <b>Quebec</b> 被新表继承下来。</p>
<p>这张表是国际通用的，因此字母的<b>拼写和发音都按英语</b>。唯一的例外是字母 Z：<b>法语文本把它写作 ZOULOU</b>，而国际文本和欧洲文本写作 <b>Zulu</b>。考试按法语文本作答，问到 Z 时答 <b>Zoulou</b>。</p>
<table>
<thead><tr><th>字母</th><th>拼读词（法语文本写法）</th><th>易错点</th></tr></thead>
<tbody>
<tr><td>A</td><td>ALFA</td><td>不是 ALPHA（无 H）</td></tr>
<tr><td>B</td><td>BRAVO</td><td>—</td></tr>
<tr><td>C</td><td>CHARLIE</td><td>—</td></tr>
<tr><td>D</td><td>DELTA</td><td>—</td></tr>
<tr><td>E</td><td>ECHO</td><td>—</td></tr>
<tr><td>F</td><td>FOX-TROT</td><td>写法中间带连字符</td></tr>
<tr><td>G</td><td>GOLF</td><td>—</td></tr>
<tr><td>H</td><td>HOTEL</td><td>—</td></tr>
<tr><td>I</td><td>INDIA</td><td>—</td></tr>
<tr><td>J</td><td>JULIETT</td><td>结尾双 T</td></tr>
<tr><td>K</td><td>KILO</td><td>—</td></tr>
<tr><td>L</td><td>LIMA</td><td>—</td></tr>
<tr><td>M</td><td>MIKE</td><td>—</td></tr>
<tr><td>N</td><td>NOVEMBER</td><td>—</td></tr>
<tr><td>O</td><td>OSCAR</td><td>—</td></tr>
<tr><td>P</td><td>PAPA</td><td>—</td></tr>
<tr><td>Q</td><td>QUEBEC</td><td>1927 年旧表中唯一保留下来的词</td></tr>
<tr><td>R</td><td>ROMEO</td><td>—</td></tr>
<tr><td>S</td><td>SIERRA</td><td>—</td></tr>
<tr><td>T</td><td>TANGO</td><td>—</td></tr>
<tr><td>U</td><td>UNIFORM</td><td>—</td></tr>
<tr><td>V</td><td>VICTOR</td><td>—</td></tr>
<tr><td>W</td><td>WHISKEY</td><td>—</td></tr>
<tr><td>X</td><td>X-RAY</td><td>写法中间带连字符</td></tr>
<tr><td>Y</td><td>YANKEE</td><td>—</td></tr>
<tr><td>Z</td><td>ZOULOU (zulu)</td><td>法语文本用 Zoulou，国际文本用 Zulu</td></tr>
</tbody>
</table>
<p><b>呼号里的数字不按解释法拼读</b>，而是直接读作数字。原文的例子：</p>
<div class="formula">F5PTC   → Foxtrot 5 Papa Tango Charlie
FD6JZK  → Foxtrot Delta six Juliett Zoulou Kilo
FT5TIO  → Foxtrot Tango 5 Tango India Oscar</div>
<div class="note"><p>另有一张<b>数字</b>的解释法表（table d'épellation des chiffres），原文明确指出它<b>不在考试范围内</b>，业余爱好者也很少使用，不必背诵。</p></div>
<div class="tips"><p>考试题型只有两类：给出呼号问拼读，或给出拼读问呼号。失分点几乎全在拼写细节上：<code>ALFA</code>（无 H）、<code>JULIETT</code>（双 T）、<code>FOX-TROT</code> 与 <code>X-RAY</code>（带连字符）、<code>WHISKEY</code>，以及法语文本的 <code>ZOULOU</code>。做题时先逐字母对照表，再把呼号中的数字原样读出。</p></div>""",
    },
    {
        "id": "R32",
        "ref": "R-3.2",
        "title_zh": "其余的缩写：RST 报告、code Z 与 Morse 缩写",
        "title_fr": "Abréviations en code Q (annexe I de l'arrêté du 21/09/00) — suite : code RST et abréviations en code Morse",
        "body": """<p>除 22 个必考 Q 简语外，还有三类缩写要了解。</p>
<ul>
<li><b>RST 码</b>（code RST）：电报信号报告，取自 « Readibility, Strength, Tone »，即法语 « Lisibilité, Force, Tonalité »（可读度、信号强度、音调）。非电报发射时省略 T；R 取 1 到 5，S 即 S 表（S-mètre）读数，取 1 到 9。</li>
<li><b>其他 Q 码体系</b>：UIT 建议书 M.1172 收了 77 个 Q 码（QRA 到 QTZ，QST 除外）和 64 个其他符号与缩写；另有 37 个 QOx / QUx 码只用于海上和/或航空业务；军方则用 <b>code Z</b>。</li>
<li><b>历史来源</b>：1859 年 Western Union 的 « code 92 » 中，<b>73</b> 意为 « Veuillez accepter mes hommages respectueux »（后演变为业余界的「致敬」），<b>88</b> 意为 « Affectueusement »；<b>CQ</b> 由 Marconi 于 1904 年提出、1908 年起在海事电报中普及（出自法语词 « Sécurité »）。</li>
</ul>
<p>电报通信常用的 15 个缩写（T/R 61-02 建议书）：<b>AR</b>（连写）发射结束；<b>BK</b>（Break）打断发射；<b>CQ</b> 普遍呼叫；<b>CW</b>（Continuous Waves）等幅波—电报；<b>DE</b> 分隔被叫与主叫呼号；<b>K</b> 请对方发射；<b>MSG</b> 报文；<b>PSE</b>（Please）请；<b>R</b> 收到；<b>RST</b> 可读度、强度、音调（Report）；<b>RX</b> 接收机；<b>SIG</b> 信号；<b>TX</b> 发射机；<b>UR</b>（Your）你的；<b>VA</b>（连写）一次通联结束。</p>
<p>电报考试已由 arrêté du 23/04/12 取消（原为 21/09/00 部令附件 1 第 3 部分），但这些缩写仍属 T/R 61-02 要求掌握，考试会就其中带下划线的 3 个出题。</p>
<div class="warn">⚠️ 待核实：原文说考试会考其中「3 个带下划线的缩写」，但 PDF 转文本后下划线信息丢失，无法确认是哪 3 个；从题库看重点落在 PSE、RX、TX 上。</div>
<div class="warn">⚠️ 待核实：原文 §R-3.2.d 把 TX 注为 « Emetteur »（发射机），而考题答案给的是 « Transceiver »（收发信机），两者不一致，应以题库答案为准。</div>""",
    },
    {
        "id": "R32a",
        "ref": "R-3.2.a",
        "title_zh": "必须掌握的 22 个 Q 简语（Q 码）",
        "title_fr": "Abréviations en code Q (annexe I de l'arrêté du 21/09/00)",
        "body": """<p>这 22 个 Q 简语（abréviations en code Q）来自 T/R 61-02 建议书，也就是 HAREC 的考纲。用法规则只有一条：<b>Q 码后面加问号就是提问</b>；<b>不加问号就是回答（或通知）</b>，必要时可在后面补上具体信息（频率、时刻、评分等）。</p>
<table>
<thead><tr><th>缩写</th><th>提问形式（加 ?）</th><th>回答／通知形式</th></tr></thead>
<tbody>
<tr><td><b>QRA</b></td><td>Quel est le nom de votre station?<br>你台站的名称是什么？</td><td>Le nom de ma station est…<br>我台站的名称是……</td></tr>
<tr><td><b>QRG</b></td><td>Voulez-vous m'indiquer ma fréquence exacte (ou la fréquence exacte de…)<br>请告诉我我的准确频率（或……的准确频率）？</td><td>Votre fréquence exacte (ou la fréquence exacte de…) est de… kHz (ou MHz)<br>你的准确频率（或……的准确频率）是…… kHz（或 MHz）</td></tr>
<tr><td><b>QRH</b></td><td>Ma fréquence varie-t-elle?<br>我的频率是否漂移？</td><td>Votre fréquence varie.<br>你的频率在漂移。</td></tr>
<tr><td><b>QRK</b></td><td>Quelle est l'intelligibilité de mes signaux (ou des signaux de …)?<br>我的信号（或……的信号）可懂度如何？</td><td>L'intelligibilité de vos signaux (ou des signaux de…) est: 1: mauvaise; 2: médiocre; 3: assez bonne; 4: bonne; 5: excellente<br>你的信号（或……的信号）可懂度为：1 差；2 勉强；3 尚可；4 好；5 极好</td></tr>
<tr><td><b>QRL</b></td><td>Êtes-vous occupé?<br>你忙吗？</td><td>Je suis occupé (avec…). Prière de ne pas brouiller<br>我正忙（与……），请勿干扰</td></tr>
<tr><td><b>QRM</b></td><td>Êtes-vous brouillé?<br>你是否受到干扰？</td><td>Je suis brouillé: 1: Je ne suis nullement brouillé; 2: faiblement; 3: modérément; 4: fortement; 5: très fortement<br>干扰程度：1 完全没有干扰；2 轻微；3 中等；4 强；5 极强</td></tr>
<tr><td><b>QRN</b></td><td>Êtes-vous troublé par des parasites?<br>你是否受到（天电等）噪声干扰？</td><td>Je suis troublé par des parasites: 1: Je ne suis nullement troublé par des parasites; 2: faiblement; 3: modérément; 4: fortement; 5: très fortement<br>噪声影响：1 完全没有；2 轻微；3 中等；4 强；5 极强</td></tr>
<tr><td><b>QRO</b></td><td>Dois-je augmenter la puissance d'émission?<br>要我增大发射功率吗？</td><td>Augmentez la puissance d'émission.<br>请增大发射功率。</td></tr>
<tr><td><b>QRP</b></td><td>Dois-je diminuer la puissance d'émission?<br>要我减小发射功率吗？</td><td>Diminuez la puissance d'émission.<br>请减小发射功率。</td></tr>
<tr><td><b>QRT</b></td><td>Dois-je cesser la transmission?<br>我应当停止发射吗？</td><td>Cessez la transmission.<br>请停止发射。</td></tr>
<tr><td><b>QRU</b></td><td>Avez-vous quelque chose pour moi?<br>你有东西（报文）要给我吗？</td><td>Je n'ai rien [pas de messages] pour vous.<br>我没有（没有报文）给你。</td></tr>
<tr><td><b>QRV</b></td><td>Êtes-vous prêt?<br>你准备好了吗？</td><td>Je suis prêt<br>我准备好了。</td></tr>
<tr><td><b>QRX</b></td><td>À quel moment me rappellerez-vous?<br>你何时再呼叫我？</td><td>Je vous rappellerai à… h (sur… kHz [ou MHz]).<br>我将在……时（在…… kHz 或 MHz 上）再呼叫你。</td></tr>
<tr><td><b>QRZ</b></td><td>Par qui suis-je appelé?<br>我在被谁呼叫？</td><td>Vous êtes appelé par… sur… kHz (ou MHz).<br>你在…… kHz（或 MHz）上被……呼叫。</td></tr>
<tr><td><b>QSA</b></td><td>Quelle est la force de mes signaux (ou des signaux de…)?<br>我的信号（或……的信号）强度如何？</td><td>La force de vos signaux (ou des signaux de…) est: 1: à peine perceptible; 2: faible; 3: assez bonne; 4: bonne; 5: très bonne<br>你的信号（或……的信号）强度为：1 几乎听不到；2 弱；3 尚可；4 好；5 很好</td></tr>
<tr><td><b>QSB</b></td><td>La force de mes signaux varie-t-elle?<br>我的信号强度是否在起伏？</td><td>La force de vos signaux varie.<br>你的信号强度在起伏。</td></tr>
<tr><td><b>QSL</b></td><td>Pouvez-vous me donner accusé de réception?<br>你能给我收妥确认吗？</td><td>Je vous donne accusé de réception<br>我给你收妥确认。</td></tr>
<tr><td><b>QSO</b></td><td>Pouvez-vous communiquer avec… directement (ou par relais)?<br>你能与……直接（或经中继）通信吗？</td><td>Je puis communiquer avec… directement (ou par l'intermédiaire de…).<br>我能与……直接（或经……中转）通信。</td></tr>
<tr><td><b>QSP</b></td><td>Voulez-vous retransmettre à… gratuitement?<br>你愿意免费向……转发吗？</td><td>Je peux retransmettre à… gratuitement.<br>我可以免费向……转发。</td></tr>
<tr><td><b>QSY</b></td><td>Dois-je passer à la transmission sur une autre fréquence?<br>要我换到另一个频率发射吗？</td><td>Passez à la transmission sur une autre fréquence (ou sur… kHz [ou MHz]).<br>请换到另一个频率（或…… kHz／MHz）发射。</td></tr>
<tr><td><b>QTH</b></td><td>Quelle est votre position en latitude et en longitude (ou d'après tout autre indication)?<br>你所在位置的经纬度（或任何其他定位方式）是什么？</td><td>Ma position est… latitude… longitude (ou d'après tout autre indication).<br>我的位置是……纬度……经度（或按其他定位方式）。</td></tr>
<tr><td><b>QTR</b></td><td>Quelle est l'heure exacte?<br>准确时间是多少？</td><td>L'heure exacte est…<br>准确时间是……</td></tr>
</tbody>
</table>
<p><b>用 1 到 5 评分的回答怎么理解</b>：把 1 当成「否」、5 当成「是」。因此问 QRM?（你被干扰吗？），没被干扰就答 <b>QRM 1</b>；问 QSA?（信号强吗？），信号很强就答 <b>QSA 5</b>。这一点非常容易答反。</p>
<div class="formula">QRO?                      → Dois-je augmenter ma puissance d'émission?
QRG 14050                 → Votre fréquence exacte est 14050 (kHz)
« Avez-vous quelque chose pour moi? » → QRU?
« La force de vos signaux est très bonne » → QSA 5</div>
<div class="note"><p>必考的是<b>官方通信</b>里的含义。同一个 Q 码在业余通联中常被赋予别的意思：原文指出 <b>QRA、QSO、QSP、QTH</b> 在业余界含义更窄，而 <b>QRK 与 QSA 的含义被互换</b>（在业余界 QSA 常被用来问信号强度、QRK 被用来问可懂度）。历史原因：1927 年以来 RR 一直把 QRK 定义为可懂度、QSA 定义为信号强度；1932 年制定 RST 时的工作文件却把 QRK 用于发射精确度／可懂度、QSA 用于报文可理解度，业余界沿用下来便形成了互换。<b>考试要按 UIT（官方）的含义作答</b>。</p></div>
<p>另外，QTH 与 QRA 源自海上无线电业务，分别指船舶的位置与船名（船的呼号则用 QRZ 编码）；QSO 与 QSP 的完整含义也来自报文转发的职业环境（付费转报），而不是业余爱好者的「联络」概念。</p>
<div class="tips"><p>考试会双向出题：给出含义问 Q 码（注意含义是问句就加 ?，是回答就不加），或给出 Q 码问含义。评分类（QRM、QRN、QRK、QSA）务必记住 1 = 否、5 = 是。</p></div>""",
    },
    {
        "id": "R33",
        "ref": "R-3.3",
        "title_zh": "通联的实施：呼号发送时机、避免干扰与相关义务",
        "title_fr": "Déroulement d'un contact",
        "body": """<p>ARCEP 12-1241 号决定第 4 条重述 RR 第 S25.9 条：业余电台必须<b>以很短的间隔</b>发送呼号，且至少在——</p>
<ul>
<li><b>每次发射时段的开始和结束</b>；</li>
<li>同一频率上发射超过 15 分钟时，<b>每 15 分钟</b>一次（适用于所有类型电台，包括卫星、中继和信标）；</li>
<li><b>更换发射频率</b>时，在新频率上发射时段的开始。</li>
</ul>
<p>该决定附件还要求使用者：发射前先确认不会<b>干扰</b>他人正在进行的发射（先守听再发射）；不得长期占用同一频率；不得故意干扰；不得把中继台或某种发射类别用于个人或小圈子（后两条为 02/03/21 部令新增）。</p>
<p>异频工作（同频段 <b>split</b>、跨频段 <b>cross-band</b>、经中继或转发器）是允许的，条件是发射在本人类别允许的发射类别、频段和功率之内；中继或卫星把旧 3 类操作员的报文转发到不属于他的频段也没有关系，只要操作员自己一端合规。ANFR 在调查干扰时可要求提供所用<b>软件和协议</b>的信息（12-1241 号决定前言 §4）。海上遇险程序（RR 附录 A13，已由 CMR-07 废止）与 UIT M-1171 程序不在考试范围。</p>
<div class="warn">⚠️ 待核实：本块原文 §R-3.3 讲的是「通联的实施」，并未涉及考试的科目、时长、计分与及格线；考务方面的细节需向 21/09/00 部令附件 1 的考试大纲及 ANFR 官方文件核实。</div>""",
    },
    {
        "id": "R34",
        "ref": "R-3.4",
        "title_zh": "报文内容：允许与禁止的通联",
        "title_fr": "Teneur des messages",
        "body": """<p>ARCEP 12-1241 号决定第 1 条重述了 RR 的规定：</p>
<ul>
<li>业余电台之间的发射必须限于与业余业务<b>宗旨相关</b>的通信，以及纯属<b>个人性质</b>的寒暄（RR 第 S25-2 条）。</li>
<li><b>禁止</b>对业余电台之间的发射进行编码以掩盖其含义；唯一例外是卫星业余业务中<b>地面控制站与空间站</b>之间交换的遥控指令信号，目的是保证这类电台造成的任何有害干扰能被立即消除（RR 第 S25-2A 条，即 2003 年 CMR 之后公布的条款，被 12-1241 号决定前言 §3 引用）。</li>
<li>业余电台<b>不得</b>用于传送来自非业余爱好者第三方或发给非业余爱好者第三方的通信，紧急情况或灾害救援除外（RR 第 S25-3 条）。</li>
</ul>
<p>1989 年版《业余无线电爱好者指南》（Guide du radioamateur）把可通联的题目限于：无线电技术、信息技术、天文与气象、技术期刊的内容（不得为该期刊做广告）、法规、协会生活、个人的地址与电话号码（紧急救援行动中可涉及第三方）、无线电引导（radioguidage；中继台上禁止无线电引导，业余爱好者活动的场合偶尔除外）。原文提醒：这一主题的题目会用语词陷阱来出题，例如<b>天文学（astronomie）可以谈，占星术（astrologie）不可以</b>。</p>
<p><b>通联内容的保密</b>：虽然自 1990 年起守听是自由的，但无论有意还是无意收到的通信内容，其秘密都必须保守。《刑法典》第 226-15 条（侵犯通信秘密）规定：「恶意截收、转移、使用或泄露通过电子方式发出、传送或接收的通信，或者安装用于实现此类截收的装置，处<b>一年监禁并 45 000 欧元罚金</b>」。</p>
<p>此外，《刑法典》第 R226-7 条规定：「取得或持有第 R226-1 条清单中所列的任何设备（尤其是<b>扫描接收机 scanner</b>）须经总理（Premier ministre）颁发许可」，但这类设备的<b>销售</b>是自由的——2002 年的两个判决以「欧盟规定禁止成员国限制或阻碍加贴 CE 标志设备的上市场与使用」为理由允许其上市。</p>
<div class="tips"><p>常见考法：问「哪一类话题是允许的」（法规、天文、信息技术等），或用「占星术」「商业报文」「第三方私生活信息」作干扰项，答案一律是「不允许／不得转发」。</p></div>""",
    },
    {
        "id": "R41",
        "ref": "R-4.1",
        "title_zh": "电台日志（journal de bord / carnet de trafic）",
        "title_fr": "Journal de bord",
        "body": """<p>持有发射许可的人必须在<b>电台日志</b>（journal de bord，又称 carnet de trafic，即「通信记录簿」）中记录其电台的活动。这是法国法规特有的义务，中国考试中没有对应概念，务必记牢。</p>
<p><b>必须记录的内容</b>：</p>
<ul>
<li>通信的<b>日期和时间</b>（用 UTC 或法定时间，但必须始终用同一种）；</li>
<li><b>呼号</b>（对方或中继台的）；</li>
<li><b>发射频率</b>；</li>
<li><b>发射类别</b>；</li>
<li>必要时记录<b>发射地点</b>（便携或移动时）；</li>
<li>无线电俱乐部（radio-club）还要记下<b>使用者的呼号</b>，以及在培训中完成联络的考生的姓和名。</li>
</ul>
<p>日志必须<b>随时保持最新</b>，并在负责监督的公务人员为预防干扰、便利频率使用监督而<b>提出要求时出示</b>；自最后一次登记起须<b>保存一年</b>（12-1241 号决定第 6 条）。已废止的 10-0537 号决定曾规定：通信日志可以是页码编号且不可撕下的本子，也可以以信息化方式（电子形式）保存，残疾或盲人使用者可用其他合适方式。</p>
<div class="note"><p>注意区分：必须记录的是对方的呼号、频率、日期与时间、发射类别；<b>中继台的位置不是必填项</b>。ANFR 在干扰调查中会<b>首先</b>查看 PAR 申报和电台日志。</p></div>""",
    },
    {
        "id": "R42",
        "ref": "R-4.2",
        "title_zh": "呼号使用、器材合规与台站的其他义务（§R-4.2 b、c、d、f、g）",
        "title_fr": "b à g R-4.2)",
        "body": """<p>本节是 §R-4.2 中除 a（呼号后缀）与 e（固定台申报）之外的段落。</p>
<p><b>b — 在呼号所属领土之外发射</b>：现行文本<b>没有</b>规定法国爱好者不在其呼号所配领土上发射的情形。惯例是在呼号前加发射地点的定位前缀（见 §R-4.6a）与斜杠，后接 /P 或 /M；便携或移动时还可加省（département）编号。但这些只是来自已废止旧文本的<b>惯例，不是法规义务</b>。例：住在阿尔萨斯的 Novice 在<b>马提尼克</b>或巴黎发射，用 <code>F0ABC/P</code> 即可，按惯例也可写 <code>FM/F0ABC/P</code> 或 <code>F0ABC/P75</code>，便于对方调整天线指向。</p>
<p><b>c — 航空器上的电台</b>：自 2013 年起允许在航空器（飞机、气球等）上使用无线电设备，但须符合航空法规并事先向登记国主管部门（法国民航总局 <b>DGAC</b>）取得包括飞行安全在内的所有必要许可（12-1241 号决定前言 §5.3）。此时电台属<b>移动</b>电台，呼号后加 <b>/M</b>。</p>
<p><b>d — 器材合规</b>：CPCE 第 L34-9 条要求无线电设备接受符合性评定，符合性以 <b>CE 标志</b>表示（自 2008 年起仅为自我声明）。但第 R20-3 条规定此要求<b>不适用于爱好者自制设备</b>、自用成套散件（kit）和经其改装的设备（2015-1084 号法令确认，转化 2014/30/CE 电磁兼容指令）。2014/53/EU 无线电设备指令（<b>RED</b>）由 2016-493 号条例转化为法国法，取代原 R&TTE 指令，适用于一切无线电收发信机（有线终端除外）。</p>
<p><b>f — 与互联网（ROP）的连接</b>：业余电台接入公共开放网络（réseau ouvert au public，ROP）的规则属于部长而非 ARCEP 的职权（12-1241 号决定前言 §1），该文本<b>至今未在《官方公报》（JO）公布</b>。将来可能以「采取一切措施保护公共网络的完整与安全」为条件允许接入，违规时 ARCEP 或 ANFR 可命令中止连接。<b>文本公布之前，接入互联网仍属禁止。</b></p>
<p><b>g — 征用与其他</b>：设备可依部长会议决定被临时查封和征用、且不予补偿（前言 §5.4 与 CPCE 第 L65-1 条；超过 12 天须议会表决，适用于紧急状态与戒严状态）。持有的发射设备<b>不必申报</b>，但购置或转让设备时应更新 PAR 申报；ANFR 在干扰调查中检查装置时，首先查看 PAR 申报和电台日志。</p>""",
    },
    {
        "id": "R43",
        "ref": "R-4.3",
        "title_zh": "无线电俱乐部、中继台/信标与卫星台站",
        "title_fr": "Installations de radio-club, répéteurs et satellites",
        "body": """<p><b>a — 无线电俱乐部（radio-club）</b>的设施在俱乐部呼号持有人（titulaire de l'indicatif）的责任下使用。俱乐部的设施负责人必须持有 <b>HAREC</b> 级的操作员证书（法国的「classe unique／唯一等级」，或同等证书）——<b>旧 3 类证书不够</b>。申请新呼号时，须提交主管机关签发的协会申报回执。</p>
<p>俱乐部电台可以由任何持有呼号的<b>操作员</b>使用，方式是用俱乐部呼号后跟自己的个人呼号（21/09/00 部令第 7 条修改版）。使用者必须在自己操作员类别所允许的频段、模式和功率上发射。除常规记载项目（见 §R-4.1）外，俱乐部日志还要记下电台使用者的呼号。例：操作俱乐部电台时，电报中用 « F6KGL/F6GPX »，电话中读作 « Foxtrot 6 Kilo Golf Lima opéré par Foxtrot 6 Golf Papa X-ray »。</p>
<p><b>b — 中继台与信标</b>：中继台（répétiteur／俗称 relais）在原文中定义为频率信标或其他自动装置。它可以设在使用者电台以外的另一地点，但其负责人须持有旧 3 类以外的操作员证书；不得用于个人或小圈子用途；只能发射法规允许的信息：自己的呼号、位置数据、运行数据以及影响电波传播条件的当地情况。必须设有<b>紧急关断装置</b>；出现持续干扰时，ANFR 可要求采取适当措施（这些使用条件是 2012 年以前订立的，虽无现行文本明确规定但仍在适用）。</p>
<p><b>c — 卫星</b>：RR 的 S25.11 规定，批准卫星业余业务空间电台的主管部门须确保在发射前已设置足够数量的<b>地面控制站</b>，以保证空间电台造成的任何有害干扰能被立即消除。S22.1 还规定空间电台须装有可<b>遥控立即停止发射</b>的装置。12-1241 号决定前言 §4 指出，依据 CPCE 第 L97-2 条，经营卫星系统的频率指配须取得电子通信主管部长的<b>授权</b>。</p>
<div class="tips"><p>常考两点：一是俱乐部设施负责人必须持 HAREC（非旧 3 类）证书；二是旧 3 类操作员即使在俱乐部台上也不能在自己的类别以外的频段（如 14 MHz 短波）发射。</p></div>""",
    },
    {
        "id": "R42a",
        "ref": "R-4.2.a",
        "title_zh": "呼号后缀：固定、便携、移动与海上移动",
        "title_fr": "a R-4.2)",
        "body": """<p>电台的<b>使用方式</b>通过操作员呼号后面的后缀来区分。法国的呼号是固定分配给个人的，位置与用法只靠后缀体现，这与中国按地区分配呼号的方式不同。</p>
<p><b>固定台（station fixe）</b>：不加后缀，从向 ANFR 申报的地址发射。地址的任何变更必须在 <b>2 个月</b>内通知 ANFR（21/09/00 部令第 7 条修改版）。自 2021 年起，可以向 ANFR 申报<b>两个地址</b>：操作员的住址和电台所在地址（例如他的第二住宅或其他任何地址）。</p>
<p>便携、移动或海上使用时，个人呼号后加 <b>/P</b>、<b>/M</b> 或 <b>/MM</b>（21/09/00 部令第 7 条修改版最后一段），具体情形如下：</p>
<table>
<thead><tr><th>类型</th><th>定义</th><th>电报后缀</th><th>电话读法</th></tr></thead>
<tbody>
<tr><td><b>便携台（station transportable）</b></td><td>可以搬动、但<b>在搬运途中不能工作</b>的电台</td><td>/P</td><td>Portable</td></tr>
<tr><td><b>移动台（station mobile）</b></td><td>「用于在移动中使用，或在不确定地点的停留期间使用」（RR 第 S1.67 条）</td><td>/M</td><td>Mobile</td></tr>
<tr><td><b>海上移动台（maritime mobile）</b></td><td>设在处于<b>国际水域</b>（距海岸 12 海里以外）的船舶上的电台</td><td>/MM</td><td>Maritime Mobile</td></tr>
</tbody>
</table>
<p>国际水域上的电台被视为船舶电台（RR 第 S1.77 条），受<b>船长</b>管辖（CPCE 第 D406-12 条）。设在<b>领海</b>内、江河上或停靠港口的船舶上的电台，则按<b>移动台（/M）</b>处理——内河驳船（péniche）上的电台因此属于移动台。</p>
<div class="formula">在另一位业余爱好者的固定台上以电报发射 → F5ABC/P
在车上、步行或骑车时以电话发射 → « Foxtrot Cinq Alfa Bravo Charlie Mobile »</div>
<div class="note"><p>呼号中<b>不需要</b>表示发射地点时（例如在国内的固定台），不得随意加前缀或斜杠：在法国境内通联的法国爱好者若报出 « P/F5XYZ »，在原文看来这种写法<b>没有意义</b>，因为 P 只用于表示在其他国家领土上发射。</p></div>
<div class="tips"><p>差一个字母就扣分：能搬但不能边走边用是 /P，一边移动一边用是 /M，12 海里以外的船上是 /MM。地址变更的 2 个月期限来自 21/09/00 部令第 7 条，与固定台功率申报的 2 个月期限（§R-4.2.e）是两回事。</p></div>""",
    },
    {
        "id": "R42e",
        "ref": "R-4.2.e",
        "title_zh": "固定台站的申报义务（PAR > 5 W）",
        "title_fr": "e R-4.2)",
        "body": """<p>17/12/07 部令（修改版）第 5 条规定：<b>有效辐射功率（PAR，puissance apparente rayonnée）超过 5 瓦的固定装置必须申报</b>。便携台和移动台不受此申报约束。</p>
<p>申报须在<b>安装后 2 个月内</b>送交 ANFR，内容包括：</p>
<ul>
<li>电台的<b>地址</b>（据此确定分配给它的前缀）；</li>
<li>电台的<b>地理坐标</b>：以度、分、秒表示，采用 WGS84 格式（即 GPS 坐标）；</li>
<li>在 HF、VHF、UHF、SHF <b>四个波段</b>上使用的<b>最大 PAR</b>。</li>
</ul>
<p>申报可以通过互联网在 <code>https://teleservice-amateurs.anfr.fr</code> 上办理。请注意申报内容中<b>不包含</b>天线的类型。</p>
<p>持有的发射设备不必申报，但<b>购置或转让设备时应更新 PAR 申报</b>；ANFR 在干扰调查中对装置进行检查时，会首先查看 PAR 申报和电台日志。发射功率改变时，同样应向 ANFR 更新申报。</p>
<div class="tips"><p>记三个数字：门槛 <b>5 W</b>（PAR）、期限 <b>2 个月</b>、受理机关 <b>ANFR</b>。题目的常见陷阱是问「哪些内容不必申报」——答案是天线类型。</p></div>""",
    },
]

# 该块真题的中文翻译，键为题号：{"题号": ("中文题目", "正确选项的中文")}
QT = {
    # R-3.1 国际字母解释法
    "30002": ("按照字母解释法（alphabet phonétique），字母 G 和 T 怎么拼读？", "Golf 和 Tango"),
    "30473": ("按照国际字母解释法，呼号 FD6JZK 怎么拼读？", "Foxtrot Delta six Juliett Zoulou Kilo"),
    "34779": ("呼号 FT5TIO 的拼读是？", "Foxtrot Tango 5 Tango India Oscar"),
    "50010": ("字母 K 的正确拼读是？", "Kilo"),
    # R-3.2 其他缩写
    "34705": ("缩写「PSE」是什么意思？", "请（s'il vous plaît，即 please）"),
    "35061": ("缩写「PSE」是什么意思？", "请（s'il vous plaît）"),
    "36101": ("字母 RX 代表什么？", "接收机（Receiver）"),
    "36201": ("字母 TX 代表什么？", "收发信机（Transceiver）"),
    # R-3.2.a Q 简语
    "30082": ("「你正被 HB9XYZ 呼叫」对应的代码是？", "QRZ HB9XYZ"),
    "33199": ("代码「QRT」的意思是？", "我应当停止发射吗？（Dois-je cesser la transmission ?）"),
    "70005": ("代码 QRH 的意思是？", "我的频率是否漂移？（Ma fréquence varie-t-elle ?）"),
    "70036": ("「我在被谁呼叫？」对应的 Q 码缩写是？", "QRZ"),
    # R-3.3 通联的实施
    "30031": ("业余爱好者发射之前必须确认什么？", "确认自己的发射不会干扰正在进行的其他发射"),
    "30091": ("你必须在什么时候发送自己的呼号？", "至少在每次发射的开始和结束时"),
    "30380": ("旧 3 类（Novice）操作员能否使用一颗上行 144 MHz、下行 29 MHz 的卫星？", "正确（Vrai）"),
    "31027": ("为了不产生干扰，准备发射的业余爱好者应当做什么？", "确认他将要使用的频率是空闲的"),
    "32528": ("以下哪一种说法是错误的？（A 不得长期使用同一频率；B 必须以明语发射；C 发射前要确认不会干扰正在进行的发射；D 旧 3 类操作员不得进行 cross-band 通信）", "D（cross-band 通信并非对旧 3 类操作员禁止；只要发射在其操作员类别允许的发射类别、频段与功率内即可）"),
    "34681": ("法国国家频率管理局（ANFR）能否要求业余爱好者提供其所用软件与协议的信息？", "可以，在干扰案件调查（instruction des cas de brouillage）的框架内"),
    "35053": ("在一次发射中，必须给出自己呼号的时机是：", "至少在每次发射的开始和结束时"),
    # R-3.4 报文内容
    "30078": ("业余无线电通联中允许的交谈主题是？", "业余无线电法规（réglementation radioamateur）"),
    "30199": ("你是否有权从一位业余爱好者那里接收涉及第三方私生活的报文，并将其转发给另一位业余爱好者？", "不可以，涉及私生活的信息不得转发"),
    "30420": ("2003 年世界无线电通信大会（CMR-2003）之后公布的《无线电规则》（RR）第 25.2A 条涉及什么？", "业余无线电通信的编码仅允许用于卫星控制台站（stations de commande des satellites）"),
    "30762": ("你能否接受转发一条商业报文？", "不能，任何情况下都不可以"),
    # R-4.1 电台日志
    "30010": ("电台日志（journal de bord）中必须填写的信息是？", "通信日期（date de la communication）"),
    "30079": ("以下哪一项不是电台日志中必须填写的信息？", "中继台的位置（localisation du relais）"),
    "30391": ("是否必须保留电台日志？", "是，任何情况下都必须保留"),
    "30765": ("电台日志中必须填写的内容是？", "联络时间（heure du contact）"),
    # R-4.2 b/c/d/f
    "30369": ("把业余无线电台设备连接到互联网是否被允许？", "不允许，这是禁止的"),
    "30504": ("通过什么方式可以确认一台设备符合现行法规？", "查看制造商是否给设备加贴了 CE 标志"),
    "30918": ("法国本土的旧 3 类（Novice）操作员是否有权在马提尼克（Martinique）发射？", "有权（Oui）"),
    "34720": ("能否在民航客机上操作业余无线电台？", "不能"),
    # R-4.3 俱乐部/中继/卫星
    "30699": ("某位业余爱好者搭建了一台中继台，谁可以使用它？", "所有持照的业余爱好者"),
    "32526": ("要担任无线电俱乐部（radio-club）的设施负责人，必须：", "持有旧 3 类以外的操作员证书（即 HAREC 级证书）"),
    "33020": ("旧 3 类操作员能否从无线电俱乐部在 14,115 MHz 上发射？", "不能"),
    "34700": ("业余爱好者是否有权架设信标台（balise）？", "有权"),
    # R-4.2.a 呼号后缀
    "30020": ("安装在内河驳船（péniche）上的业余电台被视作哪种电台？", "移动电台（station mobile）"),
    "30288": ("一位在法国境内通联的法国业余爱好者使用呼号 P/F5XYZ，这个呼号表示什么？", "什么都不表示（这种写法没有意义）"),
    "32506": ("取得呼号之后，任何地址变更都必须通知：", "ANFR（法国国家频率管理局）"),
    "34968": ("如果我使用另一位业余爱好者的固定台站，应使用哪个后缀？", "/P"),
    # R-4.2.e 固定台申报
    "30309": ("发射之前，业余爱好者不需要申报的是？", "所使用的天线类型（le type d'antennes utilisées）"),
    "30312": ("你有一座有效辐射功率（PAR）为 100 W 的固定台站，你有多少时间向主管部门申报？", "2 个月"),
    "34743": ("你更改了发射机的功率，应向谁申报？", "ANFR（法国国家频率管理局）"),
    "34922": ("固定台站从多大功率起必须向主管部门申报？", "5 W（PAR 超过 5 瓦）"),
}
