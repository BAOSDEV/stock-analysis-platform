"""Report summary utilities."""

from __future__ import annotations

from typing import Any


def generate_summary(data: dict[str, Any]) -> str:
    """Format a dictionary of values as a simple summary string."""
    lines = []
    for key, value in data.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)
