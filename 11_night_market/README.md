# 11 // NIGHT MARKET

```
[PYTHIA-9] location: Undercroft Night Market, Tier 1 ── stalls: 600+ ── crowd density: CRUSH
```

**Modules:** `collections`, `collections.abc`, `heapq`, `bisect`, `array`, `graphlib`, `enum`, `copy`, `weakref`, `types`

The night market fills a flooded parking structure under Tier 1. Stalls are lashed to
pillars, and boats nose between them. Everything is for sale: chrome, noodles, stolen
identities, stolen umbrellas. Mother Adder runs a dozen stalls here under a dozen names, and
she wants MONTY to take over her books tonight, because it's payday for the crew.

> **MOTHER ADDER:** Sales ledger, stall assignments, price bands, a queue of deliveries, a
> list of which jobs need which other jobs done first. My last bookkeeper used spreadsheets.
> My last bookkeeper is now a fisherman.
>
> **MONTY:** Lists and dicts will do *anything*, but the library has containers that do
> specific things *well*: counting, queuing, priority, sorted insertion, dependency order,
> named constants. Knowing which one to reach for is half of being good at this.

---

## ▓ TECH BRIEFING

### `collections`

```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict, ChainMap

Counter("abracadabra").most_common(2)   # [('a', 5), ('b', 2)]
c = Counter(apples=3); c["pears"] += 2    # missing keys count as 0
c1 + c2, c1 - c2, c1 & c2, c.total()

groups = defaultdict(list)              # missing key → calls list() to make a default
groups["stall-9"].append("noodles")

q = deque(maxlen=3)                     # fast appends/pops at BOTH ends; maxlen drops the oldest
q.append(1); q.appendleft(0); q.pop(); q.popleft(); q.rotate(1)

Item = namedtuple("Item", ["name", "price", "qty"], defaults=[1])
i = Item("chip", 40)                     # Item(name='chip', price=40, qty=1)
i.price, i._replace(qty=5), i._asdict()  # still a tuple: unpacks, indexes, hashes

od = OrderedDict(); od.move_to_end("k"); od.popitem(last=False)   # reorderable dict
ChainMap(cli, env, defaults)["port"]    # looks through several dicts, first hit wins
```

`UserDict`, `UserList` and `UserString` are easy-to-subclass wrappers.

### `collections.abc`

Abstract base classes that describe *what a container can do*:

```python
from collections.abc import Mapping, Sequence, Set, Iterable, Callable, MutableMapping
isinstance({}, Mapping)        # True
isinstance("ab", Sequence)     # True
isinstance({1}, Set)           # True
```

Subclass one and it fills in the rest: implement `__getitem__`, `__setitem__`,
`__delitem__`, `__iter__` and `__len__` on a `MutableMapping`, and you get `get`, `pop`,
`update`, `items`, `==`... for free.

### `heapq`: a priority queue on a plain list

```python
import heapq
h = []
heapq.heappush(h, (2, "courier")); heapq.heappush(h, (1, "drone"))
heapq.heappop(h)                        # (1, 'drone')   smallest first
heapq.heapify(xs)                       # turn a list into a heap in place, O(n)
heapq.nsmallest(3, offers, key=lambda o: o.price)
heapq.merge(sorted_a, sorted_b)         # lazily merge already-sorted inputs
```

### `bisect`: binary search on sorted lists

```python
import bisect
bisect.bisect_right([10, 20, 30], 25)   # 2   the insertion point
bisect.insort(prices, 17)                # insert and keep the list sorted
bisect.bisect_left(xs, x, key=...)
```

### `array`: compact typed arrays

```python
from array import array
a = array("h", [1, -2, 300])            # signed 16-bit ints; 'b','i','l','q','f','d'...
a.tobytes()   array("h").frombytes(data)   a.itemsize   a.byteswap()
```

### `graphlib`: dependency order

```python
from graphlib import TopologicalSorter, CycleError
ts = TopologicalSorter({"heist": {"recon", "gear"}, "gear": {"cash"}})
list(ts.static_order())    # ['recon', 'cash', 'gear', 'heist'] (one valid order)
```

A cycle raises `CycleError`.

### `enum`

```python
from enum import Enum, IntEnum, Flag, StrEnum, auto
class Level(Enum):
    LOW = 1
    HIGH = 2
Level.HIGH.name, Level.HIGH.value, Level(2), Level["LOW"], list(Level)

class Access(Flag):
    READ = auto(); WRITE = auto(); EXEC = auto()
    ALL = READ | WRITE | EXEC
Access.READ | Access.WRITE       # combined flags;  `in` tests membership
```

`IntEnum` and `StrEnum` members compare equal to plain ints or strs. `@enum.unique`
forbids duplicate values.

### `copy`

```python
import copy
copy.copy(x)        # shallow: new outer object, same inner objects
copy.deepcopy(x)    # recursive: completely independent
copy.replace(obj, field=value)   # 3.13+: works on namedtuples, dataclasses...
```

### `weakref`

A weak reference doesn't keep its object alive. Use one for caches and registries that
shouldn't leak memory:

```python
import weakref
cache = weakref.WeakValueDictionary()   # entries vanish when the object is garbage collected
r = weakref.ref(obj); r()               # the object, or None once it's gone
weakref.finalize(obj, callback)         # run something when obj is collected
```

### `types`

```python
import types
types.SimpleNamespace(a=1, b=2)          # a quick attribute bag with a nice repr
types.MappingProxyType(d)                # a read-only VIEW of a dict
types.FunctionType, types.GeneratorType, types.ModuleType, types.MethodType
types.new_class(...)                     # build classes dynamically
```

---

## ▓ THE JOB

In `job.py`:

1. **`best_sellers(sales, n)`**: `Counter`.
2. **`by_stall(pairs)`**: `defaultdict`.
3. **`Item`**: a `namedtuple` with a default `qty`.
4. **`last_n(events, n)`**: `deque(maxlen=...)`.
5. **`LRU`**: a least-recently-used cache on `OrderedDict`.
6. **`resolve_settings(defaults, env, cli)`**: `ChainMap` priority.
7. **`container_kind(x)`**: `collections.abc` checks.
8. **`cheapest(offers, k)`** and **`merge_feeds(*feeds)`**: `heapq`.
9. **`price_band(price)`**: `bisect`.
10. **`pack` / `unpack`**: `array` to and from bytes.
11. **`job_order(deps)`**: `graphlib`, returning `None` on a cycle.
12. **`Access`** and **`can(granted, needed)`**: a `Flag` enum.
13. **`clone_loadout(loadout)`**: `deepcopy`.
14. **`Registry`**: `weakref.WeakValueDictionary`.
15. **`frozen_view(d)`**: `types.MappingProxyType`.
