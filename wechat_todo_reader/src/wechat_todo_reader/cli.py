"""Terminal-only presentation helpers."""

from __future__ import annotations


def format_group_result(group_name: str, messages: list[str]) -> str:
    """Render messages with their allowlisted group context and stable numbering."""
    lines = [f"群聊：{group_name}", "最近消息："]
    lines.extend(f"{index}. {message}" for index, message in enumerate(messages, start=1))
    return "\n".join(lines)
