"""39 // CORP LEDGER: the Coil's rack records, through SQLAlchemy's ORM."""

from sqlalchemy import Engine, ForeignKey, String, create_engine, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Models (2.0 typed style):
#   Wing     table "wings":    id int PK; letter str(1) unique; racks: list[Rack] (back_populates="wing")
#   Rack     table "racks":    id int PK; code str(8) unique; wing_id FK -> wings.id;
#                              wing: Wing (back_populates="racks"); subjects: list[Subject] (back_populates="rack")
#   Subject  table "subjects": id str PK; name str; status str default "archived";
#                              rack_id FK -> racks.id, NULLABLE; rack: Rack | None (back_populates="subjects")
pass  # TODO: the three model classes


def make_engine(url: str = "sqlite://") -> Engine:
    """create_engine(url) and Base.metadata.create_all(engine)."""
    raise NotImplementedError("TODO")


def seed(engine: Engine, layout: dict[str, dict[str, list[tuple[str, str]]]]) -> None:
    """layout = {"C": {"C-17": [("OS-ENG-4471", "Iris Vale")], ...}, ...}. Create every Wing,
    Rack and Subject inside ONE transaction (with Session(engine) as s, s.begin())."""
    raise NotImplementedError("TODO")


def ids_in_wing(engine: Engine, letter: str) -> list[str]:
    """Sorted ids of subjects whose rack belongs to the wing with that letter (join query)."""
    raise NotImplementedError("TODO")


def count_by_status(engine: Engine) -> dict[str, int]:
    raise NotImplementedError("TODO")


def rack_code(engine: Engine, subject_id: str) -> str | None:
    """session.get the subject; return subject.rack.code, or None if the subject doesn't exist or
    has no rack."""
    raise NotImplementedError("TODO")


def fullest_rack(engine: Engine) -> str | None:
    """Code of the rack with the most subjects; ties go to the alphabetically lowest code.
    Do it in one query (join, group_by, order_by count desc then code, limit 1)."""
    raise NotImplementedError("TODO")


def release_all(engine: Engine, ids: list[str]) -> None:
    """In ONE transaction: for each id, set status "released" and rack = None. If any id doesn't
    exist, raise KeyError(id). The transaction must roll back so NOTHING changes."""
    raise NotImplementedError("TODO")


def raw_count(engine: Engine, status: str) -> int:
    """SELECT count(*) FROM subjects WHERE status = :status, via engine.connect() and text()."""
    raise NotImplementedError("TODO")
