# ============================================================
# 直接生成 Quartz 配置，不再移动或重建 content
# ============================================================

$ErrorActionPreference = "Stop"

Set-Location "F:\KnowledgeBase\personal-wiki"

# 1. 确认当前状态安全
if ((git status --porcelain).Count -gt 0) {
    git status --short
    throw "Git 工作区不干净，停止操作。"
}

if (-not (Test-Path ".\content\index.md")) {
    throw "content\index.md 不存在，停止操作。"
}

if (-not (Test-Path ".\quartz.config.default.yaml")) {
    throw "quartz.config.default.yaml 不存在，停止操作。"
}

$mdCount = (
    Get-ChildItem ".\content" -Recurse -File -Filter "*.md"
).Count

if ($mdCount -ne 50) {
    throw "Markdown 文件数量不是预期的 50，当前为：$mdCount"
}

Write-Host "当前 Markdown 文件数：$mdCount" -ForegroundColor Green


# 2. 从官方默认配置生成正式配置
Copy-Item `
    -LiteralPath ".\quartz.config.default.yaml" `
    -Destination ".\quartz.config.yaml" `
    -Force

$lines = Get-Content ".\quartz.config.yaml"
$enableExplicitPublish = $false

$result = foreach ($line in $lines) {

    # 网站名称
    if ($line -match '^\s*pageTitle:\s*Quartz 5\s*$') {
        $indent = ($line -replace '^(\s*).*$', '$1')
        "${indent}pageTitle: ""唐祥凯的个人知识库"""
        continue
    }

    # 中文区域
    if ($line -match '^\s*locale:\s*en-US\s*$') {
        $indent = ($line -replace '^(\s*).*$', '$1')
        "${indent}locale: zh-CN"
        continue
    }

    # 正式域名
    if ($line -match '^\s*baseUrl:\s*quartz\.jzhao\.xyz\s*$') {
        $indent = ($line -replace '^(\s*).*$', '$1')
        "${indent}baseUrl: wiki.tangxk.cn"
        continue
    }

    # 找到 ExplicitPublish 插件
    if (
        $line -match
        '^\s*-\s*source:\s*github:quartz-community/explicit-publish\s*$'
    ) {
        $enableExplicitPublish = $true
        $line
        continue
    }

    # 将 ExplicitPublish 从 false 改成 true
    if (
        $enableExplicitPublish -and
        $line -match '^(\s*)enabled:\s*false\s*$'
    ) {
        "$($Matches[1])enabled: true"
        $enableExplicitPublish = $false
        continue
    }

    $line

    # 在 .obsidian 后增加私有目录忽略规则
    if ($line -match '^(\s*)-\s*\.obsidian\s*$') {
        $indent = $Matches[1]
        "${indent}- _templates"
        "${indent}- _inbox"
        "${indent}- _archive"
    }
}

$result |
    Set-Content `
        -LiteralPath ".\quartz.config.yaml" `
        -Encoding utf8


# 3. 检查关键配置
Write-Host "`n[Quartz 关键配置]" -ForegroundColor Cyan

Select-String `
    -Path ".\quartz.config.yaml" `
    -Pattern `
        'pageTitle:', `
        'locale:', `
        'baseUrl:', `
        '_templates', `
        '_inbox', `
        '_archive', `
        'explicit-publish' `
    -Context 0, 1


# 4. 确认配置已生成
if (-not (Test-Path ".\quartz.config.yaml")) {
    throw "quartz.config.yaml 创建失败。"
}

Write-Host "`nquartz.config.yaml 已成功创建。" -ForegroundColor Green


# 5. 运行原知识库检查
python scripts/check_kb.py

if ($LASTEXITCODE -ne 0) {
    throw "知识库检查失败。"
}


# 6. 查看 Git 状态
Write-Host "`n[Git 状态]" -ForegroundColor Cyan
git status --short