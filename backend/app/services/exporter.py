"""Utilities for exporting pipeline outputs in JSON/Markdown."""

from __future__ import annotations

import json


def to_markdown(title: str, payload: dict) -> str:
    return "\n".join([
        f"# {title}",
        "",
        "```json",
        json.dumps(payload, indent=2),
        "```",
    ])
