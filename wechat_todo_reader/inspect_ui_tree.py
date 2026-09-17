"""Print a bounded UI Automation tree for a running WeChat window.

This diagnostic never clicks, focuses, types, saves, or sends anything.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIRECTORY / "src"))
from wechat_todo_reader.reader import WeChatReader


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only WeChat UIA tree inspector")
    parser.add_argument("--depth", type=int, default=5, help="maximum tree depth (default: 5)")
    args = parser.parse_args()
    if args.depth < 0:
        parser.error("--depth must be non-negative")

    reader = WeChatReader(allowed_groups=("__diagnostic_only__",))
    try:
        window = reader.find_main_window()
    except RuntimeError as error:
        print(f"微信窗口：无法检查（{error}）")
        return 2
    if window is None:
        print("微信窗口：未找到")
        return 1

    print("微信窗口：找到")
    for control in reader._walk(window, max_depth=args.depth):
        depth = 0
        parent = control
        while parent is not window:
            depth += 1
            try:
                parent = parent.GetParentControl()
            except Exception:
                break
            if depth > args.depth:
                break
        print(
            f"{'  ' * depth}{reader._safe_value(control, 'ControlTypeName')} "
            f"Name={reader._safe_value(control, 'Name')!r} "
            f"AutomationId={reader._safe_value(control, 'AutomationId')!r} "
            f"ClassName={reader._safe_value(control, 'ClassName')!r}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
