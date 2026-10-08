# 03 // DATA SHARDS

```
[PYTHIA-9] location: THE ADDER'S NEST, back room ── shards loaded: 412 ── order: NONE
```

Mother Adder tips a biscuit tin onto the table. Hundreds of glass data shards spill across
the formica, each one the size of a fingernail and faintly glowing. Iris smashed her own
data core rather than let Ouroboros have it.

> **MOTHER ADDER:** Each shard has a sequence number burned into it, and a checksum. Some are
> duplicates, since she made copies. Some are corrupted. Some belong to other people's files
> she was carrying. I never could make sense of them.
>
> **MONTY:** That's because you were using *fingers*. What you need are **data structures**.
> Python has four built in, and they'll do almost everything you ever need: the **list**, the
> **tuple**, the **dict**, and the **set**. Let's plug the shard reader in.

---

## ▓ TECH BRIEFING

### list: ordered, mutable

```python
shards = [4, 1, 3]
shards.append(9)          # [4, 1, 3, 9]
shards.extend([7, 7])     # [4, 1, 3, 9, 7, 7]
shards.insert(0, 100)     # put 100 at index 0
shards.pop()              # remove and return the last item (or .pop(i))
shards.remove(7)          # remove the first 7 (ValueError if absent)
shards.sort()             # in place, returns None!
sorted(shards)            # returns a NEW sorted list
shards.reverse()          # in place;  reversed(shards) is an iterator
shards.index(3)  shards.count(7)  len(shards)  9 in shards
del shards[0]
shards.clear()
```

### Slicing works on all sequences

```python
xs = [0, 1, 2, 3, 4, 5]
xs[1:4]    # [1, 2, 3]
xs[:2]     # [0, 1]        first two
xs[-2:]    # [4, 5]        last two
xs[::2]    # [0, 2, 4]     every other
xs[::-1]   # reversed copy
xs[:]      # shallow copy
xs[1:3] = ["a", "b", "c"]   # slice assignment can even change the length
```

### tuple: ordered, immutable

```python
point = (3, 4)
single = (5,)            # the COMMA makes a tuple, not the parentheses
x, y = point             # unpacking
a, b = b, a              # swap, no temp variable
head, *middle, tail = [1, 2, 3, 4]    # head=1, middle=[2, 3], tail=4
```

Use tuples for fixed-shape records ("a point is two numbers") and lists for "a bunch of
the same kind of thing". Tuples of hashable things are hashable, so they can be dict keys.

### dict: key → value, insertion-ordered

```python
owner = {"id": "IV-7", "level": 3}
owner["id"]                     # 'IV-7'   KeyError if missing
owner.get("rank")               # None     no error
owner.get("rank", 0)            # 0        default
owner["rank"] = 5               # add or overwrite
"id" in owner                   # True     checks KEYS
del owner["rank"]
owner.pop("level", None)        # remove and return, with a default
owner.setdefault("tags", []).append("x")    # get, or insert the default and get it
owner.update({"a": 1}, b=2)
owner | {"c": 3}                # merged copy (3.9+);  owner |= {...} updates in place
for key, value in owner.items(): ...
list(owner.keys())   list(owner.values())
dict.fromkeys(["a", "b"], 0)    # {'a': 0, 'b': 0}
dict(zip(keys, values))
```

Keys must be **hashable**: str, int, float, tuple of hashables, frozenset. Lists can't be
keys because they can change.

### set and frozenset: unique, unordered

```python
seen = {"a", "b"}          # NOTE: {} is an empty DICT, use set() for an empty set
seen.add("c")   seen.discard("z")   seen.remove("a")   # remove raises if absent
a | b    a & b    a - b    a ^ b      # union, intersection, difference, symmetric diff
a <= b                               # subset
a.isdisjoint(b)
frozenset({"x", "y"})                # immutable, hashable: can go in sets or be a dict key
```

Membership (`in`) on sets and dicts is O(1). On lists it's O(n).

### Comprehensions

```python
[x * 2 for x in xs]                       # list
[x for x in xs if x % 2 == 0]             # with filter
[(x, y) for x in "ab" for y in range(2)]  # nested loops, left to right
{name: len(name) for name in names}       # dict
{c.lower() for c in "HeLLo"}              # set
```

### Sorting with keys

```python
sorted(words, key=len)                         # by length
sorted(words, key=str.lower)                   # case-insensitive
sorted(people, key=lambda p: p["age"], reverse=True)
sorted(items, key=lambda t: (-t[1], t[0]))     # score DESC, then name ASC
```

Python's sort is **stable**: equal items keep their original order.

### Built-ins that eat whole collections

`len`, `sum`, `min`, `max` (take `key=` and `default=`), `any`, `all`, `sorted`, `reversed`,
`enumerate`, `zip` (use `strict=True` to demand equal lengths), `list()`, `tuple()`, `set()`,
`dict()`.

```python
max(scores, key=scores.get)   # the key with the biggest value
list(zip(*[[1, 2], [3, 4]]))  # [(1, 3), (2, 4)]   transpose
```

### Copies vs references

`b = a` does not copy. Both names point at the same list. `a.copy()`, `list(a)` and `a[:]`
make shallow copies (see `copy.deepcopy` in ch 11).

---

## ▓ THE JOB

A shard is a tuple `(seq, owner, text, checksum)`. In `job.py`:

1. **`checksum(text)`**: the sum of the character codes (`ord`) modulo 256.
2. **`valid_shards(shards)`**: only shards whose checksum matches their text (a list comprehension).
3. **`reassemble(shards, owner)`**: that owner's valid shards, **sorted by seq**, texts joined, duplicates of the same seq used once.
4. **`owners(shards)`**: the sorted list of distinct owners.
5. **`index_by_owner(shards)`**: a dict of owner → sorted list of seqs (no duplicates).
6. **`split_packet(packet)`**: star-unpack a packet into `(header, body_list, footer)`.
7. **`shared_contacts(*contact_lists)`**: the names in **every** list, sorted.
8. **`leaderboard(scores, n)`**: the top `n` names by score (desc), ties broken alphabetically.
9. **`invert(mapping)`**: swap keys and values with a dict comprehension. If values repeat, collect the keys into a sorted list.
10. **`transpose(grid)`**: rows become columns (lists of lists).
