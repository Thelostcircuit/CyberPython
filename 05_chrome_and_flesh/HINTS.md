# HINTS // 05 CHROME AND FLESH

## Credits
<details><summary>Hint 1: which dunders?</summary>

`__repr__`, `__str__`, `__eq__`, `__lt__`, `__hash__`, `__add__`, `__sub__`, `__mul__`,
`__rmul__`, `__bool__`. `sorted()` and `max()` only need `__lt__`.
</details>
<details><summary>Hint 2: type checks</summary>

Return `NotImplemented` (not `raise`) when `other` isn't the right type. Python then tries the
reflected method, and if that fails too it raises `TypeError` for you. For `*`, check
`isinstance(n, int)`.
</details>
<details><summary>Hint 3: the other side</summary>

`__rmul__ = __mul__` inside the class body reuses the same function for `3 * Credits(5)`.
Formatting: `f"¢{self.amount:,}"`.
</details>

## Implant
<details><summary>Hint</summary>

In `__init__`, validate first: `if not self.valid_slot(slot): raise ValueError(...)`.
For the repr, `type(self).__name__` gives `"Weapon"` for a Weapon. Use `!r` to get quotes:
`f"{type(self).__name__}({self.name!r}, {self.slot!r}, {self.power})"`.
</details>

## Weapon
<details><summary>Hint</summary>

```python
def __init__(self, name, slot, power, damage=0):
    super().__init__(name, slot, power)
    self.damage = damage
```
And `describe` returns `super().describe() + f" DMG {self.damage}"`.
</details>

## Chassis
<details><summary>Hint 1: storage</summary>

Store implants in a dict keyed by slot: `self._implants = {}`. Dicts keep insertion order, so
iterating `.values()` gives installation order.
</details>
<details><summary>Hint 2: the budget property</summary>

In `__init__` write `self.budget = budget` (no underscore), so the setter validates it.
The setter stores into `self._budget`.
</details>
<details><summary>Hint 3: the container dunders</summary>

`__len__` → `len(self._implants)`, `__iter__` → `iter(self._implants.values())`,
`__contains__` → `any(i.name == name for i in ...)`, `__getitem__` → `self._implants[slot]`.
</details>
