# 12 // LOADED DICE

```
[PYTHIA-9] location: The Loaded Dice, Kessler Arcade ── table: 7 (dice) ── stake: ¢12,000
```

**Modules:** `math`, `cmath`, `decimal`, `fractions`, `numbers`, `random`, `statistics`

The Loaded Dice is velvet and chrome and cigarette haze, and the dealers wear mirrored
contacts so you can't read their eyes. Table 7 plays **Serpent's Eye**: two dice, bet on the
total. It pays out like it's fair. It isn't.

> **SABLE:** The dice are chipped. There's a microcontroller in each one that shifts the
> weight a little whenever the bet gets large. Nobody can prove it.
>
> **MONTY:** Nobody has tried *statistics*. We watch a few hundred rolls, work out the odds a
> fair die would give, and measure how far off the house is. We'll need exact arithmetic for
> the money, because floats and money do not mix. And a proper random number generator, to
> simulate what "fair" looks like.

---

## ▓ TECH BRIEFING

### `math`

```python
import math
math.pi  math.e  math.tau  math.inf  math.nan
math.sqrt(2)  math.isqrt(17)        # 1.414..., 4 (integer square root)
math.floor(-2.5)  math.ceil(2.1)  math.trunc(-2.7)   # -3, 3, -2
math.log(8, 2)  math.log10(1000)  math.exp(1)
math.sin  math.cos  math.atan2(y, x)  math.degrees  math.radians
math.hypot(3, 4)                    # 5.0
math.dist((0, 0), (3, 4))           # 5.0
math.gcd(12, 18)  math.lcm(4, 6)    # 6, 12
math.comb(52, 5)  math.perm(10, 3)  math.factorial(5)
math.prod([2, 3, 4])  math.fsum([0.1] * 10)   # 24, 1.0 exactly (fsum avoids float drift)
math.isclose(0.1 + 0.2, 0.3)        # True: never use == on floats
math.isnan(x)  math.isinf(x)  math.copysign(1, -0.0)
```

### `cmath`: complex numbers

```python
import cmath
cmath.sqrt(-1)           # 1j
z = 3 + 4j; abs(z)       # 5.0
cmath.phase(z), cmath.polar(z), cmath.rect(r, phi), z.real, z.imag, z.conjugate()
```

### `decimal`: exact base-10 money

```python
from decimal import Decimal, ROUND_HALF_UP, getcontext, localcontext
Decimal("0.1") + Decimal("0.2")         # Decimal('0.3')  exact
Decimal(0.1)                            # Decimal('0.1000000000000000055511...')  ← build from STR
Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)   # Decimal('2.68')
getcontext().prec = 50                   # significant digits for the current thread
with localcontext() as ctx: ctx.prec = 5; ...
```

### `fractions`: exact rationals

```python
from fractions import Fraction
Fraction(6, 36)          # Fraction(1, 6)  always reduced
Fraction(1, 3) + Fraction(1, 6)          # Fraction(1, 2)
Fraction("0.25"), Fraction(0.5), f.numerator, f.denominator
Fraction(math.pi).limit_denominator(1000)   # Fraction(355, 113)
```

### `numbers`: the numeric tower

`numbers.Number` ⊃ `Complex` ⊃ `Real` ⊃ `Rational` ⊃ `Integral`. `int` is Integral,
`Fraction` is Rational, `float` is Real, `complex` is Complex. `Decimal` is registered only as
a `Number`, since it deliberately doesn't mix with floats. Use them in `isinstance` checks.

### `random`: pseudo-random numbers

```python
import random
random.random()              # float in [0.0, 1.0)
random.randint(1, 6)         # 1..6 inclusive
random.randrange(0, 10, 2)   # like range()
random.choice(xs)  random.choices(xs, weights=w, k=10)  random.sample(xs, k=3)
random.shuffle(xs)           # in place
random.uniform(a, b)  random.gauss(mu, sigma)  random.expovariate(lambd)

rng = random.Random(42)      # your OWN generator: reproducible with a seed, isolated state
rng.randint(1, 6)
```

`random` is for simulations and games. It is **predictable**. For tokens, passwords and
keys use `secrets` (ch 19).

### `statistics`

```python
import statistics as st
st.mean(xs)  st.fmean(xs)  st.median(xs)  st.mode(xs)  st.multimode(xs)
st.stdev(xs)  st.pstdev(xs)  st.variance(xs)       # sample vs population
st.quantiles(xs, n=4)                               # quartile cut points
st.correlation(xs, ys)  st.covariance(xs, ys)
slope, intercept = st.linear_regression(xs, ys)
st.NormalDist(mu=0, sigma=1).cdf(1.96)             # ≈ 0.975
```

---

## ▓ THE JOB

In `job.py`:

1. **`split_pot(total, ways)`**: split a `Decimal` amount into `ways` shares, to the cent, and make the shares add up **exactly**.
2. **`compound(principal, rate, years)`**: yearly compound interest in `Decimal`, rounded half-up to cents.
3. **`odds_of_total(target, dice, sides)`**: the exact `Fraction` chance that `dice` fair dice sum to `target`.
4. **`roll_report(rolls)`**: mean, median, modes, and sample stdev with `statistics`.
5. **`z_score(value, data)`**: how many sample standard deviations `value` is from the mean.
6. **`rigged(rolls, sides, tolerance)`**: whether any face's observed frequency is off from fair by more than `tolerance`.
7. **`simulate(seed, n)`**: `n` rolls of two dice with a seeded `random.Random`. Reproducible, and it doesn't touch the global RNG.
8. **`shuffled(deck, seed)`**: a seeded shuffle that leaves the input untouched.
9. **`hand_count(deck_size, hand)`** and **`dist(p, q)`**: `math.comb` and `math.dist`.
10. **`quadratic_roots(a, b, c)`**: both roots via `cmath`, which works even when they're complex.
11. **`kind(x)`**: classify a number with the `numbers` ABCs.
