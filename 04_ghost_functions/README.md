# 04 // GHOST FUNCTIONS

```
[PYTHIA-9] location: freight elevator 9, going up ── crew: 2 ── job: courier locker, Tier 12
```

Dex is fifteen, maybe sixteen, with a shaved head and a jacket held together by optimism
and cable ties. He talks like he's being charged by the second.

> **DEX:** So there's a courier, right? Ouroboros courier, drops sealed cases at a locker bank
> on Tier 12 every night at ten. The lockers rotate their codes. Every locker, every night, a
> different algorithm. Last runner tried to hand-crack them and got caught on locker two.
>
> What we need is a *kit*. Something that takes any locker and just, like, *does* the thing.
>
> **MONTY:** He's describing functions, bless him. Write a thing once, give it a name, use it
> everywhere. Functions that take functions. Functions that *make* functions. Functions that
> wrap other functions like a coat. Once you've got those, you stop cracking locks one by
> one and start building crackers.

---

## ▓ TECH BRIEFING

### Defining and calling

```python
def crack(code: str, attempts: int = 3) -> bool:
    """Docstring: the first string in a function. help(crack) shows it."""
    return code == "0000"

crack("1234")                 # positional
crack("1234", attempts=5)     # keyword
crack(attempts=5, code="1")   # keywords in any order
```

A function without `return` returns `None`. Return several values as a tuple:
`return x, y`.

### Parameter kinds

```python
def f(a, b=2, *args, c, d=4, **kwargs): ...
#     ^  ^     ^      ^  ^      ^
#     |  |     |      keyword-only (after *)
#     |  |     extra positionals → tuple
#     |  default                    extra keywords → dict

def g(x, y, /, z):     # x and y are POSITIONAL-ONLY (before /)
def h(*, key):         # a bare * means "everything after is keyword-only"
```

Unpacking at the call site:

```python
args = [1, 2]; opts = {"c": 3}
f(*args, **opts)      # same as f(1, 2, c=3)
```

### The mutable default trap

Defaults are evaluated **once**, when the `def` runs, and not on every call:

```python
def add(item, bag=[]):      # BUG: every call shares the same list
    bag.append(item)
    return bag

def add(item, bag=None):    # the fix
    if bag is None:
        bag = []
    bag.append(item)
    return bag
```

### Functions are values

```python
tools = [str.upper, str.lower, len]
tools[2]("abc")                    # 3
sorted(names, key=len)             # pass a function as an argument
square = lambda x: x * x           # an anonymous one-expression function
```

`map(f, xs)` and `filter(pred, xs)` exist, but a comprehension is usually clearer.

### Scope: LEGB

Names are looked up **L**ocal → **E**nclosing function → **G**lobal (module) →
**B**uilt-in. Assigning to a name makes it local, unless you declare otherwise:

```python
count = 0
def bump():
    global count      # rebind the module-level name (use sparingly)
    count += 1

def outer():
    n = 0
    def inner():
        nonlocal n    # rebind the ENCLOSING function's name
        n += 1
        return n
    return inner
```

### Closures

An inner function remembers the variables of the function that created it, even after the
outer function has returned:

```python
def make_key(prefix):
    def key(n):
        return f"{prefix}-{n}"
    return key

ouro = make_key("OS")
ouro(7)    # 'OS-7'
```

### Decorators

A decorator is a function that takes a function and returns a replacement. `@deco` above a
`def` is shorthand for `f = deco(f)`:

```python
import functools

def shout(func):
    @functools.wraps(func)            # copy __name__, __doc__ etc. onto the wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    return f"hi {name}"

greet("dex")   # 'HI DEX'
```

A decorator **with arguments** is a function that *returns* a decorator:

```python
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(n)]
        return wrapper
    return decorator

@repeat(3)
def ping(): return "ping"
```

Functions are objects. You can attach attributes to them (`wrapper.calls = []`).

### Recursion

A function can call itself. It needs a base case. Python's default recursion limit is about
1000 frames (`sys.getrecursionlimit()`).

```python
def total(nested):
    return sum(total(x) if isinstance(x, list) else x for x in nested)
```

---

## ▓ THE JOB

In `job.py`:

1. **`total_loot(*amounts, cut=0.0)`**: sum any number of amounts, take the crew's `cut` off (a fraction), round to 2 places.
2. **`make_payload(target, *, retries=3, stealth=False)`**: return a dict. `retries` and `stealth` must be keyword-only.
3. **`build_request(method, /, **headers)`**: `method` positional-only. Build `"GET host=x;port=9"` with the headers sorted by name.
4. **`tag_target(name, tags=None)`**: fix the mutable-default trap. Return a *new* list of tags plus the name.
5. **`make_counter(start=0)`**: return a function that returns `start+1`, `start+2`, ... on each call (closure + `nonlocal`).
6. **`pipeline(*funcs)`**: return a function that applies `funcs` left to right.
7. **`log_calls`**: a decorator that records each call's `(args, kwargs)` in `wrapper.calls`, and keeps the original `__name__` and `__doc__`.
8. **`retry(times)`**: a decorator *factory*. Call the function, and if it raises, try again, up to `times` attempts in total. Then re-raise the last error.
9. **`depth(nested)`**: the maximum nesting depth of a list of lists, using recursion.
