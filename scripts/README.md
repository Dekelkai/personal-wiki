# 知识库检查脚本

在项目根目录运行：

```powershell
python scripts/check_kb.py
```

脚本只使用 Python 标准库，检查 UTF-8 可读性、Frontmatter 必填字段与枚举、日期、重复标题、Wiki Link 和明显敏感信息模式。失效 Wiki Link 会列出但不会导致脚本崩溃；错误会令进程返回非零状态。
