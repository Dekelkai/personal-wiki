#!/usr/bin/env python3
"""检查个人知识库的 Frontmatter、链接、编码与敏感信息风险。"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
REQUIRED = ("title", "type", "domain", "status", "publish", "created", "updated")
TYPES = {"index", "concept", "method", "guide", "paper", "dataset", "project", "experiment", "decision", "troubleshooting", "reference", "article"}
DOMAINS = {"home", "research", "engineering", "ai", "projects", "writing", "reference"}
STATUSES = {"draft", "maintained", "completed", "archived"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")
SENSITIVE = (
    ("API Key", re.compile(r"(?i)api[_ -]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")),
    ("Token", re.compile(r"(?i)(?:access[_ -]?)?token\s*[:=]\s*['\"]?[A-Za-z0-9_.\-]{12,}")),
    ("password", re.compile(r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
    ("secret", re.compile(r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9_.\-]{12,}")),
    ("私钥头", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "缺少 Frontmatter 起始分隔符"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "缺少 Frontmatter 结束分隔符"
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return data, f"无法解析 Frontmatter 行：{line}"
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, None


def link_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    return target[:-3] if target.lower().endswith(".md") else target


def main() -> int:
    files = sorted(CONTENT.rglob("*.md"))
    errors: list[str] = []
    warnings: list[str] = []
    broken: list[str] = []
    titles: defaultdict[str, list[Path]] = defaultdict(list)
    texts: dict[Path, str] = {}

    stems = {path.stem for path in files}
    relative_no_ext = {path.relative_to(CONTENT).with_suffix("").as_posix() for path in files}

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            errors.append(f"{rel}: 无法按 UTF-8 读取：{exc}")
            continue
        texts[path] = text

        is_template = "_templates" in path.parts
        if is_template:
            continue

        frontmatter, problem = parse_frontmatter(text)
        if problem:
            errors.append(f"{rel}: {problem}")
            continue

        for field in REQUIRED:
            if not frontmatter.get(field):
                errors.append(f"{rel}: 缺少必填字段 {field}")

        title = frontmatter.get("title")
        if title:
            titles[title].append(path)
        if frontmatter.get("type") and frontmatter["type"] not in TYPES:
            errors.append(f"{rel}: type 值无效：{frontmatter['type']}")
        if frontmatter.get("domain") and frontmatter["domain"] not in DOMAINS:
            errors.append(f"{rel}: domain 值无效：{frontmatter['domain']}")
        if frontmatter.get("status") and frontmatter["status"] not in STATUSES:
            errors.append(f"{rel}: status 值无效：{frontmatter['status']}")
        if frontmatter.get("publish") not in {"true", "false"}:
            errors.append(f"{rel}: publish 必须为 true 或 false")
        for field in ("created", "updated"):
            value = frontmatter.get(field, "")
            if value and not DATE_RE.fullmatch(value):
                errors.append(f"{rel}: {field} 日期格式无效：{value}")

    for title, paths in sorted(titles.items()):
        if len(paths) > 1:
            joined = ", ".join(str(p.relative_to(ROOT)) for p in paths)
            errors.append(f"重复 title「{title}」：{joined}")

    for path, text in texts.items():
        rel = path.relative_to(ROOT)
        is_template = "_templates" in path.parts
        for raw in WIKI_RE.findall(text):
            target = link_target(raw)
            if not target or (is_template and "{{" in target):
                continue
            if target not in stems and target not in relative_no_ext:
                broken.append(f"{rel}: [[{raw}]]")
        if not is_template:
            for label, pattern in SENSITIVE:
                if pattern.search(text):
                    warnings.append(f"{rel}: 发现可能的敏感信息模式（{label}）")

    if errors:
        print("\n[错误]")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\n[警告]")
        for item in warnings:
            print(f"- {item}")
    if broken:
        print("\n[失效 Wiki Link]")
        for item in broken:
            print(f"- {item}")

    print("\n[汇总]")
    print(f"扫描文件数: {len(files)}")
    print(f"错误数: {len(errors)}")
    print(f"警告数: {len(warnings)}")
    print(f"失效链接数: {len(broken)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
