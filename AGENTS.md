# AGENTS.md

本文件约束所有参与维护本知识库的 Agent。正式知识源是 Markdown、YAML Frontmatter 与 Git。

## 修改前

1. 先搜索已有页面、标题、别名和近义概念。
2. 优先补充已有页面，不重复创建近义页面。
3. 修改现有文件前，在项目根目录 `.backup/<时间戳>/` 按原相对路径备份。
4. 不确定的信息必须标注“待验证”，不得把推测写成事实。
5. 引用外部资料时记录来源。

## 禁止事项

1. 禁止直接删除正式笔记。
2. 禁止批量移动目录。
3. 禁止未经确认修改 `publish` 字段。
4. 禁止将 `_inbox` 内容自动公开。
5. 禁止修改、移动、删除或批量复制 `F:\OneDrive\obsidian\PaperNotes` 和 `F:\Blog` 中的文件。
6. 禁止把 API Key、Token、密码、Cookie、私钥、私人服务器地址等敏感信息写入知识库。
7. 禁止创建模糊名称或为每个失效 Wiki Link 自动创建空页面。

## 内容规范

1. 文件命名、Frontmatter、Wiki Link 和 Emoji 遵守项目 README 与 `schemas/frontmatter.schema.json`。
2. Emoji 不进入文件名、路径、Frontmatter 字段名或枚举值。
3. 正式页面必须有实质内容，地图负责组织，具体页面负责解释。
4. 对正文做实质性重写时保留用户原始观点，不得将推测改写为事实。
5. Markdown 文件统一使用 UTF-8。

## 完成与交付

1. 修改完成后运行 `python scripts/check_kb.py`。
2. 根据检查结果修复本轮造成的错误，再次运行检查。
3. 最终输出修改摘要、创建文件列表、修改文件列表和仍未解决的问题。
