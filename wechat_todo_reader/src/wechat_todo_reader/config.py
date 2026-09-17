"""Validated configuration for allowlisted WeChat group reads."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReaderConfig:
    """The only user-controlled groups the reader may open and inspect."""

    allowed_groups: tuple[str, ...]
    recent_message_limit: int


def load_config(path: Path) -> ReaderConfig:
    """Load a strict, non-empty group allowlist from a JSON file."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot load configuration: {error}") from error

    if not isinstance(payload, dict):
        raise ValueError("configuration root must be an object")

    groups = payload.get("allowed_groups")
    limit = payload.get("recent_message_limit")
    if not isinstance(groups, list) or not groups:
        raise ValueError("allowed_groups must be a non-empty list")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("recent_message_limit must be a positive integer")

    cleaned = tuple(group.strip() for group in groups if isinstance(group, str) and group.strip())
    if len(cleaned) != len(groups) or len(set(cleaned)) != len(cleaned):
        raise ValueError("allowed_groups must contain unique, non-empty string names")
    return ReaderConfig(allowed_groups=cleaned, recent_message_limit=limit)
