# 知识库检查脚本

脚本只使用 Python 标准库，用于检查 Markdown 编码、Frontmatter、Wiki Link 和明显敏感信息模式。

## 运行方式

在项目根目录运行默认检查：

```powershell
python scripts/check_kb.py
```

显示全部失效 Wiki Link：

```powershell
python scripts/check_kb.py --verbose
```

## 输出规则

- 普通文本和任务列表不是 Wiki Link，不参与链接检查。
- 真实的 `[[Wiki Link]]` 会根据 `content/` 中现有 Markdown 文件解析。
- 默认按来源文件分组显示失效链接，每个文件最多显示前 10 个。
- 超出默认上限时显示“另有 N 个未显示”。
- `--verbose` 显示每个来源文件中的全部失效链接。
- 失效链接计入“警告数”，并单独统计“失效链接数”。
- 汇总中单独显示首页失效链接数。

## 退出码

- 存在 Frontmatter、编码等错误时返回非零退出码。
- 只有失效链接或敏感信息警告时仍返回 0，便于逐步治理内容。

脚本不会忽略 `content/maps/`，因此知识地图中的真实拼写错误仍会被发现。
