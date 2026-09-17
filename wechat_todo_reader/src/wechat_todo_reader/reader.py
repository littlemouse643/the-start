"""Strictly read-only Windows UI Automation access to an existing WeChat UI."""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

from .text import select_recent_texts


class WeChatReader:
    """Reads visible UIA text from explicitly allowlisted WeChat group chats."""

    def __init__(self, allowed_groups: tuple[str, ...]) -> None:
        self._allowed_groups = frozenset(allowed_groups)

    @staticmethod
    def _automation() -> Any:
        try:
            import uiautomation as auto
        except ImportError as error:
            raise RuntimeError(
                "uiautomation is unavailable; install requirements.txt with a Windows Python runtime"
            ) from error
        return auto

    @staticmethod
    def _safe_value(control: Any, attribute: str) -> str:
        try:
            return str(getattr(control, attribute, "") or "")
        except Exception:
            return ""

    @classmethod
    def _walk(cls, control: Any, *, max_depth: int = 6) -> Iterator[Any]:
        stack: list[tuple[Any, int]] = [(control, 0)]
        while stack:
            current, depth = stack.pop()
            yield current
            if depth >= max_depth:
                continue
            try:
                children = current.GetChildren() or []
            except Exception:
                children = []
            stack.extend((child, depth + 1) for child in reversed(children))

    def find_main_window(self) -> Any | None:
        """Find a visible top-level WeChat window without launching or activating it."""
        auto = self._automation()
        root = auto.GetRootControl()
        try:
            windows = root.GetChildren() or []
        except Exception:
            return None

        for window in windows:
            title = self._safe_value(window, "Name")
            class_name = self._safe_value(window, "ClassName")
            if title in {"微信", "WeChat"} or "WeChat" in class_name:
                return window
        return None

    def _find_visible_group(self, window: Any, group_name: str) -> Any | None:
        for control in self._walk(window):
            if self._safe_value(control, "Name") == group_name:
                return control
        return None

    def _find_message_list(self, window: Any) -> Any | None:
        for control in self._walk(window):
            if self._safe_value(control, "AutomationId") == "chat_message_list":
                return control
        return None

    @staticmethod
    def _select_group(group: Any) -> None:
        """Select an allowlisted conversation without touching its message composer."""
        try:
            group.Click()
        except Exception as error:
            raise RuntimeError("could not select the allowlisted group through UIA") from error

    def _read_visible_message_texts(self, message_list: Any, limit: int) -> list[str]:
        candidates: list[str] = []
        for child in self._walk(message_list, max_depth=2):
            class_name = self._safe_value(child, "ClassName")
            if class_name in {"mmui::ChatTextItemView", "mmui::ChatBubbleItemView"}:
                candidates.append(self._safe_value(child, "Name"))
        return select_recent_texts(candidates, limit)

    def read_group(self, group_name: str, limit: int) -> list[str]:
        """Read visible text only after enforcing the exact group-name allowlist."""
        if group_name not in self._allowed_groups:
            raise ValueError(f"group is not allowlisted: {group_name}")
        if limit < 1:
            raise ValueError("limit must be positive")

        window = self.find_main_window()
        if window is None:
            raise RuntimeError("WeChat main window was not found")

        group = self._find_visible_group(window, group_name)
        if group is None:
            raise RuntimeError(
                f"allowlisted group is not visible: {group_name}; run inspect_ui_tree.py before changing selectors"
            )

        self._select_group(group)
        time.sleep(0.5)

        message_list = self._find_message_list(window)
        if message_list is None:
            raise RuntimeError("chat_message_list was not found; run inspect_ui_tree.py")
        return self._read_visible_message_texts(message_list, limit)
