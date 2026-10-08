# HINTS // 12 LOADED DICE

## split_pot
<details><summary>Hint 1</summary>

`base = (total / ways).quantize(Decimal("0.01"), rounding=ROUND_DOWN)`
</details>
<details><summary>Hint 2</summary>

Leftover cents: `int((total - base * ways) / Decimal("0.01"))`. Then give `base + 0.01` to
the first `leftover` shares.
</details>

## compound
<details><summary>Hint</summary>

`(principal * (1 + rate) ** years).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
`Decimal ** int` stays exact.
</details>

## odds_of_total
<details><summary>Hint</summary>

`itertools.product(range(1, sides + 1), repeat=dice)` lists every possible roll (ch 13 covers
it properly). Count the ones that hit the target and build a `Fraction(hits, total)`.
</details>

## roll_report
<details><summary>Hint</summary>

`statistics.fmean`, `statistics.median`, `sorted(statistics.multimode(...))`, and
`round(statistics.stdev(...), 3)`.
</details>

## rigged
<details><summary>Hint</summary>

`any(abs(rolls.count(f) / len(rolls) - 1 / sides) > tolerance for f in range(1, sides + 1))`
</details>

## simulate / shuffled
<details><summary>Hint</summary>

Make `rng = random.Random(seed)` and only ever call methods on `rng`. For shuffling, copy
first (`list(deck)`), then `rng.shuffle(copy)`, which works in place and returns `None`.
</details>

## quadratic_roots
<details><summary>Hint</summary>

`d = cmath.sqrt(b*b - 4*a*c)`, then `((-b + d) / (2*a), (-b - d) / (2*a))`.
</details>

## kind
<details><summary>Hint</summary>

Check `bool` first (it's a subclass of `int`). Then test `numbers.Integral`, `Rational`,
`Real`, `Complex` in that order.
</details>
