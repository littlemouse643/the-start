"""Pure helpers for selecting visible message text."""

from __future__ import annotations

from collections.abc import Iterable


def select_recent_texts(candidates: Iterable[str], limit: int) -> list[str]:
    """Return the last unique, non-blank candidate strings in visual order."""
    selected: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        text = candidate.strip()
        if text and text not in seen:
            selected.append(text)
            seen.add(text)
    return selected[-limit:]
