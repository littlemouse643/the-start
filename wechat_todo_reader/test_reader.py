"""Run the P0/P1 read-only WeChat group-message probe."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIRECTORY / "src"))

from wechat_todo_reader.cli import format_group_result
from wechat_todo_reader.config import load_config
from wechat_todo_reader.reader import WeChatReader


def main() -> int:
    config_path = PROJECT_DIRECTORY / "config.json"
    if not config_path.exists():
        print("配置：未找到 config.json；请先复制 config.example.json 并填写精确群名。")
        return 2

    try:
        config = load_config(config_path)
        reader = WeChatReader(config.allowed_groups)
        if reader.find_main_window() is None:
            print("微信窗口：未找到")
            return 1
        print("微信窗口：找到")

        for group_name in config.allowed_groups:
            messages = reader.read_group(group_name, config.recent_message_limit)
            if not messages:
                print(f"群聊：{group_name}\n最近消息：未读取到可用文本")
                return 1
            print(format_group_result(group_name, messages))
        return 0
    except (RuntimeError, ValueError) as error:
        print(f"读取失败：{error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
