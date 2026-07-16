#!/usr/bin/env python3
"""检查个人知识库的 Frontmatter、Wiki Link、编码与敏感信息风险。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SCHEMA = ROOT / "schemas" / "frontmatter.schema.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")
SENSITIVE = (
    ("API Key", re.compile(r"(?i)api[_ -]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")),
    ("Token", re.compile(r"(?i)(?:access[_ -]?)?token\s*[:=]\s*['\"]?[A-Za-z0-9_.\-]{12,}")),
    ("password", re.compile(r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
    ("secret", re.compile(r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9_.\-]{12,}")),
    ("私钥头", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
DEFAULT_LINK_LIMIT = 10


def load_schema_contract() -> tuple[tuple[str, ...], dict[str, set[str]]]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = schema.get("required")
    properties = schema.get("properties", {})
    if not isinstance(required, list) or not all(
        isinstance(item, str) for item in required
    ):
        raise ValueError("Schema required 必须为字符串数组")

    enums: dict[str, set[str]] = {}
    for field in ("type", "domain", "status"):
        values = properties.get(field, {}).get("enum")
        if not isinstance(values, list) or not all(
            isinstance(item, str) for item in values
        ):
            raise ValueError(f"Schema {field}.enum 必须为字符串数组")
        enums[field] = set(values)
    return tuple(required), enums


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查个人知识库 Markdown 文件")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示每个来源文件中的全部失效 Wiki Link",
    )
    return parser.parse_args()


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


def display_grouped_broken_links(
    broken_by_file: dict[Path, list[str]], *, verbose: bool
) -> None:
    if not broken_by_file:
        return

    print("\n[失效 Wiki Link 警告]")
    for path in sorted(broken_by_file, key=lambda item: item.as_posix()):
        links = broken_by_file[path]
        shown = links if verbose else links[:DEFAULT_LINK_LIMIT]
        print(f"- {path}（{len(links)} 个）")
        for raw in shown:
            print(f"  - [[{raw}]]")
        hidden = len(links) - len(shown)
        if hidden:
            print(f"  - 另有 {hidden} 个未显示")


def main() -> int:
    args = parse_args()
    try:
        required, enums = load_schema_contract()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print("\n[错误]")
        print(f"- 无法读取 Frontmatter Schema：{exc}")
        return 1

    files = sorted(CONTENT.rglob("*.md"))
    errors: list[str] = []
    general_warnings: list[str] = []
    broken_by_file: defaultdict[Path, list[str]] = defaultdict(list)
    titles: defaultdict[str, list[Path]] = defaultdict(list)
    texts: dict[Path, str] = {}

    stems = {path.stem for path in files}
    relative_no_ext = {
        path.relative_to(CONTENT).with_suffix("").as_posix() for path in files
    }

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            errors.append(f"{rel}: 无法按 UTF-8 读取：{exc}")
            continue
        texts[path] = text

        if "_templates" in path.parts:
            continue

        frontmatter, problem = parse_frontmatter(text)
        if problem:
            errors.append(f"{rel}: {problem}")
            continue

        for field in required:
            if not frontmatter.get(field):
                errors.append(f"{rel}: 缺少必填字段 {field}")

        title = frontmatter.get("title")
        if title:
            titles[title].append(path)
        if frontmatter.get("type") and frontmatter["type"] not in enums["type"]:
            errors.append(f"{rel}: type 值无效：{frontmatter['type']}")
        if frontmatter.get("domain") and frontmatter["domain"] not in enums["domain"]:
            errors.append(f"{rel}: domain 值无效：{frontmatter['domain']}")
        if frontmatter.get("status") and frontmatter["status"] not in enums["status"]:
            errors.append(f"{rel}: status 值无效：{frontmatter['status']}")
        if frontmatter.get("publish") not in {"true", "false"}:
            errors.append(f"{rel}: publish 必须为 true 或 false")
        for field in ("created", "updated"):
            value = frontmatter.get(field, "")
            if value and not DATE_RE.fullmatch(value):
                errors.append(f"{rel}: {field} 日期格式无效：{value}")

    for title, paths in sorted(titles.items()):
        if len(paths) > 1:
            joined = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"重复 title「{title}」：{joined}")

    for path, text in texts.items():
        rel = path.relative_to(ROOT)
        is_template = "_templates" in path.parts
        for raw in WIKI_RE.findall(text):
            target = link_target(raw)
            if not target or (is_template and "{{" in target):
                continue
            if target not in stems and target not in relative_no_ext:
                broken_by_file[rel].append(raw)

        if not is_template:
            for label, pattern in SENSITIVE:
                if pattern.search(text):
                    general_warnings.append(
                        f"{rel}: 发现可能的敏感信息模式（{label}）"
                    )

    broken_count = sum(len(links) for links in broken_by_file.values())
    warning_count = len(general_warnings) + broken_count
    index_rel = Path("content/index.md")
    index_broken_count = len(broken_by_file.get(index_rel, []))

    if errors:
        print("\n[错误]")
        for item in errors:
            print(f"- {item}")
    if general_warnings:
        print("\n[其他警告]")
        for item in general_warnings:
            print(f"- {item}")
    display_grouped_broken_links(broken_by_file, verbose=args.verbose)

    print("\n[汇总]")
    print(f"扫描文件数: {len(files)}")
    print(f"错误数: {len(errors)}")
    print(f"警告数: {warning_count}")
    print(f"失效链接数: {broken_count}")
    print(f"首页失效链接数: {index_broken_count}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
