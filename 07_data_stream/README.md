# 07 // DATA STREAM

```
[PYTHIA-9] location: pump station 6, under the Pit ── tap: Ouroboros backbone, fibre 3 ── 40 Tb/s
```

Pump station 6 is where an Ouroboros backbone fibre runs past the city's drainage system.
Sable knows the maintenance hatch code. Dex knows how to splice fibre without the sheath
alarm tripping. You know how to be quiet.

What you don't have is somewhere to put forty terabits a second.

> **DEX:** We could, uh, buy more storage?
>
> **MONTY:** We could buy all the storage in Coilhaven and it'd be full in an afternoon. No.
> We don't *store* the stream, we **iterate** over it. We take one item, look at it, decide,
> and let it go. Python's whole looping machinery is built on that idea, and **generators**
> let us write streams that compute each value only when somebody asks for it. Lazy. Like
> Dex, but useful.
>
> **DEX:** Hey.

---

## ▓ TECH BRIEFING

### Iterables vs iterators

- An **iterable** is anything you can loop over. It has `__iter__()`, which returns an iterator.
- An **iterator** produces values one at a time with `__next__()`, and raises `StopIteration`
  when it's done. Iterators are also iterables (their `__iter__` returns `self`).

```python
it = iter([10, 20])      # calls list.__iter__()
next(it)                 # 10
next(it)                 # 20
next(it)                 # StopIteration
next(it, "done")         # 'done'   default instead of raising
```

A `for` loop is just `iter()` once, then `next()` until `StopIteration`. A list can be looped
over many times, but an **iterator is used up after one pass**.

### Writing an iterator class

```python
class Countdown:
    def __init__(self, start):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1
```

### Generators: the easy way

Any function containing `yield` is a **generator function**. Calling it runs no code at all:
it returns a generator object. Each `next()` runs the body up to the next `yield`, then
pauses there with all its local variables intact.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
    # falling off the end raises StopIteration for you

g = countdown(3)       # nothing has run yet
list(g)                # [3, 2, 1]
list(g)                # []   exhausted
```

Generators can be infinite (`while True: yield ...`). That's fine, as long as the consumer
stops asking.

### yield from

Delegate to another iterable (or generator), including recursively:

```python
def walk(tree):
    for node in tree:
        if isinstance(node, list):
            yield from walk(node)
        else:
            yield node
```

### Generator expressions

Like a list comprehension, but with parentheses and lazy:

```python
squares = (x * x for x in range(10**12))   # instant: nothing computed yet
sum(x for x in data if x > 0)              # inside a call, one pair of parens is enough
```

Chain them into pipelines. Each stage pulls one item at a time from the stage before, so the
whole stream is never in memory:

```python
lines   = (l.strip() for l in source)
frames  = (l for l in lines if l and not l.startswith("#"))
lengths = (len(f) for f in frames)
```

### Re-iterable objects

If `__iter__` is itself a generator function, every `for` loop gets a *fresh* generator:

```python
class Tap:
    def __init__(self, data): self.data = data
    def __iter__(self):
        for x in self.data:
            yield x
```

### send(), close(), and generators as coroutines

`yield` is also an *expression*. `value = yield out` pauses, hands `out` to the caller, and
later receives whatever the caller passes to `.send(value)`:

```python
def averager():
    total = count = 0
    avg = None
    while True:
        x = yield avg          # hand out the average, wait for the next number
        total += x; count += 1
        avg = total / count

a = averager()
next(a)          # "prime" it: run to the first yield
a.send(10)       # 10.0
a.send(20)       # 15.0
a.close()        # raises GeneratorExit inside it
```

A generator's `return value` becomes `StopIteration.value`, which is also the result of a
`yield from` expression. `asyncio` (ch 24) grew out of exactly this machinery.

### Built-ins that work lazily

`range`, `zip`, `map`, `filter`, `enumerate`, `reversed`, and `iter(callable, sentinel)` all
give you lazy iterators. `itertools` (ch 13) has many more.

---

## ▓ THE JOB

In `job.py`:

1. **`Countdown`**: an iterator class (`__iter__` + `__next__`) that counts down to 1.
2. **`frames(lines)`**: a generator that yields stripped lines, skipping blanks and `#` comments. It must be lazy.
3. **`chunked(iterable, size)`**: yield lists of `size` items, with the last one possibly shorter.
4. **`flatten(nested)`**: yield the leaves of arbitrarily nested lists and tuples, using `yield from`.
5. **`take(n, iterable)`**: the first `n` items as a list. It has to work on infinite generators.
6. **`windows(iterable, n)`**: sliding windows as tuples: `(1,2,3), (2,3,4), ...`.
7. **`interleave(*iterables)`**: round-robin between the iterables until they're all exhausted.
8. **`Tap`**: a re-iterable wrapper that also counts how many times it's been iterated.
9. **`running_max()`**: a `send()`-driven generator that yields the largest value seen so far.
