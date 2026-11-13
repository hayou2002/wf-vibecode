#!/usr/bin/env python3
"""认出项目自带的检查命令，并留下"真的跑过"的证据。

用法：
    py -3 run_checks.py list <项目> [--json]
    py -3 run_checks.py run  <项目> --yes [--only 名字] [--timeout 秒] [--json]

默认只列不跑；真要执行必须显式加 --yes。只运行识别到的白名单检查名，
不做清理、不装依赖、不碰 git。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WANTED = ("test", "lint", "typecheck", "types", "check", "build")

SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", ".next", "dist", "build"}

PACKAGE_MANAGERS = (
    ("pnpm-lock.yaml", "pnpm"),
    ("yarn.lock", "yarn"),
    ("bun.lockb", "bun"),
    ("bun.lock", "bun"),
    ("package-lock.json", "npm"),
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def read_package_scripts(root: Path) -> tuple[str, dict]:
    path = root / "package.json"
    if not path.is_file():
        return "", {}
    try:
        data = json.loads(read_text(path))
    except ValueError:
        return "", {}
    if not isinstance(data, dict):
        return "", {}
    scripts = data.get("scripts") or {}
    if not isinstance(scripts, dict):
        scripts = {}
    runner = "npm"
    for filename, name in PACKAGE_MANAGERS:
        if (root / filename).is_file():
            runner = name
            break
    return runner, {str(k): str(v) for k, v in scripts.items()}


def detect(root: Path) -> list:
    found: list = []
    runner, scripts = read_package_scripts(root)
    if scripts:
        for name in WANTED:
            if name in scripts:
                command = f"{runner} run {name}" if runner != "npm" else f"npm run {name}"
                found.append({"name": f"package:{name}", "command": command, "source": "package.json"})
    if (root / "pyproject.toml").is_file() or (root / "pytest.ini").is_file() or (root / "tox.ini").is_file():
        found.append({"name": "pytest", "command": "python -m pytest -q", "source": "Python 项目配置"})
    if (root / "Cargo.toml").is_file():
        found.append({"name": "cargo:test", "command": "cargo test", "source": "Cargo.toml"})
    if (root / "go.mod").is_file():
        found.append({"name": "go:test", "command": "go test ./...", "source": "go.mod"})
        found.append({"name": "go:vet", "command": "go vet ./...", "source": "go.mod"})
    makefile = root / "Makefile"
    if makefile.is_file():
        targets = re.findall(r"(?m)^([A-Za-z0-9_.-]+)\s*:", read_text(makefile))
        for want in ("test", "lint", "check", "build"):
            if want in targets:
                found.append({"name": f"make:{want}", "command": f"make {want}", "source": "Makefile"})
    agents = root / "AGENTS.md"
    if agents.is_file():
        text = read_text(agents)
        hits = re.findall(r"(?m)^\s*[-*]\s*`([^`\n]{4,120})`", text)
        commands = [item for item in hits if re.match(r"^[a-zA-Z]", item) and " " in item]
        for item in commands[:5]:
            found.append({"name": f"agents:{item.split()[0]}", "command": item, "source": "AGENTS.md"})
    seen = set()
    unique = []
    for item in found:
        if item["command"] in seen:
            continue
        seen.add(item["command"])
        unique.append(item)
    return unique


def tail(text: str, limit: int = 12) -> list:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return lines[-limit:]


def run_one(item: dict, root: Path, timeout: int) -> dict:
    exe = item["command"].split()[0]
    if shutil.which(exe) is None:
        return {
            "name": item["name"],
            "command": item["command"],
            "source": item["source"],
            "exit_code": None,
            "skipped": True,
            "seconds": 0.0,
            "tail": [f"这台上没有 {exe}，这一项跑不了，不算通过也不算失败"],
        }
    started = time.time()
    try:
        proc = subprocess.run(
            item["command"],
            cwd=str(root),
            shell=True,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )
        code = proc.returncode
        output = (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        code = -1
        output = f"超过 {timeout} 秒还没结束，已中断"
    except OSError as exc:
        code = -2
        output = f"起不来：{exc}"
    return {
        "name": item["name"],
        "command": item["command"],
        "source": item["source"],
        "exit_code": code,
        "skipped": False,
        "seconds": round(time.time() - started, 1),
        "tail": tail(output),
    }


def cmd_list(args) -> int:
    root = Path(args.project)
    if not root.is_dir():
        raise SystemExit(f"不是目录：{root}")
    items = detect(root)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0
    if not items:
        print("没认出这个项目自带的检查命令。")
        print("先看它的 AGENTS.md、README 和 CI 配置，用项目自己的命令跑，不要套用记忆里的。")
        return 0
    print(f"{root} 里认到这些检查：")
    width = max(len(item["name"]) for item in items)
    for item in items:
        print(f"  {item['name']:<{width}}  {item['command']}   （来自 {item['source']}）")
    print("\n确认后再执行：加 --yes。")
    return 0


def cmd_run(args) -> int:
    root = Path(args.project)
    if not root.is_dir():
        raise SystemExit(f"不是目录：{root}")
    items = detect(root)
    if args.only:
        items = [item for item in items if item["name"] == args.only]
    if not items:
        print("没有要跑的检查。先用 `list` 看看认到了什么。")
        return 0
    if not args.yes:
        print("这会真的执行下面的命令：")
        for item in items:
            print(f"  {item['command']}")
        print("\n确认没问题就加 --yes 再跑一次。")
        return 0
    results = [run_one(item, root, args.timeout) for item in items]
    failed = [item for item in results if item["exit_code"] not in (0, None)]
    skipped = [item for item in results if item.get("skipped")]
    if args.json:
        print(
            json.dumps(
                {"results": results, "failed": len(failed), "skipped": len(skipped)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if failed else 0
    for item in results:
        if item.get("skipped"):
            state = "跑不了"
        elif item["exit_code"] == 0:
            state = "通过"
        else:
            state = f"失败（退出码 {item['exit_code']}）"
        print(f"[{state}] {item['command']}   {item['seconds']}s")
        for line in item["tail"]:
            print(f"    {line}")
    print(f"\n共 {len(results)} 项，失败 {len(failed)} 项，跑不了 {len(skipped)} 项。")
    print("把上面这些命令和退出码写进交付说明，就是这次的真实验证证据。")
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_checks.py", description="认出并运行项目自带的检查")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func, helptext in (
        ("list", cmd_list, "只列出认到的检查命令"),
        ("run", cmd_run, "执行检查（需要 --yes）"),
    ):
        item = sub.add_parser(name, help=helptext)
        item.add_argument("project", help="项目目录")
        item.add_argument("--json", action="store_true", help="输出 JSON")
        if name == "run":
            item.add_argument("--yes", action="store_true", help="确认执行")
            item.add_argument("--only", help="只跑某一项")
            item.add_argument("--timeout", type=int, default=600, help="单项超时秒数，默认 600")
        item.set_defaults(func=func)
    return parser


def main(argv: list | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
