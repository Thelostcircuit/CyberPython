"""12 // LOADED DICE: prove the house cheats (and keep our money exact)."""

import cmath
import itertools
import math
import numbers
import random
import statistics
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from fractions import Fraction
from typing import Any

CENT = Decimal("0.01")


def split_pot(total: Decimal, ways: int) -> list[Decimal]:
    """Split into `ways` shares of whole cents. Every share is total/ways rounded DOWN to the
    cent; then the leftover cents are handed out one each to the first shares.
    The shares must sum exactly to total (total always has at most 2 decimal places).

    split_pot(Decimal("100.00"), 3) -> [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")]
    """
    raise NotImplementedError("TODO")


def compound(principal: Decimal, rate: Decimal, years: int) -> Decimal:
    """principal * (1 + rate) ** years, rounded ROUND_HALF_UP to cents at the END only."""
    raise NotImplementedError("TODO")


def odds_of_total(target: int, dice: int = 2, sides: int = 6) -> Fraction:
    """Exact probability that `dice` fair dice with faces 1..sides sum to target."""
    raise NotImplementedError("TODO")


def roll_report(rolls: list[int]) -> dict[str, Any]:
    """{"mean": float, "median": number, "modes": sorted list, "stdev": sample stdev rounded
    to 3 places}. Use the statistics module."""
    raise NotImplementedError("TODO")


def z_score(value: float, data: list[float]) -> float:
    """(value - mean) / sample stdev, rounded to 2 places."""
    raise NotImplementedError("TODO")


def rigged(rolls: list[int], sides: int, tolerance: float) -> bool:
    """For each face 1..sides, compare its observed frequency (count / len(rolls)) with the
    fair 1/sides. True if ANY face is off by MORE than tolerance."""
    raise NotImplementedError("TODO")


def simulate(seed: int, n: int) -> list[int]:
    """n totals of two six-sided dice, using random.Random(seed): for each roll call
    rng.randint(1, 6) twice and add. Must not use or disturb the global random state."""
    raise NotImplementedError("TODO")


def shuffled(deck: list[Any], seed: int) -> list[Any]:
    """A shuffled COPY using random.Random(seed).shuffle. The input list is unchanged."""
    raise NotImplementedError("TODO")


def hand_count(deck_size: int, hand: int) -> int:
    """How many different hands of `hand` cards from `deck_size` (order doesn't matter)."""
    raise NotImplementedError("TODO")


def dist(p: tuple[float, ...], q: tuple[float, ...]) -> float:
    """Euclidean distance between two points (math.dist)."""
    raise NotImplementedError("TODO")


def quadratic_roots(a: float, b: float, c: float) -> tuple[complex, complex]:
    """Both roots of ax² + bx + c = 0 via cmath.sqrt, (-b + d) / 2a first, then (-b - d) / 2a."""
    raise NotImplementedError("TODO")


def kind(x: Any) -> str:
    """"integral", "rational", "real", "complex" (most specific first, via numbers ABCs),
    else "not a number". bool counts as "not a number" here."""
    raise NotImplementedError("TODO")
