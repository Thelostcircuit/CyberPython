"""37 // NEON GRAPHS: one picture for R. Okonkwo."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402


def pulse_chart(t, values, title: str) -> Figure:
    """One Axes; ax.plot(t, values); title; xlabel "t (s)"; ylabel "activity"."""
    raise NotImplementedError("TODO")


def wing_bars(counts: dict[str, int]) -> Figure:
    """ax.bar with the wings as the x categories (in dict order) and the counts as heights."""
    raise NotImplementedError("TODO")


def hot_scatter(x, y, limit: float) -> Figure:
    """Two ax.scatter calls: first the points with y <= limit (label "normal"), then y > limit
    (label "hot"); then ax.legend()."""
    raise NotImplementedError("TODO")


def panels(series: dict[str, list[float]]) -> Figure:
    """plt.subplots(len(series), 1, sharex=True, squeeze=False); in panel i plot the i-th series
    and set its title to the i-th key."""
    raise NotImplementedError("TODO")


def activity_hist(values, bins: int) -> tuple[Figure, list[int]]:
    """ax.hist(values, bins=bins); return (fig, the counts as a list of Python ints)."""
    raise NotImplementedError("TODO")


def annotate_peak(x, y) -> Figure:
    """Plot y against x, and ax.annotate("peak", xy=(x at max y, max y))."""
    raise NotImplementedError("TODO")


def rack_heatmap(matrix) -> Figure:
    """ax.imshow(matrix, cmap="magma") plus fig.colorbar(image, ax=ax)."""
    raise NotImplementedError("TODO")


def save_png(fig: Figure, path, dpi: int) -> tuple[int, int]:
    """fig.savefig(path, dpi=dpi); read it back with matplotlib.image.imread and return
    (width, height) in pixels."""
    raise NotImplementedError("TODO")
