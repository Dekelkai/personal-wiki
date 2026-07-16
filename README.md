# 个人知识 Wiki

这是一个以 Markdown、YAML Frontmatter 和 Git 为规范数据源的长期知识库，内容覆盖当前研究、计算机科学与工程、人工智能、项目实验和写作输出。Obsidian 用于编辑，Quartz 负责公开展示。

## 主要目录

- `content/`：Obsidian Vault 与知识正文；
- `content/maps/`：五个领域入口的源文件目录，网页标题不使用“地图”命名；
- `content/research/`：研究主题、综述、数据集、指标、方法和论文证据；
- `content/engineering/`：计算机基础、编程语言和工程实践；
- `content/ai/`：人工智能知识与工具实践；
- `content/projects/`：项目、实验与技术决策；
- `content/reference/`：参考资料和内部维护内容；
- `content/_inbox/`：待核验任务，始终不公开；
- `content/_templates/`：笔记模板；
- `schemas/`：Frontmatter Schema；
- `scripts/`：检查与本地预览工具；
- `docs/`：项目设计、路线和试点记录。

Obsidian Vault 路径：`F:\KnowledgeBase\personal-wiki\content`。

## 内容来源边界

- `personal-wiki` 保存整理后的长期知识和项目记录；
- PaperNotes、Zotero PDF、专题报告和博客是只读来源，不进行无审查的批量复制；
- 原始材料需要先识别概念、方法、数据集、指标、论文证据和实验，再决定更新已有页面或创建新页面；
- `publish: false` 只控制 Quartz 输出，不是敏感信息保护机制。

## 新建或修改页面

1. 先搜索已有标题、别名和近义概念；
2. 判断页面属于哪种知识对象，而不是只按文件夹归类；
3. 使用 `content/_templates/` 中最接近的模板；
4. 新页面默认 `status: draft`、`publish: false`；
5. 区分外部事实、论文结论、个人实验和待验证判断；
6. 为外部事实和研究结论保留来源；
7. 修改后运行检查和 Quartz 构建。

详细规则见 `AGENTS.md`、`schemas/frontmatter.schema.json` 和 `docs/项目总览与路线图.md`。

## 检查与构建

```bash
python3 scripts/check_kb.py
node ./quartz/bootstrap-cli.mjs build
```

## 本地审阅私有研究页面

```bash
python3 scripts/preview_kb.py
```

浏览器访问 `http://localhost:8080/`。默认只额外开放 `content/research/` 中的私有草稿；其他范围和完整预览方式见 `scripts/README.md`。

## 外部目录

以下目录只能按用户指定路径选择性读取，禁止 Agent 修改：

- `F:\OneDrive\obsidian\PaperNotes`；
- `F:\Blog`。
