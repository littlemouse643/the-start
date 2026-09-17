"""Terminal formatting behavior tests."""

from __future__ import annotations

import unittest

from wechat_todo_reader.cli import format_group_result


class FormatGroupResultTests(unittest.TestCase):
    """Tests that catch missing group context or unnumbered messages in output."""

    def test_numbers_messages_under_the_allowlisted_group_name(self) -> None:
        rendered = format_group_result("XXX课程群", ["第一条", "第二条"])

        self.assertEqual(rendered, "群聊：XXX课程群\n最近消息：\n1. 第一条\n2. 第二条")


if __name__ == "__main__":
    unittest.main()
