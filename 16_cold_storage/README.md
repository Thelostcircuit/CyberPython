# 16 // COLD STORAGE

```
[PYTHIA-9] target: coil_vault.db (sample) ── engine: SQLite 3 ── tables: 14 ── rows: 38,114
```

**Modules:** `sqlite3`, `pickle`, `pickletools`, `copyreg`, `shelve`, `marshal`, `dbm`

Iris didn't just draw a map of the vault. She smuggled out a *sample* of its database, a
week-old copy of the table that tracks every archived mind. It's SQLite: one file, no server.
Before you go anywhere near the real thing, MONTY wants you fluent in it, and in every
other way Python can persist data to disk.

> **MONTY:** The Coil will have backups, caches, snapshots of in-memory state. Some of it will
> be in formats that can **execute code when you load them**. Specifically, `pickle`. So
> today we learn how to store data, how to query it safely, and which formats you must *never*
> load from a source you don't trust.

---

## ▓ TECH BRIEFING

### `sqlite3`: a real SQL database in one file

```python
import sqlite3
conn = sqlite3.connect("vault.db")          # or ":memory:"
conn.row_factory = sqlite3.Row             # rows behave like dicts: row["name"]
conn.execute("""CREATE TABLE IF NOT EXISTS subjects (
                  id TEXT PRIMARY KEY, name TEXT NOT NULL, rack TEXT)""")

conn.execute("INSERT INTO subjects VALUES (?, ?, ?)", ("OS-ENG-4471", "Iris Vale", "C-17"))
conn.executemany("INSERT INTO subjects VALUES (?, ?, ?)", rows)
conn.execute("INSERT INTO t VALUES (:id, :name)", {"id": 1, "name": "x"})   # named style

cur = conn.execute("SELECT name FROM subjects WHERE rack LIKE ?", ("C-%",))
cur.fetchone(), cur.fetchall(), cur.rowcount
for row in conn.execute("SELECT ..."): ...

with conn:                  # a transaction: commits on success, rolls back on exception
    conn.execute(...)
conn.close()
```

**Always use `?` placeholders.** Never build SQL with f-strings. Text glued into a query can
change what the query *does* (SQL injection). Placeholders keep data as data.

`conn.backup(other)`, `conn.iterdump()` (an SQL text dump), `sqlite3.register_adapter` /
`register_converter` (custom Python types), and `conn.create_function` (Python functions
callable from SQL) are there when you need them.

### `pickle`: serialise (almost) any Python object

```python
import pickle
blob = pickle.dumps({"crew": ["dex", "sable"], "stake": 12000})
pickle.loads(blob)
with open("state.pkl", "wb") as f: pickle.dump(obj, f)
with open("state.pkl", "rb") as f: obj = pickle.load(f)
```

> ⚠ **Never unpickle data you didn't create yourself.** Loading a pickle can run arbitrary
> code by design: the format stores instructions for *rebuilding* objects, including
> "call this function". For data that crosses a trust boundary, use JSON (ch 18).

- `pickletools.dis(blob)` prints the opcodes of a pickle, and `pickletools.genops(blob)`
  iterates them. This is how you *inspect* a suspicious pickle without loading it.
- `copyreg.pickle(SomeClass, reducer)` registers how to pickle a class you can't modify.
  A reducer returns `(callable, args)` used to rebuild the object. Classes can also define
  `__reduce__` or `__getstate__`/`__setstate__` themselves.

### `shelve`: a persistent dict of pickles

```python
import shelve
with shelve.open("crew_db") as db:
    db["dex"] = {"role": "runner"}      # keys are strings, values anything picklable
    db.get("sable")
```

The same trust warning applies: it's pickle underneath.

### `dbm`: a simple persistent key-value store

```python
import dbm
with dbm.open("cache", "c") as db:     # "c" = create if missing
    db["key"] = "value"                # stored as bytes
    db["key"]                          # b'value'
```

`dbm` picks a backend: `dbm.sqlite3` (the default since 3.13), `dbm.gnu`, `dbm.ndbm`, or the
pure-Python fallback `dbm.dumb`. `dbm.whichdb(path)` identifies an existing file.

### `marshal`

`marshal` is Python's internal serialiser for code objects (it's how `.pyc` files are
written). It only handles core types, and its format can change between Python versions. Know
it exists, but use `pickle` or `json` for your own data.

```python
import marshal
marshal.loads(marshal.dumps([1, "a", b"b", 2.5]))
```

---

## ▓ THE JOB

In `job.py`:

1. **`open_vault(path)`**: connect, set `row_factory = sqlite3.Row`, create the `subjects` table if it's missing, and return the connection.
2. **`add_subjects(conn, rows)`**: `executemany` inside a transaction.
3. **`in_wing(conn, wing)`**: subjects whose rack starts with a wing letter, as dicts, sorted by id. Use a **parameter**.
4. **`rack_counts(conn)`**: `{wing_letter: count}` via SQL `GROUP BY`.
5. **`transfer(conn, subject_id, new_rack)`**: an update in a transaction. Raise `KeyError` if no such subject.
6. **`save_state` / `load_state`**: pickle to and from a file.
7. **`opcode_names(blob)`**: inspect a pickle with `pickletools.genops` **without loading it**.
8. **`register_beacon_reducer()`**: teach pickle to handle `Beacon` via `copyreg`.
9. **`shelve_put` / `shelve_get`**: `shelve`.
10. **`dbm_put` / `dbm_get`**: `dbm`, returning `str`.
11. **`marshal_roundtrip(value)`**: `marshal` there and back.
