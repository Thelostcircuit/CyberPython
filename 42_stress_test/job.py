"""42 // STRESS TEST: the countdown sequencer. The spec is the pytest suite in tests/suite/."""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

_DURATION = re.compile(r"(?:(\d+)m)?(?:(\d+)s)?")


def parse_duration(text: str) -> int:
    """"9m" -> 540, "30s" -> 30, "1m30s" -> 90 (minutes before seconds). Surrounding spaces
    are ignored. Anything else (including "") raises ValueError."""
    raise NotImplementedError("TODO")


@dataclass
class Step:
    name: str
    seconds: int


class Sequencer:
    """An ordered list of Steps. See tests/suite/test_sequencer.py for the exact behaviour:
    len(), total_seconds(), add(step) (returns self; negative seconds -> ValueError mentioning
    "negative"), timeline() -> [(start_second, name)], fits(limit) -> total <= limit."""

    def __init__(self, steps: list[Step] | None = None):
        self.steps: list[Step] = list(steps or [])

    pass  # TODO: __len__, total_seconds, add, timeline, fits


def save_plan(seq: Sequencer, path: str | Path) -> None:
    """Write the steps as a JSON list of {"name", "seconds"} objects."""
    raise NotImplementedError("TODO")


def load_plan(path: str | Path) -> Sequencer:
    raise NotImplementedError("TODO")


def crew_name() -> str:
    """The CREW_NAME environment variable, or "crew"."""
    raise NotImplementedError("TODO")


def announce(seq: Sequencer) -> None:
    """Print "T+MM:SS <name>" for each timeline entry, then "total MM:SS"."""
    raise NotImplementedError("TODO")
