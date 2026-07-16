#!/usr/bin/env python3
"""检查 Quartz 构建产物中的内部页面和静态资源引用。"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit


LINK_ATTRIBUTES = {
    "a": ("href",),
    "audio": ("src",),
    "iframe": ("src",),
    "img": ("src",),
    "link": ("href",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "video": ("src",),
}
SKIPPED_SCHEMES = {"data", "javascript", "mailto", "tel"}


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.h1_count = 0
        self.is_redirect = False

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag == "h1":
            self.h1_count += 1
        attributes = dict(attrs)
        if tag == "meta" and (attributes.get("http-equiv") or "").lower() == "refresh":
            content = attributes.get("content") or ""
            match = re.search(r"(?:^|;)\s*url\s*=\s*['\"]?([^'\"]+)", content, re.I)
            if match:
                self.is_redirect = True
                self.links.append(match.group(1).strip())
        expected = LINK_ATTRIBUTES.get(tag)
        if not expected:
            return
        for name, value in attrs:
            if name not in expected or not value:
                continue
            if name == "srcset":
                for item in value.split(","):
                    candidate = item.strip().split(maxsplit=1)[0]
                    if candidate:
                        self.links.append(candidate)
            else:
                self.links.append(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查 Quartz HTML 内部链接和资源")
    parser.add_argument("directory", type=Path, help="Quartz 输出目录")
    parser.add_argument(
        "--base-path",
        default="/personal-wiki",
        help="站点部署子路径，默认 /personal-wiki",
    )
    return parser.parse_args()


def page_route(root: Path, html: Path) -> str:
    relative = html.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return f"/{relative[:-10]}"
    return f"/{relative[:-5]}"


def strip_base_path(path: str, base_path: str) -> str:
    normalized = "/" + base_path.strip("/") if base_path.strip("/") else ""
    if normalized and path == normalized:
        return "/"
    if normalized and path.startswith(normalized + "/"):
        return path[len(normalized) :]
    return path


def target_candidates(root: Path, url_path: str) -> list[Path]:
    decoded = unquote(url_path).lstrip("/")
    pure = PurePosixPath(decoded)
    if ".." in pure.parts:
        return []
    if not decoded or url_path.endswith("/"):
        return [root / pure / "index.html"]
    target = root.joinpath(*pure.parts)
    if pure.suffix:
        return [target]
    return [target, target.with_suffix(".html"), target / "index.html"]


def validate_directory(root: Path, base_path: str) -> int:
    root = root.resolve()
    if not root.is_dir():
        print(f"错误：构建目录不存在：{root}")
        return 1

    html_files = sorted(root.rglob("*.html"))
    errors: set[str] = set()
    checked_links = 0

    for html in html_files:
        text = html.read_text(encoding="utf-8")
        relative = html.relative_to(root).as_posix()
        if "<undefined" in text:
            errors.add(f"{relative}: 包含无效 <undefined> 元素")

        collector = LinkCollector()
        collector.feed(text)
        if not collector.is_redirect and collector.h1_count != 1:
            errors.add(f"{relative}: H1 数量为 {collector.h1_count}，应为 1")
        source_url = "https://local.invalid" + page_route(root, html)

        for raw in collector.links:
            parts = urlsplit(raw)
            if parts.scheme in SKIPPED_SCHEMES:
                continue
            if parts.netloc:
                base_prefix = "/" + base_path.strip("/")
                if not base_prefix or not (
                    parts.path == base_prefix or parts.path.startswith(base_prefix + "/")
                ):
                    continue
            if not parts.path and parts.fragment:
                continue

            resolved = urlsplit(urljoin(source_url, raw))
            path = strip_base_path(resolved.path, base_path)
            candidates = target_candidates(root, path)
            checked_links += 1
            if not candidates or not any(candidate.is_file() for candidate in candidates):
                errors.add(f"{relative}: {raw} -> {unquote(path)}")

    print("\n[站点构建检查]")
    print(f"HTML 文件数: {len(html_files)}")
    print(f"内部引用数: {checked_links}")
    print(f"错误数: {len(errors)}")
    if errors:
        for error in sorted(errors):
            print(f"- {error}")
        return 1
    return 0


def main() -> int:
    args = parse_args()
    return validate_directory(args.directory, args.base_path)


if __name__ == "__main__":
    sys.exit(main())
