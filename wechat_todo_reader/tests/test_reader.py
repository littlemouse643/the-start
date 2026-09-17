"""Safety-contract tests for the Windows UIA reader."""

from __future__ import annotations

import unittest

from wechat_todo_reader.reader import WeChatReader


class WeChatReaderTests(unittest.TestCase):
    """Tests that catch accidental reads from a group outside the allowlist."""

    def test_refuses_group_not_in_allowlist_before_accessing_uia(self) -> None:
        reader = WeChatReader(allowed_groups=("课程群",))

        with self.assertRaisesRegex(ValueError, "not allowlisted"):
            reader.read_group("其他群", limit=3)


if __name__ == "__main__":
    unittest.main()
