# HINTS // 16 COLD STORAGE

## open_vault
<details><summary>Hint</summary>

`conn = sqlite3.connect(path)`, then `conn.row_factory = sqlite3.Row`, then
`conn.execute(SCHEMA)`, then `return conn`.
</details>

## add_subjects
<details><summary>Hint</summary>

```python
with conn:
    conn.executemany("INSERT INTO subjects (id, name, rack) VALUES (?, ?, ?)", rows)
```
If a row raises, the `with` block rolls the whole batch back.
</details>

## in_wing
<details><summary>Hint</summary>

`conn.execute("SELECT ... WHERE rack LIKE ? ORDER BY id", (f"{wing}-%",))`. The `%` goes in
the *parameter*, not in the SQL. `dict(row)` works on a `sqlite3.Row`.
</details>

## rack_counts
<details><summary>Hint</summary>

`SELECT substr(rack, 1, 1) AS wing, COUNT(*) AS n FROM subjects GROUP BY wing`
</details>

## transfer
<details><summary>Hint</summary>

Keep the cursor that `conn.execute(UPDATE ...)` returns. `cur.rowcount` says how many rows
changed.
</details>

## opcode_names
<details><summary>Hint</summary>

`pickletools.genops(blob)` yields `(opcode, arg, position)`. You want `opcode.name`.
</details>

## register_beacon_reducer
<details><summary>Hint</summary>

`copyreg.pickle(Beacon, _reduce_beacon)`
</details>

## shelve / dbm
<details><summary>Hint</summary>

Both open with a context manager. `shelve.open(str(path))` behaves like a dict.
`dbm.open(str(path), "c")` stores bytes, so `.decode("utf-8")` what you read back.
</details>
