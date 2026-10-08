import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # make job.py importable

from job import Sequencer, Step  # noqa: E402


@pytest.fixture
def plan():
    return Sequencer([Step("call lift", 30), Step("loop cameras", 45), Step("open door", 60)])
