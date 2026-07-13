# 唐祥凯的个人知识库

这是一个面向长期维护的个人 Wiki，覆盖学术研究、计算机视觉、工程技术、AI Agent、项目实践与个人写作。正式知识源为 Markdown、YAML Frontmatter 与 Git；Obsidian 用于编辑，未来计划使用 Quartz 展示。

## 目录结构

- `content/`：Obsidian Vault 与知识正文。
- `content/maps/`：五大领域知识地图。
- `content/research/`、`engineering/`、`ai/`、`projects/`、`writing/`：领域内容。
- `content/reference/`：命令、清单、排查、术语和资源。
- `content/_inbox/`：待核验和待分类内容，默认不公开。
- `content/_templates/`：标准笔记模板。
- `schemas/`：Frontmatter 规范。
- `scripts/`：本地检查工具。
- `docs/`：工程说明与后续设计文档。

Obsidian Vault 路径为 `F:\KnowledgeBase\personal-wiki\content`。

## 数据职责边界

- Personal Wiki：整理后的长期知识、项目记录与可发布内容。
- PaperNotes：现有私人论文笔记来源，本轮位于 `F:\OneDrive\obsidian\PaperNotes`，不得直接修改。
- Hexo 博客：已发布或准备发布的博客来源，本轮位于 `F:\Blog`，不得直接修改。
- 后续迁移必须先制定映射、去重、隐私和回滚方案，不进行无审查的批量复制。

## 新建笔记

1. 先全文搜索已有标题和近义概念。
2. 选择明确的中文名称；英文官方技术名称保留官方写法。
3. 从 `content/_templates/` 复制最合适的模板。
4. 填写全部必需 Frontmatter，默认 `status: draft`、`publish: false`。
5. 增加用途说明、实质内容、相关页面与待补充区域。
6. 将页面连接到合适的知识地图。

## 使用模板

模板使用 `{{title}}` 和 `{{date}}` 占位符。创建正式页面后替换所有占位符，并根据实际内容调整 `type`、`domain` 和章节；不要把模板本身发布。

## 维护知识地图

知识地图位于 `content/maps/`，负责组织领域入口和关键关系。新增重要页面时补充最相关的一张地图，避免在多张地图中重复堆叠相同链接，也不要为尚未存在的所有链接批量创建空页面。

## Agent 修改流程

1. 阅读 `AGENTS.md` 并搜索已有页面。
2. 对待修改文件创建 `.backup/<时间戳>/` 备份。
3. 小步修改并保留用户原始观点。
4. 运行 `python scripts/check_kb.py`。
5. 修复本轮错误，复检后汇总创建、修改和待确认事项。

## 隐私与发布

- `_inbox` 和新页面默认 `publish: false`。
- 未经人工确认不得修改发布状态。
- 不记录凭据、Cookie、私钥、私人服务器地址和其他敏感信息。
- 公开前检查事实、来源、版权、隐私与失效链接。

## 后续计划

后续将分阶段评估 Quartz、Git 版本管理和自动部署。当前不安装 Quartz、不配置远程 Git、不启用自动部署；实施前需先确认公开范围、构建环境、域名与隐私策略。
