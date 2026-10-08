# 39 // CORP LEDGER

```
[CHEESE SHOP] purchase: sqlalchemy ── target: Coil local DB (Postgres, ORM-managed) ── rehearsal: SQLite
```

**Package:** [`SQLAlchemy`](https://docs.sqlalchemy.org/en/20/): the SQL toolkit and ORM (object-relational mapper). Version 2.0 style.

At the gap, the release order and the rack records have to change *together*: every subject
marked released and unlinked from its rack, all in one transaction. If anything fails halfway,
nothing may change at all. The Coil's local database is PostgreSQL behind an SQLAlchemy ORM
layer. You'll rehearse against SQLite with the same models. SQLAlchemy doesn't care which
database it's talking to.

> **WENSLEYDALE:** SQLAlchemy lets you work with database rows as Python objects, sir, and write
> queries in Python that become proper SQL for whichever database you're on. And when you want
> raw SQL, it'll let you do that too, safely. The whole trade uses it.
>
> **MONTY:** Remember ch 16's `sqlite3`? Same ideas: tables, transactions, parameters. This is
> the industrial version.

---

## ▓ TECH BRIEFING

### Engine and models (2.0 style)

```python
from sqlalchemy import create_engine, ForeignKey, String, select, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Rack(Base):
    __tablename__ = "racks"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    subjects: Mapped[list["Subject"]] = relationship(back_populates="rack")

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[str] = mapped_column(default="archived")
    rack_id: Mapped[int | None] = mapped_column(ForeignKey("racks.id"))   # `| None` → nullable
    rack: Mapped["Rack | None"] = relationship(back_populates="subjects")

engine = create_engine("sqlite://")          # in-memory;  "postgresql+psycopg://user@host/db"
Base.metadata.create_all(engine)             # CREATE TABLE ...
```

### Sessions and transactions

```python
with Session(engine) as session:
    with session.begin():                    # commit at the end, roll back on exception
        rack = Rack(code="C-17")
        rack.subjects.append(Subject(id="OS-ENG-4471", name="Iris Vale"))
        session.add(rack)                    # the subject is added too ("cascade")

with Session(engine) as session, session.begin():   # the common one-liner
    ...
```

### Querying

```python
session.get(Subject, "OS-ENG-4471")                          # by primary key, or None
session.scalars(select(Subject).where(Subject.status == "held")).all()
session.scalars(select(Subject.id).join(Subject.rack).where(Rack.code.like("C-%"))).all()
session.execute(select(Subject.status, func.count()).group_by(Subject.status)).all()
select(Rack).order_by(Rack.code.desc()).limit(5)
subject.rack.code                                             # navigate relationships
```

Lazy-loaded relationships run their query on first access, so do it while the session is
open. `selectinload`/`joinedload` load them eagerly.

### Core and raw SQL

```python
with engine.connect() as conn:
    conn.execute(text("SELECT count(*) FROM subjects WHERE status = :s"), {"s": "held"}).scalar_one()
```

`text()` with `:named` parameters is the safe way to run raw SQL. Never format values into the
string. **Alembic**, a separate package, handles schema migrations.

---

## ▓ THE JOB

In `job.py`, using **SQLAlchemy 2.0** (every function opens its own `Session`):

1. **`Wing`**, **`Rack`** and **`Subject`**: the models described in the file.
2. **`make_engine(url)`**: create the engine and the tables.
3. **`seed(engine, layout)`**: load a nested `{wing: {rack: [(id, name), ...]}}` layout in one transaction.
4. **`ids_in_wing(engine, letter)`**: a join query, sorted.
5. **`count_by_status(engine)`**: `GROUP BY`.
6. **`rack_code(engine, subject_id)`**: follow the relationship, or return `None`.
7. **`fullest_rack(engine)`**: the rack code with the most subjects (ties: the lowest code).
8. **`release_all(engine, ids)`**: mark them released and unlink them from their racks, **atomically**. If any id is unknown, raise `KeyError` and change nothing.
9. **`raw_count(engine, status)`**: raw SQL with `text()` and a bound parameter.
