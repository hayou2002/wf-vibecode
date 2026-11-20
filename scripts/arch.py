#!/usr/bin/env python3
"""arch-grower 包装器:定位引擎、保护已有架构图、管理看板偏好。

用法:
  arch.py [--root <项目>] <arch 子命令> [参数...]
  arch.py dashboard on|off|status
  arch.py --root <项目> export-ui [--publish|--no-publish]
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
PREFS = HOME / ".oil-dev" / "arch-grower.json"
DASH_REL = Path("docs") / "架构看板.html"


def find_cli() -> Path:
    env = os.environ.get("ARCH_GROWER_CLI")
    if env:
        candidate = Path(env)
        if candidate.is_file():
            return candidate
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent.parent / "arch-grower" / "scripts" / "arch_cli.py",
        HOME / ".config" / "magpie" / "library" / "skills" / "arch-grower" / "scripts" / "arch_cli.py",
        HOME / ".codex" / "skills" / "arch-grower" / "scripts" / "arch_cli.py",
        HOME / ".agents" / "skills" / "arch-grower" / "scripts" / "arch_cli.py",
        HOME / ".claude" / "skills" / "arch-grower" / "scripts" / "arch_cli.py",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    sys.exit("找不到 arch-grower 引擎:请设置 ARCH_GROWER_CLI,或把 arch-grower 装到技能目录。")


def dashboard_pref() -> bool:
    try:
        return bool(json.loads(PREFS.read_text(encoding="utf-8")).get("dashboard", False))
    except (OSError, ValueError):
        return False


def set_dashboard_pref(value: str) -> int:
    value = value.lower()
    if value not in ("on", "off", "status"):
        print("用法:arch.py dashboard on|off|status")
        return 2
    if value == "status":
        print("架构看板:默认开启" if dashboard_pref() else "架构看板:默认关闭")
        return 0
    PREFS.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    try:
        data = json.loads(PREFS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    data["dashboard"] = value == "on"
    PREFS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"架构看板:默认{'开启' if data['dashboard'] else '关闭'}(记在 {PREFS})")
    return 0


def ensure_gitignore(root: Path) -> None:
    if not (root / ".git").exists() and not (root / ".gitignore").exists():
        return
    gitignore = root / ".gitignore"
    text = ""
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8", errors="replace")
    lines = {line.strip() for line in text.splitlines()}
    if ".arch/" in lines or ".arch" in lines:
        return
    prefix = "" if not text else ("" if text.endswith("\n") else "\n")
    with gitignore.open("a", encoding="utf-8") as handle:
        handle.write(prefix + "\n# arch-grower 本地架构状态\n.arch/\n")
    print("已把 .arch/ 加进 .gitignore(只留本地)")


def publish_dashboard(root: Path) -> int:
    source = root / ".arch" / "dashboard.html"
    if not source.exists():
        print("还没有看板:先跑 export-ui")
        return 1
    target = root / DASH_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"架构看板已发布:{target}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    root = Path.cwd()
    force = False
    publish = None
    rest = []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--root" and index + 1 < len(args):
            root = Path(args[index + 1]).expanduser().resolve()
            index += 2
            continue
        if arg == "--force":
            force = True
            index += 1
            continue
        if arg == "--publish":
            publish = True
            index += 1
            continue
        if arg == "--no-publish":
            publish = False
            index += 1
            continue
        rest.append(arg)
        index += 1

    if not rest:
        print(__doc__.strip())
        print("\n用法:arch.py [--root <项目>] <arch 子命令> [参数...]")
        print("      arch.py dashboard on|off|status")
        print("      arch.py --root <项目> export-ui [--publish|--no-publish]")
        return 0

    if rest[0] == "dashboard":
        return set_dashboard_pref(rest[1] if len(rest) > 1 else "status")

    if not root.is_dir():
        print(f"项目目录不存在:{root}")
        return 2

    if rest[0] == "init" and (root / ".arch" / "graph.json").exists() and not force:
        print("已有 .arch/graph.json,init 会覆盖整张架构图。")
        print("先备份,确认后再加 --force。")
        return 3

    cli = find_cli()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run([sys.executable, str(cli), *rest], cwd=root, env=env)
    if proc.returncode != 0:
        return proc.returncode

    if rest[0] == "init":
        ensure_gitignore(root)
    if rest[0] == "export-ui":
        want = dashboard_pref() if publish is None else publish
        if want:
            publish_dashboard(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
