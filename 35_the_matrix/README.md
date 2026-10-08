# 35 // THE MATRIX

```
[CHEESE SHOP] purchase: numpy ── input: coil_telemetry.npy ── 86,400 samples × 512 racks ── float64
```

**Package:** [`numpy`](https://numpy.org/doc/stable/): fast N-dimensional arrays, and the foundation under pandas, matplotlib, scikit-learn and most scientific Python.

Forty-four million numbers: one reading per rack per second for a whole day. In plain Python
lists, looping over them takes minutes. In NumPy it takes milliseconds.

> **WENSLEYDALE:** NumPy stores numbers the way a machine likes them, sir: packed tight, all the
> same type, in one block of memory. And it does arithmetic on the *whole block at once*, in C.
> No Python loop in sight. Everyone who crunches numbers in Python starts here.
>
> **MONTY:** The trick is to stop thinking in loops, and think in whole arrays instead.
> "Subtract the mean from every column" is one line, not a nested loop.

---

## ▓ TECH BRIEFING

### Arrays

```python
import numpy as np
a = np.array([[1.0, 2.0], [3.0, 4.0]])    # from nested lists
a.shape, a.ndim, a.dtype, a.size          # (2, 2), 2, dtype('float64'), 4
np.zeros((3, 4)), np.ones(5), np.full((2, 2), 7), np.eye(3)
np.arange(0, 10, 2)                       # [0 2 4 6 8]
np.linspace(0, 1, 5)                      # [0. 0.25 0.5 0.75 1.]
a.reshape(4, 1), a.T, a.ravel()           # reshaping is (usually) free: it's a view
a.astype(np.int32)
```

### Vectorised maths and axes

```python
a * 2, a + a, a ** 2, np.sqrt(a), np.exp(a)     # element-wise, no loops
a.sum(), a.mean(), a.std(), a.min(), a.max()
a.sum(axis=0)          # down the columns (one result per column)
a.mean(axis=1)         # across the rows (one result per row)
a.argmax(), np.cumsum(a), np.diff(x)
```

### Indexing, slicing, masks

```python
a[0, 1]                # row 0, column 1
a[:, 0]                # the whole first column
a[1:, :]               # slicing gives a VIEW (it shares memory; use .copy() to detach)
mask = a > 2           # a boolean array
a[mask]                # the elements where the mask is True
np.where(a > 2, a, 0)  # choose element-wise
np.flatnonzero(mask), np.argwhere(mask)
a[[0, 1], [1, 0]]      # "fancy" indexing with index arrays
```

### Broadcasting

Arrays with different shapes combine when their trailing dimensions are equal or 1:

```python
cols = np.array([[1, 2, 3], [4, 5, 6]])      # shape (2, 3)
cols - cols.mean(axis=0)                      # (2, 3) - (3,) → per-column centring
pts = np.array([[0, 0], [3, 4]])              # (n, 2)
diff = pts[:, None, :] - pts[None, :, :]      # (n, 1, 2) - (1, n, 2) → (n, n, 2)
np.sqrt((diff ** 2).sum(axis=-1))             # an n×n distance matrix, no loops
```

### Linear algebra, randomness, FFT

```python
A @ B                             # matrix multiply
np.linalg.solve(A, b)             # solve Ax = b
np.linalg.inv(A), np.linalg.det(A), np.linalg.norm(v), np.linalg.eig(A)

rng = np.random.default_rng(42)   # the modern, seedable generator
rng.normal(0, 1, size=1000), rng.integers(0, 6, size=10), rng.choice(arr, 3)

spectrum = np.fft.rfft(signal)                    # frequency content
freqs = np.fft.rfftfreq(len(signal), d=1/rate)
```

### Useful odds and ends

`np.unique(a, return_counts=True)`, `np.bincount(ints, weights=w)`, `np.convolve(x, kernel,
"valid")`, `np.clip(a, lo, hi)`, `np.isclose`/`np.allclose` (float comparisons),
`np.save`/`np.load` (`.npy` files), `np.nan` and `np.nanmean`. Use `np.testing.assert_allclose`
in tests.

---

## ▓ THE JOB

In `job.py`, **with no Python loops over the data** (vectorise!):

1. **`to_array(rows)`**: a `float64` 2-D array.
2. **`standardise(a)`**: z-score each column: subtract the column mean, then divide by the column std.
3. **`hot_racks(temps, limit)`**: the indices where the temperature exceeds the limit.
4. **`rolling_mean(x, w)`**: the moving average over windows of `w` (`"valid"` mode).
5. **`distance_matrix(points)`**: all pairwise Euclidean distances, via broadcasting.
6. **`solve_loads(A, b)`**: solve the linear system.
7. **`clip_count(a, lo, hi)`**: `(clipped_array, how_many_values_were_changed)`.
8. **`noise(seed, n)`**: reproducible standard-normal samples from `default_rng`.
9. **`wing_means(values, wings)`**: the mean value per wing label, via `np.unique` and `np.bincount`.
10. **`dominant_frequency(signal, rate)`**: the strongest frequency, via `np.fft.rfft`, ignoring 0 Hz.
