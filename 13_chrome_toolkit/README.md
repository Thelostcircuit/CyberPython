# 13 // CHROME TOOLKIT

```
[PYTHIA-9] input: lachesis_ledger.img ── entries: 2.1M ── format: Iris's own shorthand
```

**Modules:** `itertools`, `functools`, `operator`

Iris's ledger is a record of everything she smuggled out of Ouroboros: shift rotas,
guard pairings, access-card batches, door logs. It's enormous and repetitive, and none of it
is in any order.

> **DEX:** So we loop over it. Loops, right? We're good at loops now.
>
> **MONTY:** We are. But loops within loops within loops get slow to write and hard to read.
> Every runner worth their chrome carries three modules. `itertools` is a whole toolkit of
> lazy iterator building blocks: combinations, grouping, batching, chaining. `functools` is
> for functions that work on functions: caching, partial application, reduction.
> And `operator` gives you every Python operator as a plain function. Together they turn
> twenty lines into two.

---

## ▓ TECH BRIEFING

### `itertools`: lazy building blocks

```python
from itertools import *
count(10, 2)                 # 10 12 14 ...   (infinite)
cycle("AB")                  # A B A B ...    (infinite)
repeat("x", 3)               # x x x
accumulate([1, 2, 3])        # 1 3 6           running totals (or any func: accumulate(xs, max))
chain([1, 2], [3])           # 1 2 3           chain.from_iterable(list_of_lists)
compress("abcd", [1, 0, 1, 0])   # a c
dropwhile(pred, xs)  takewhile(pred, xs)  filterfalse(pred, xs)
islice(xs, 2, 10, 3)         # slicing for ANY iterator
starmap(pow, [(2, 3), (3, 2)])   # 8 9
tee(it, 2)                   # split one iterator into two independent ones
zip_longest("ab", "x", fillvalue="-")   # (a,x) (b,-)
pairwise([1, 2, 3])          # (1,2) (2,3)
batched(range(5), 2)         # (0,1) (2,3) (4,)
groupby("aaabcc")            # ('a', <group>), ('b', ...), ('c', ...)  groups CONSECUTIVE keys
                             # so sort by the key first if you want all of each group together
product("ab", repeat=2)      # aa ab ba bb     the cartesian product
permutations("abc", 2)       # ab ac ba bc ca cb
combinations("abc", 2)       # ab ac bc
combinations_with_replacement("ab", 2)   # aa ab bb
```

### `functools`

```python
from functools import cache, lru_cache, partial, reduce, wraps, singledispatch, \
    total_ordering, cached_property, cmp_to_key

@cache                       # memoise: unbounded cache keyed by arguments
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=256)      # bounded;  fib.cache_info(), fib.cache_clear()

reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1)   # 24: fold a sequence into one value

int_from_hex = partial(int, base=16)              # pre-fill some arguments
int_from_hex("ff")                                # 255

@singledispatch               # choose an implementation by the type of the first argument
def describe(x): return "thing"
@describe.register
def _(x: int): return "int"

@total_ordering               # write __eq__ and __lt__; get <=, >, >= free
class Rank: ...

class Dossier:
    @cached_property          # computed on first access, then stored on the instance
    def summary(self): ...

sorted(xs, key=cmp_to_key(old_style_cmp))         # adapt a cmp(a, b) -> -1/0/1 function
```

### `operator`: operators as functions

```python
import operator as op
op.add(2, 3)  op.mul  op.neg  op.not_  op.contains  op.getitem  op.eq  op.lt
op.itemgetter("rank", "name")(row)     # (row["rank"], row["name"])
op.attrgetter("slot")(implant)         # implant.slot  (dotted paths too: "owner.name")
op.methodcaller("upper")("iris")       # 'IRIS'
sorted(rows, key=op.itemgetter("rank", "name"))
reduce(op.mul, xs, 1)
```

These are faster and more readable than the equivalent lambdas.

---

## ▓ THE JOB

In `job.py`:

1. **`guard_pairs(guards)`**: every unordered pair (`combinations`).
2. **`routes(stops)`**: every order to visit them in (`permutations`).
3. **`codes(digits, length)`**: every code of that length (`product`).
4. **`running_totals(xs)`**: `accumulate`.
5. **`rle(text)`**: run-length encode with `groupby`: `"aaab"` → `[("a", 3), ("b", 1)]`.
6. **`card_batches(ids, n)`**: `batched`.
7. **`deltas(xs)`**: differences between neighbours (`pairwise`).
8. **`until_alarm(events)`**: the events before the first `"ALARM"` (`takewhile`).
9. **`assign_shifts(tasks, crew)`**: round-robin tasks onto the crew (`cycle`).
10. **`ways_to_climb(n)`**: memoised recursion with `@cache`.
11. **`product_of(xs)`**: `reduce` + `operator.mul`.
12. **`hex_reader`**: a `partial` of `int`.
13. **`describe`**: a `singledispatch` function.
14. **`Clearance`**: a `total_ordering` class.
15. **`Dossier.summary`**: a `cached_property` that is only computed once.
16. **`sort_roster(rows)`**: `itemgetter` with two keys.
