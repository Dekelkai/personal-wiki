# 个人知识 Wiki

这是一个以 Markdown、YAML Frontmatter 和 Git 为规范数据源的长期知识库。内容按照稳定学科和知识对象组织，Obsidian 用于编辑，Quartz 负责公开展示。

## 知识结构

```text
知识首页
├── 计算机科学
├── 研究资料
├── 实践记录
└── 写作与输出
```

- `content/computer-science/`：算法、编程语言、系统、软件工程和人工智能；
- `content/resources/`：论文、数据集、指标、综述和参考资料；
- `content/practice/`：实验、项目、技术决策和问题排查；
- `content/writing/`：学术写作、技术报告和博客输出；
- `content/reference/`：内部维护规范，不进入默认本地预览；
- `content/_inbox/`：待核验任务，始终不公开；
- `content/_templates/`：标准页面模板；
- `content/_archive/`：历史索引与归档内容；
- `schemas/`：Frontmatter Schema；
- `scripts/`：检查与本地预览工具；
- `docs/`：项目设计、路线和试点记录。

Obsidian Vault：`F:\KnowledgeBase\personal-wiki\content`。

## 分类方法

目录回答“知识属于哪个稳定领域”，Frontmatter `type` 回答“页面是什么对象”。例如：

- 无人机绝对视觉定位：`computer-science` + `topic`；
- AerialVL：`resources` + `dataset`；
- 视觉定位误差指标：`resources` + `metric`；
- 实际复现实验：`practice` + `experiment`。

`topics` 用于表达计算机视觉、视觉定位、Go 等交叉主题，不为每个标签创建目录。

## 内容来源边界

- `personal-wiki` 保存经过整理、去重和来源标注的长期知识；
- PaperNotes、Zotero PDF、专题报告和博客是只读来源，不进行无审查批量复制；
- `publish: false` 只控制 Quartz 输出，不是敏感信息保护机制；
- 外部事实、论文结论、个人实验和推断分别表述。

## 新建或修改页面

1. 搜索已有标题、别名和近义概念；
2. 判断稳定领域和知识对象；
3. 使用 `content/_templates/` 中最接近的模板；
4. 新页面默认 `status: draft`、`publish: false`；
5. 为外部事实和研究结论保留来源；
6. 修改后运行检查和 Quartz 构建。

详细规则见 `AGENTS.md`、`schemas/frontmatter.schema.json`、`docs/内容与排版规范.md` 和 `docs/项目总览与路线图.md`。

## 检查与构建

```bash
python3 scripts/check_kb.py
node ./quartz/bootstrap-cli.mjs build
```

## 本地审阅

```bash
python3 scripts/preview_kb.py
```

浏览器访问 `http://localhost:8080/`。默认额外开放 `computer-science` 与 `resources` 中的私有草稿；其他范围见 `scripts/README.md`。

## 外部目录

以下目录只能按用户指定路径选择性读取，禁止 Agent 修改：

- `F:\OneDrive\obsidian\PaperNotes`；
- `F:\OneDrive\obsidian\Notes`；
- `F:\Blog`。
