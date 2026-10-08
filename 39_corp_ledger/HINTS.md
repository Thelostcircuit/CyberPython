# HINTS // 39 CORP LEDGER

## The models
<details><summary>Hint</summary>

```python
class Rack(Base):
    __tablename__ = "racks"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    wing_id: Mapped[int] = mapped_column(ForeignKey("wings.id"))
    wing: Mapped["Wing"] = relationship(back_populates="racks")
    subjects: Mapped[list["Subject"]] = relationship(back_populates="rack")
```
`Mapped[int | None]` makes a column nullable.
</details>

## seed
<details><summary>Hint</summary>

Build the objects as a tree (`wing.racks.append(rack)`, `rack.subjects = [...]`) and
`s.add(wing)`. The cascade adds the children too. Doing all wings inside one
`with Session(engine) as s, s.begin():` makes the whole seed atomic.
</details>

## ids_in_wing
<details><summary>Hint</summary>

`select(Subject.id).join(Subject.rack).join(Rack.wing).where(Wing.letter == letter).order_by(Subject.id)`,
then `s.scalars(stmt)`.
</details>

## count_by_status / fullest_rack
<details><summary>Hint</summary>

`select(Subject.status, func.count()).group_by(Subject.status)`. For the fullest rack, join
the subjects, `group_by(Rack.id)`, and `order_by(func.count(Subject.id).desc(), Rack.code)`,
then `.limit(1)`.
</details>

## release_all
<details><summary>Hint</summary>

Raise inside `with Session(engine) as s, s.begin():`. The exception leaves the `begin()`
block, which rolls back all your earlier changes.
</details>

## raw_count
<details><summary>Hint</summary>

`conn.execute(text("... WHERE status = :status"), {"status": status}).scalar_one()`
</details>
