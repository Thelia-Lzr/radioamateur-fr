# 法国业余无线电考试中文备考资料

根据 F6KGL / F5KFF 备考课程与 Exam’1 题库整理，面向使用中文学习法国 CEPT/HAREC 考试内容的学习者。

## 从这里开始

- **[完整中文教材](manuel-zh.html)**：18 个大章、126 个小节，包含各章重点、每节必备法语词汇、简短考点总结与 455 道课后例题。
- **[七天冲刺计划](docs/七天冲刺教材.md)**：按法规 10/20、技术 12/20 的起点安排复习。
- **[Anki 卡组](decks/README.md)**：法规、技术、法国法规知识点和词汇卡。
- **[法语词汇表](data/vocabulaire.csv)**：1069 条中法对照词汇，可导入 Anki。

下载或克隆项目后，用浏览器打开 `manuel-zh.html`。原题图片已嵌入网页；公式使用 MathJax，首次显示公式需要网络。

## 课后题怎么用

默认显示法语题干、四个选项和原题图；翻译、重点词汇、答案与解析默认隐藏。

| 操作 | 功能 |
|---|---|
| 鼠标点击题框 | 选中当前题目 |
| 方向键 | 平滑切换选中的题目 |
| `1–4` | 选择选项，用颜色反馈对错 |
| `C` | 切换当前题目的翻译与词汇 |
| `X` | 切换当前题目的图片 |
| `Z` | 展开或收起当前题目的答案与解析 |
| `Esc` | 退出选题 |
| 重做本题 | 恢复该题初始状态 |

快捷键只作用于当前选中的题目，各题状态独立。正文考点词使用紫色加重；原来的核对过程已精简为必要的易错提醒。

## 目录

```text
radioamateur-fr/
├── manuel-zh.html            当前可直接阅读的完整教材
├── README.md                项目入口
├── requirements.txt         教材、卡组维护工具依赖
├── THIRD_PARTY_NOTICES.md    来源、署名与许可范围
├── decks/                   8 份 Anki 卡包及选择说明
├── data/                    可导入词汇表
├── docs/                    冲刺计划与维护说明
├── source/                  生成器、翻译、讲解与原始素材
│   ├── Exam1/               上游模拟软件、2692 道题及原题图
│   ├── Exam1RA/             Android 版参考源码
│   ├── study_guide.json     各章考点、总结和强调词
│   ├── study_polish.py      内容精简、总结及异色强调
│   └── manual_quiz.py       课后题渲染与交互
├── tools/                   当前项目完整性检查工具
└── archive/                 历史教材、公式补丁、旧基线与编辑工具
```

当前使用入口与历史材料已分开，旧文件保留在 [归档目录](archive/README.md)。上游源码以普通文件副本保存，不上传嵌套 Git 元数据。缓存、虚拟环境及本机配置由 `.gitignore` 排除。

## 维护

完整说明见 [维护说明](docs/维护说明.md)。安装依赖后可检查项目或生成教材草稿：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/verify_project.py
.venv/bin/python source/gen_manuel.py --output /tmp/radioamateur-draft.html
```

当前成品包含历次人工公式与文字修订。生成草稿后应与成品比较，再决定是否替换。卡组内教材是其打包时的副本，网页更新不会自动修改已导入的卡片。

## 来源与许可

中文教材根据 F6KGL / F5KFF《COURS》（2025 年 11 月版）改编，遵循 **CC BY-NC-SA 4.0**：署名、非商业性使用、相同方式共享。原题、选项、图像与注释来自 [F4JTV/Exam1](https://github.com/F4JTV/Exam1)。第三方代码与素材保留各自权利，详见 [来源与署名](THIRD_PARTY_NOTICES.md)。

本项目为学习辅助材料，与 ANFR、Arcep 等官方机构无隶属关系。考试安排与法规以 [ANFR 公布的现行资料](https://www.anfr.fr/gerer/radioamateurs/les-certificats/page)为准；练习题库的题量分布不代表正式考试的抽题比例。
