# HINTS // 37 NEON GRAPHS

## pulse_chart
<details><summary>Hint</summary>

`fig, ax = plt.subplots()`, `ax.plot(t, values)`, `ax.set_title(...)`, `ax.set_xlabel(...)`,
`ax.set_ylabel(...)`, `return fig`.
</details>

## wing_bars
<details><summary>Hint</summary>

`ax.bar(list(counts), list(counts.values()))`. String x values become categories, in the
order you give them.
</details>

## hot_scatter
<details><summary>Hint</summary>

Turn the inputs into arrays, make a mask `hot = y > limit`, and scatter `x[~hot], y[~hot]`
first, then `x[hot], y[hot]`. Give each a `label=`, then call `ax.legend()`.
</details>

## panels
<details><summary>Hint</summary>

`squeeze=False` makes `axes` a 2-D array even with one row, so `axes[:, 0]` always works.
`zip` it with `series.items()`.
</details>

## activity_hist
<details><summary>Hint</summary>

`counts, edges, patches = ax.hist(values, bins=bins)`. The counts are floats, so convert them
with `int()`.
</details>

## annotate_peak / rack_heatmap
<details><summary>Hint</summary>

`i = y.argmax()`, then `ax.annotate("peak", xy=(x[i], y[i]), ...)`. For the heatmap:
`im = ax.imshow(matrix, cmap="magma")`, then `fig.colorbar(im, ax=ax)`, which adds a second
Axes.
</details>

## save_png
<details><summary>Hint</summary>

`fig.savefig(path, dpi=dpi)`. `mpimg.imread(path).shape` is `(height, width, channels)`.
Watch the order!
</details>
