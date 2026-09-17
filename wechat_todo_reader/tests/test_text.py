"""Text selection behavior tests."""

from __future__ import annotations

import unittest

from wechat_todo_reader.text import select_recent_texts


class SelectRecentTextsTests(unittest.TestCase):
    """Tests that catch leakage of decorative, blank, or repeated UIA names."""

    def test_removes_empty_and_duplicate_control_names(self) -> None:
        candidates = ["群成员", "你好", "", "你好", "  ", "收到", "明天见"]

        self.assertEqual(select_recent_texts(candidates, limit=3), ["你好", "收到", "明天见"])


if __name__ == "__main__":
    unittest.main()
