# HINTS // 35 THE MATRIX

## standardise
<details><summary>Hint</summary>

`(a - a.mean(axis=0)) / a.std(axis=0)`. Broadcasting stretches the per-column results over the
rows.
</details>

## hot_racks
<details><summary>Hint</summary>

`np.flatnonzero(temps > limit)`
</details>

## rolling_mean
<details><summary>Hint</summary>

Convolving with a flat kernel is a moving average: `np.convolve(x, np.ones(w) / w, "valid")`.
(Or use `np.cumsum` differences.)
</details>

## distance_matrix
<details><summary>Hint</summary>

`diff = points[:, None, :] - points[None, :, :]` gives shape `(n, n, d)`. Square it, sum over
the last axis, and take `np.sqrt`.
</details>

## clip_count
<details><summary>Hint</summary>

Count with a combined mask, `((a < lo) | (a > hi)).sum()`, and wrap it in `int()` so you
return a Python int rather than a NumPy one.
</details>

## wing_means
<details><summary>Hint</summary>

`labels, inverse = np.unique(wings, return_inverse=True)`. `inverse[i]` is the group number
of item i. `np.bincount(inverse, weights=values)` sums per group, and `np.bincount(inverse)`
counts. Divide.
</details>

## dominant_frequency
<details><summary>Hint</summary>

Take the magnitude `np.abs(np.fft.rfft(signal))` and the frequencies
`np.fft.rfftfreq(len(signal), d=1/rate)`. Skip index 0 (the DC offset, which is the average)
and take `argmax`.
</details>
