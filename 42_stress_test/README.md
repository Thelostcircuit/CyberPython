# 42 // STRESS TEST

```
[CHEESE SHOP] purchase: pytest (on the house) ── target: the countdown sequencer ── attempts available: 1
```

**Package:** [`pytest`](https://docs.pytest.org/): the test runner most Python projects use.

The last component is the **countdown sequencer**, the small program that walks the crew
through the nine minutes, step by step. Sable has already written its test suite in
pytest, the way professional teams do. Your job is to write the sequencer so that the whole
suite goes green.

> **WENSLEYDALE:** pytest, sir. Plain `assert` statements, fixtures that hand each test what it
> needs, one test run over many inputs. Read the tests carefully. They *are* the specification.
>
> **MONTY:** This time you read the tests first, then write the code. Many teams work exactly
> this way.

---

## ▓ TECH BRIEFING

Open `tests/suite/` and read along. Every idea below is used there.

### Tests are plain functions

```python
def test_parse_minutes():
    assert parse_duration("9m") == 540        # a failing assert shows both sides
```

pytest collects files named `test_*.py` and functions named `test_*`. Run it with
`uv run pytest tests/suite -v`. `-x` stops at the first failure, and `-k name` selects tests
by name.

### Parametrize: one test, many inputs

```python
@pytest.mark.parametrize("text, seconds", [("9m", 540), ("30s", 30), ("1m30s", 90)])
def test_durations(text, seconds):
    assert parse_duration(text) == seconds
```

### Fixtures: setup that tests ask for by name

```python
@pytest.fixture
def plan():
    return Sequencer([Step("call lift", 30), Step("open door", 60)])

def test_total(plan):                 # pytest sees the parameter name and calls the fixture
    assert plan.total_seconds() == 90
```

Fixtures in `conftest.py` are shared by every test file in that folder. Some are built in:
- `tmp_path`: a fresh temporary folder (a `Path`).
- `monkeypatch`: set environment variables or attributes, automatically undone afterwards.
- `capsys`: capture what was printed.

### Other tools

```python
with pytest.raises(ValueError, match="empty"):
    parse_duration("")
assert total == pytest.approx(0.3)              # float comparison with tolerance
@pytest.mark.skipif(sys.platform == "win32", reason="...")
```

---

## ▓ THE JOB

Implement everything in `job.py` so that `uv run pytest tests/suite` passes. The deck's gate
(`tests/test_job.py`) simply runs that pytest suite for you.

1. **`parse_duration(text)`**: `"9m"`, `"30s"`, `"1m30s"` → seconds.
2. **`Step`**: a small dataclass with a `name` and `seconds`.
3. **`Sequencer`**: holds steps, and has `total_seconds()`, `add()`, `timeline()` and `fits(limit)`.
4. **`load_plan(path)`** / **`save_plan(seq, path)`**: JSON on disk.
5. **`crew_name()`**: read `CREW_NAME` from the environment, defaulting to `"crew"`.
6. **`announce(seq)`**: print the timeline.
