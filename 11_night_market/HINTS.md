# HINTS // 11 NIGHT MARKET

## Item
<details><summary>Hint</summary>

`Item = namedtuple("Item", ["name", "price", "qty"], defaults=[1])`. Defaults apply to the
*rightmost* fields.
</details>

## last_n
<details><summary>Hint</summary>

`list(deque(events, maxlen=n))`. A full deque drops items from the other end.
</details>

## LRU
<details><summary>Hint 1</summary>

Keep `self._data = OrderedDict()`. The front is the least recently used entry, and the back is
the most recent.
</details>
<details><summary>Hint 2</summary>

`get`: `self._data.move_to_end(key)`, then return. `put`: assign, `move_to_end`, and if the
dict is too big, `self._data.popitem(last=False)` pops from the front.
</details>

## container_kind
<details><summary>Hint</summary>

Loop over `[(Mapping, "mapping"), (Sequence, "sequence"), (Set, "set"), (Iterable, "iterable")]`
and return the first `isinstance` hit. A `dict` is iterable too, which is why the order matters.
</details>

## price_band
<details><summary>Hint</summary>

`BAND_NAMES[bisect.bisect_right(BAND_CUTOFFS, price)]`. `bisect_right` returns how many
cutoffs are `<= price`.
</details>

## pack / unpack
<details><summary>Hint</summary>

`array("h", readings).tobytes()`. For the reverse: `a = array("h"); a.frombytes(data);
return a.tolist()`.
</details>

## job_order
<details><summary>Hint</summary>

`list(TopologicalSorter(deps).static_order())` inside `try`, with `except CycleError: return None`.
</details>

## Access / can
<details><summary>Hint</summary>

```python
class Access(Flag):
    READ = auto()
    WRITE = auto()
    EXEC = auto()
    ALL = READ | WRITE | EXEC
```
`can` is `needed in granted`: a flag contains another flag if all of its bits are set.
</details>

## Registry
<details><summary>Hint</summary>

`self._refs = weakref.WeakValueDictionary()`. Use it like a dict. Entries disappear by
themselves once nothing else refers to the object.
</details>
