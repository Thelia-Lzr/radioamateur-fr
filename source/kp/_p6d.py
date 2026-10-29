# -*- coding: utf-8 -*-
import json, re
OUT = '/home/thelia/Documents/radioamateur-fr/source/kp/out_6.json'
d = json.load(open(OUT))

# K086: 加两段说明
b = d['K086']['body']
b = b.replace("## 判据\n",
 """## 混频在收发机里的用途
混频是收发机的基本环节：**发射端**把话音谱搬（translater）到高频，**接收端**把高频搬到**中频**再做滤波与放大；课程只要求掌握**频率算术**与「**和差两条路、滤波器选一条**」这个模型。记住输出一定是**成对出现**的和频与差频，选哪一条由后级滤波器决定。
## 判据
- 先完整列一遍：**原频率 f1、f2 ＋ 2f1、2f2 ＋ f1±f2**，再补三阶，**原频率不能漏**；
""")
b = b.replace("法语卷面的固定词：mélangeur、mélanges du 2nd/3e ordre、distorsion quadratique／cubique。",
 "法语卷面的固定词：mélangeur、mélanges du 2nd/3e ordre、distorsion quadratique／cubique。二次失真的产物里**原频率仍在输出中**，这是最容易漏选的一项，也是「只写和频差频」的选项陷阱所在。")
d['K086']['body'] = b

# K087: 加判据
b = d['K087']['body']
b = b.replace("- 反射计（réflectomètre）",
 """- 两条计算路线**各有单位要求**：阻抗法只在**纯电阻**（无电抗）时成立；功率法必须**先开平方**再代入 ρ，忘了开方就会算出 1/9 之类的错值。线路上量出 Umax／Umin（有效值）同样可直接求 ROS。
- 反射计（réflectomètre）""")
d['K087']['body'] = b

# K089: 加说明
b = d['K089']['body']
b = b.replace("## 其他判据",
 """## 为什么这些细节值得记
两科目**分开评定**，所以「保留 1 年」让考生可以**分两次通过**；2 个月的等待期是补考的硬门槛。**原 3 类换 HAREC** 的价值在于 **CEPT** 互认：拿到 HAREC 后可在 CEPT 国家**免行政手续停留 3 个月以内**操作（建议 T/R 61-01 与 61-02，见国际规章知识点），而原 3 类证书本来就**不是** CEPT Novice。
## 其他判据""")
d['K089']['body'] = b

# K090: 加 Ah 段落
b = d['K090']['body']
b = b.replace("## 给电阻选瓦数",
 """## 蓄电池容量：安时（Ah）
蓄电池常用**安时 Ah** 表示容量，它就是电量：**1 Ah＝1 A×3600 s＝3600 C**。换算时先把 Ah 化成 C（或把 mA 化成 A、小时化成秒）再套 Q＝I·t，就能避开选项里「1,4 Ah」这类混排单位。
结合电能公式还能算**能量**：\(W=U\cdot Q=U\cdot I\cdot t\)。例如 12 V 蓄电池放出 1,4 Ah，能量＝12×1,4＝**16,8 Wh**＝16,8×3600＝60 480 J。判据：**电量看 Ah／C，能量看 Wh／J，功率看 W**——三个量用错就是典型错项。
## 给电阻选瓦数""")
d['K090']['body'] = b

json.dump(dict(sorted(d.items())), open(OUT, 'w'), ensure_ascii=False, indent=1)
d = json.load(open(OUT))
allok = True
for k in sorted(d):
    v = d[k]
    assert set(v) == {'title_fr','title_zh','front','body'}, (k, set(v))
    han = len(re.findall(r'[\u4e00-\u9fff]', v['body']))
    tzh = len(re.findall(r'[\u4e00-\u9fff]', v['title_zh']))
    ok = 400 <= han <= 800 and tzh <= 12
    allok &= ok
    print(k, han, 'title_zh', tzh, '' if ok else '<== CHECK')
print('ALL OK' if allok else 'NEEDS FIX')
