"""Types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Action:
    tool: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    verdict: str  # "allow" | "ask" | "block"
    reason: str
    rule: str = ""
