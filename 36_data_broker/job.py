"""36 // DATA BROKER: the Coil registry, cleaned and cross-examined with pandas.

Columns in the CSV: id, name, rack, archived (a date), handler_id, status, activity
"""

import io

import pandas as pd


def load(csv_text: str) -> pd.DataFrame:
    """pd.read_csv from the text, with parse_dates=["archived"]."""
    raise NotImplementedError("TODO")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from `name`, drop duplicate ids keeping the LAST row for each, fill
    missing `activity` with 0.0, and reset_index(drop=True). Return a new frame."""
    raise NotImplementedError("TODO")


def with_wing(df: pd.DataFrame) -> pd.DataFrame:
    """A new frame with a "wing" column = first character of "rack". Don't modify df."""
    raise NotImplementedError("TODO")


def ids_in_wing(df: pd.DataFrame, wing: str) -> list[str]:
    """Sorted ids whose rack starts with `wing` (use with_wing and a boolean mask)."""
    raise NotImplementedError("TODO")


def count_by_wing(df: pd.DataFrame) -> dict[str, int]:
    """{wing: number of rows}, via groupby(...).size(). Values as Python ints."""
    raise NotImplementedError("TODO")


def activity_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Index: wing (sorted). Columns: "mean" and "max" of activity."""
    raise NotImplementedError("TODO")


def archived_per_month(df: pd.DataFrame) -> dict[str, int]:
    """{"YYYY-MM": number archived that month}, in chronological order.
    Use df["archived"].dt.to_period("M")."""
    raise NotImplementedError("TODO")


def with_handlers(df: pd.DataFrame, staff: pd.DataFrame) -> pd.DataFrame:
    """Left-merge staff (columns handler_id, handler) onto df on handler_id; rows with no
    matching handler get handler "unassigned". Keep df's row order."""
    raise NotImplementedError("TODO")


def release_queue(df: pd.DataFrame, n: int) -> list[str]:
    """The first n ids sorted by activity descending, then id ascending."""
    raise NotImplementedError("TODO")


def status_table(df: pd.DataFrame) -> dict[str, dict[str, int]]:
    """pivot_table: index wing, columns status, count of id, fill_value 0.
    Return {wing: {status: count}} with Python ints."""
    raise NotImplementedError("TODO")
