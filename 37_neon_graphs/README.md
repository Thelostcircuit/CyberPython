# 37 // NEON GRAPHS

```
[CHEESE SHOP] purchase: matplotlib ── audience: R. Okonkwo, night shift ── time to convince her: ~2 seconds
```

**Package:** [`matplotlib`](https://matplotlib.org/stable/): plots, charts and figures, for the screen or for files.

You get one chance to show R. Okonkwo what's happening in wing C: a single image, slipped into
her shift report where she'll see it and her supervisor won't. It has to make the case at a
glance: who's in there, how long they've been held, and the 3.2 Hz pulse that shouldn't exist.

> **WENSLEYDALE:** Matplotlib, sir. Draws anything: lines, bars, scatters, histograms, heatmaps,
> whole dashboards of little panels. pandas uses it under the hood for `.plot()`. It's not the
> newest thing on my shelves, but it's what everything else is measured against.
>
> **MONTY:** One tip: use the **object-oriented** API. Make a figure and axes explicitly, and
> call methods on *them*. The `plt.plot()` shortcut style gets confusing the moment you have
> more than one chart.

---

## ▓ TECH BRIEFING

### Figures and Axes

```python
import matplotlib
matplotlib.use("Agg")                 # a non-GUI backend: draw to files (servers, tests)
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))            # a Figure holding one Axes (one plot area)
ax.plot(t, pulse, label="wing C", color="#ff00ff", linewidth=2)
ax.set_title("Wing C activity"); ax.set_xlabel("t (s)"); ax.set_ylabel("activity")
ax.legend(); ax.grid(True, alpha=0.3)
fig.savefig("wingC.png", dpi=150, bbox_inches="tight")
plt.close(fig)                                    # free it (important in loops and tests)
```

`fig, axes = plt.subplots(3, 1, sharex=True)` gives a grid, and `axes` is a NumPy array of
Axes. `fig.tight_layout()` stops labels overlapping. `fig.suptitle(...)` titles the whole
figure.

### The chart types you'll use most

```python
ax.plot(x, y)                         # lines
ax.bar(names, heights)                # bars (ax.barh for horizontal)
ax.scatter(x, y, c=colours, s=sizes)  # points
counts, edges, patches = ax.hist(values, bins=20)
im = ax.imshow(matrix, cmap="magma"); fig.colorbar(im, ax=ax)     # heatmaps
ax.fill_between(x, lo, hi, alpha=0.2), ax.axhline(y=70, linestyle="--"), ax.errorbar(...)
ax.annotate("peak", xy=(x0, y0), xytext=(x0 + 1, y0 + 1), arrowprops={"arrowstyle": "->"})
```

### Reading a figure back (how the tests check your work)

```python
ax.get_title(), ax.get_xlabel(), ax.lines[0].get_ydata(), ax.patches[0].get_height()
[t.get_text() for t in ax.get_legend().get_texts()]
ax.collections[0].get_offsets()       # scatter points
ax.texts                              # annotations
```

Styles: `plt.style.use("dark_background")` suits a cyberpunk dashboard. `plt.style.available`
lists the rest. `ax.set_xscale("log")`, `ax.set_xlim(...)`, twin axes with `ax.twinx()`.

---

## ▓ THE JOB

The Agg backend is already selected at the top of `job.py`. Every function returns the
`Figure` (and the tests close it). Using matplotlib's OO API:

1. **`pulse_chart(t, values, title)`**: one line, with the title and axis labels `"t (s)"` / `"activity"`.
2. **`wing_bars(counts)`**: a bar chart of `{wing: count}`, in the order given.
3. **`hot_scatter(x, y, limit)`**: two scatter series, `"normal"` and `"hot"` (y > limit), plus a legend.
4. **`panels(series)`**: one panel per series, stacked vertically with a shared x-axis, each titled by its key.
5. **`activity_hist(values, bins)`**: `(fig, counts as a list of ints)`.
6. **`annotate_peak(x, y)`**: a line chart with a `"peak"` annotation at the maximum.
7. **`rack_heatmap(matrix)`**: `imshow` plus a colourbar.
8. **`save_png(fig, path, dpi)`**: save it, and return the image size in pixels as `(width, height)`.
