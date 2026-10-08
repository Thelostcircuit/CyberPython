import json

import pytest

from job import Sequencer, Step, announce, crew_name, load_plan, parse_duration, save_plan


@pytest.mark.parametrize("text, seconds", [
    ("9m", 540), ("30s", 30), ("1m30s", 90), ("0s", 0), ("12m05s", 725), (" 2m ", 120),
])
def test_parse_duration(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize("bad", ["", "9", "m", "5h", "1s1m", "-3s"])
def test_parse_duration_rejects(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)


def test_step_is_a_value():
    assert Step("a", 5) == Step("a", 5)
    assert Step("a", 5).seconds == 5


def test_total(plan):
    assert plan.total_seconds() == 135
    assert len(plan) == 3


def test_add_returns_self(plan):
    assert plan.add(Step("stage payload", 20)) is plan
    assert plan.total_seconds() == 155


def test_add_rejects_negative(plan):
    with pytest.raises(ValueError, match="negative"):
        plan.add(Step("time travel", -1))


def test_timeline(plan):
    assert plan.timeline() == [(0, "call lift"), (30, "loop cameras"), (75, "open door")]


@pytest.mark.parametrize("limit, ok", [(135, True), (540, True), (134, False)])
def test_fits(plan, limit, ok):
    assert plan.fits(limit) is ok


def test_empty_sequencer():
    s = Sequencer()
    assert s.total_seconds() == 0
    assert s.timeline() == []


def test_save_and_load(plan, tmp_path):
    path = tmp_path / "plan.json"
    save_plan(plan, path)
    assert json.loads(path.read_text()) == [
        {"name": "call lift", "seconds": 30},
        {"name": "loop cameras", "seconds": 45},
        {"name": "open door", "seconds": 60}]
    assert load_plan(path).timeline() == plan.timeline()


def test_crew_name(monkeypatch):
    monkeypatch.delenv("CREW_NAME", raising=False)
    assert crew_name() == "crew"
    monkeypatch.setenv("CREW_NAME", "the Coil breakers")
    assert crew_name() == "the Coil breakers"


def test_announce(plan, capsys):
    announce(plan)
    assert capsys.readouterr().out == (
        "T+00:00 call lift\n"
        "T+00:30 loop cameras\n"
        "T+01:15 open door\n"
        "total 02:15\n")


def test_average_step(plan):
    assert plan.total_seconds() / len(plan) == pytest.approx(45.0)
