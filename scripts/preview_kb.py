#!/usr/bin/env python3
"""在临时副本中预览指定领域的 publish:false 正式页面。"""

from __future__ import annotations

import argparse
import http.server
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
QUARTZ_CLI = ROOT / "quartz" / "bootstrap-cli.mjs"
SITE_CHECK = ROOT / "scripts" / "check_site.py"
DEPLOY_BASE_PATH = "/personal-wiki"
IGNORED_PARTS = {"_inbox", "_templates", "_archive", ".obsidian", "private", "templates"}
PUBLISH_FALSE_RE = re.compile(r"^(\s*publish:\s*)false(\s*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="构建仅限本机访问的 Quartz 私有内容预览",
    )
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8080, help="HTTP 端口")
    parser.add_argument(
        "--private-root",
        action="append",
        dest="private_roots",
        metavar="目录",
        help="临时开放指定的 content 一级目录；可重复使用，默认 computer-science 和 resources",
    )
    parser.add_argument(
        "--all-private",
        action="store_true",
        help="临时开放所有正式私有页面；日常审阅不建议使用",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="只验证临时预览构建，不启动 HTTP 服务",
    )
    return parser.parse_args()


def promote_publish_in_frontmatter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return False

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return False

    for index in range(1, end):
        newline = "\n" if lines[index].endswith("\n") else ""
        body = lines[index][:-1] if newline else lines[index]
        match = PUBLISH_FALSE_RE.fullmatch(body)
        if match:
            lines[index] = f"{match.group(1)}true{match.group(2)}{newline}"
            path.write_text("".join(lines), encoding="utf-8")
            return True
    return False


def prepare_preview_content(
    destination: Path,
    private_roots: set[str],
    all_private: bool,
) -> int:
    shutil.copytree(CONTENT, destination)
    promoted = 0
    for path in destination.rglob("*.md"):
        relative = path.relative_to(destination)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if not all_private and relative.parts[0] not in private_roots:
            continue
        if promote_publish_in_frontmatter(path):
            promoted += 1
    return promoted


class QuartzPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):  # type: ignore[no-untyped-def]
        parsed = urlsplit(self.path)
        request_path = parsed.path
        if request_path == DEPLOY_BASE_PATH:
            request_path = "/"
        elif request_path.startswith(DEPLOY_BASE_PATH + "/"):
            request_path = request_path[len(DEPLOY_BASE_PATH) :]

        query = f"?{parsed.query}" if parsed.query else ""
        self.path = request_path + query
        relative = Path(unquote(request_path.lstrip("/")))
        candidate = Path(self.directory) / relative
        if not candidate.exists() and relative.suffix == "":
            html_candidate = candidate.with_suffix(".html")
            if html_candidate.is_file():
                self.path = request_path + ".html" + query
        return super().send_head()

    def list_directory(self, path):  # type: ignore[no-untyped-def]
        self.send_error(404, "File not found")
        return None


def main() -> int:
    args = parse_args()
    private_roots = set(args.private_roots or ["computer-science", "resources"])
    missing_roots = sorted(root for root in private_roots if not (CONTENT / root).is_dir())
    if missing_roots:
        print(f"不存在的 content 目录：{', '.join(missing_roots)}")
        return 2

    with tempfile.TemporaryDirectory(prefix="personal-wiki-preview-") as temp:
        preview_root = Path(temp)
        preview_content = preview_root / "content"
        preview_output = preview_root / "public"
        promoted = prepare_preview_content(
            preview_content,
            private_roots,
            args.all_private,
        )

        print(f"临时预览目录：{preview_root}")
        scope = "全部正式私有页面" if args.all_private else ", ".join(sorted(private_roots))
        print(f"私有内容范围：{scope}")
        print(f"临时开放 publish:false 页面数：{promoted}")
        print("源文件和正式 publish 字段不会被修改。")

        command = [
            "node",
            str(QUARTZ_CLI),
            "build",
            "--directory",
            str(preview_content),
            "--output",
            str(preview_output),
        ]
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            return result.returncode

        check_result = subprocess.run(
            [sys.executable, str(SITE_CHECK), str(preview_output)],
            cwd=ROOT,
            check=False,
        )
        if check_result.returncode != 0:
            return check_result.returncode
        if args.build_only:
            print("本地私有内容预览构建成功。")
            return 0

        handler = lambda *values, **kwargs: QuartzPreviewHandler(  # noqa: E731
            *values,
            directory=str(preview_output),
            **kwargs,
        )
        server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
        print(f"本地预览：http://localhost:{args.port}/")
        print(f"子路径预览：http://localhost:{args.port}{DEPLOY_BASE_PATH}/")
        print("仅用于本机审阅；内容修改后请重启。按 Ctrl+C 停止。")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n本地预览已停止。")
        finally:
            server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
