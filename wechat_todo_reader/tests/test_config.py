"""Configuration behavior tests for the read-only reader."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from wechat_todo_reader.config import load_config


class LoadConfigTests(unittest.TestCase):
    """Tests that catch an unsafe allowlist being accepted."""

    def test_accepts_unique_nonempty_group_names(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(
                '{"allowed_groups": ["课程群", "项目群"], "recent_message_limit": 3}',
                encoding="utf-8",
            )

            config = load_config(path)

        self.assertEqual(config.allowed_groups, ("课程群", "项目群"))
        self.assertEqual(config.recent_message_limit, 3)

    def test_rejects_empty_duplicate_blank_or_zero_limit_allowlists(self) -> None:
        payloads = (
            '{"allowed_groups": [], "recent_message_limit": 3}',
            '{"allowed_groups": ["课程群", "课程群"], "recent_message_limit": 3}',
            '{"allowed_groups": ["  "], "recent_message_limit": 3}',
            '{"allowed_groups": ["课程群"], "recent_message_limit": 0}',
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            for payload in payloads:
                path.write_text(payload, encoding="utf-8")

                with self.assertRaises(ValueError):
                    load_config(path)


if __name__ == "__main__":
    unittest.main()
