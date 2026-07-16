# 知识库检查脚本

脚本只使用 Python 标准库，用于检查 Markdown 编码、Frontmatter、Wiki Link 和明显敏感信息模式。Frontmatter 必填字段以及 `type`、`domain`、`status` 枚举从 `schemas/frontmatter.schema.json` 动态读取，避免 Schema 与脚本规则分叉。

## 运行方式

在项目根目录运行默认检查：

```bash
python3 scripts/check_kb.py
```

显示全部失效 Wiki Link：

```bash
python3 scripts/check_kb.py --verbose
```

## 输出规则

- 普通文本和任务列表不是 Wiki Link，不参与链接检查。
- Schema 缺失、JSON 无法解析或核心枚举格式错误时，检查直接失败并返回非零退出码。
- 真实的 `[[Wiki Link]]` 会根据 `content/` 中现有 Markdown 文件解析。
- 默认按来源文件分组显示失效链接，每个文件最多显示前 10 个。
- 超出默认上限时显示“另有 N 个未显示”。
- `--verbose` 显示每个来源文件中的全部失效链接。
- 失效链接计入“警告数”，并单独统计“失效链接数”。
- 汇总中单独显示首页失效链接数。

## 退出码

- 存在 Frontmatter、编码等错误时返回非零退出码。
- 只有失效链接或敏感信息警告时仍返回 0，便于逐步治理内容。

脚本会检查所有正式内容目录，因此领域入口中的真实拼写错误仍会被发现。

## 本地预览私有页面

正式 Quartz 构建启用了 ExplicitPublish，因此 `publish: false` 页面不会进入公开站点。需要在本机审阅私有草稿时运行：

```bash
python3 scripts/preview_kb.py
```

然后在 Windows 浏览器访问：

```text
http://localhost:8080/
```

该脚本会在 `/tmp` 创建内容副本。默认临时开放 `content/computer-science/` 和 `content/resources/` 中的私有草稿，并继续排除 `_inbox`、`_templates`、`_archive` 和 `.obsidian`，避免维护规则和其他未审阅草稿同时出现在页面中。源 Markdown、`publish` 字段、`quartz.config.yaml`、`public/` 和部署流程均不会被修改。

预览工程或多个领域：

```bash
python3 scripts/preview_kb.py --private-root practice
python3 scripts/preview_kb.py --private-root computer-science --private-root practice
```

只有确实需要完整内部审阅时才使用：

```bash
python3 scripts/preview_kb.py --all-private
```

只验证预览构建而不启动服务：

```bash
python3 scripts/preview_kb.py --build-only
```

预览脚本会在 Quartz 构建后自动检查生成 HTML 中的页面链接、脚本、样式、图片引用和单 H1 结构。也可以单独检查正式构建产物：

```bash
python3 scripts/check_site.py public
```

默认仅监听 `127.0.0.1`。确有跨设备访问需要时才显式使用 `--host 0.0.0.0`，并先确认网络和隐私边界。

服务器同时支持根路径 `http://localhost:8080/` 和线上同构子路径 `http://localhost:8080/personal-wiki/`。左侧目录使用后者生成链接，预览服务器会自动映射到本地构建产物。未生成首页的裸目录不会暴露文件列表。
