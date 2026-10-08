# HINTS // 42 STRESS TEST

Run `uv run pytest tests/suite -v` and fix one red test at a time. Each failure shows you the
expected and actual values.

## parse_duration
<details><summary>Hint</summary>

A regex with two optional groups, `(?:(\d+)m)?(?:(\d+)s)?`, and `fullmatch` on the stripped
text. That pattern also matches the empty string, so reject empty input separately.
</details>

## Sequencer
<details><summary>Hint</summary>

`timeline()` keeps a running start time: append `(t, step.name)`, then `t += step.seconds`.
`add()` checks for negative seconds, appends, and `return self`.
</details>

## save_plan / load_plan
<details><summary>Hint</summary>

`json.dumps([{"name": s.name, "seconds": s.seconds} for s in seq.steps])`, and the reverse
with `Step(d["name"], d["seconds"])`.
</details>

## crew_name / announce
<details><summary>Hint</summary>

`os.environ.get("CREW_NAME", "crew")`. For the times: `f"{n // 60:02d}:{n % 60:02d}"`.
</details>
