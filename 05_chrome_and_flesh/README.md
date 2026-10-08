# 05 // CHROME AND FLESH

```
[PYTHIA-9] location: Sable's garage, Tier 3 ── threat: Ouroboros cleanup team, ETA 20 min
```

You get there first, just about. Sable's garage is full of disassembled combat chrome. She's
sitting on an engine block with her left arm open from wrist to shoulder, poking at the wiring
with a screwdriver. The arm is Ouroboros-grade. So, you notice, is the kill-switch in it.

> **SABLE:** Termination notice. Cute. That means a cleanup team, and a remote shutdown code for
> every implant I've got. Heart regulator included.
>
> I need to inventory everything in me: what's installed, which slot, how much power it pulls,
> which ones they can reach remotely. And I need to do it before they get here.
>
> **MONTY:** Then we'll need to **model** her. Not the person, the chrome. In Python you don't
> just have data, you have **objects**: data and behaviour bundled together, each with its own
> type. You write the type with `class`, and then your objects can do arithmetic, compare
> themselves, act like containers. Whatever you teach them.

---

## ▓ TECH BRIEFING

### A class

```python
class Implant:
    SLOTS = ("arm", "eye", "spine", "heart")      # class attribute: shared by all instances

    def __init__(self, name: str, slot: str, power: int):
        self.name = name                           # instance attributes
        self.slot = slot
        self.power = power

    def describe(self) -> str:                     # a method: `self` is the instance
        return f"{self.name} [{self.slot}] {self.power}W"

arm = Implant("Gorilla Arm", "arm", 40)
arm.describe()          # Python calls Implant.describe(arm)
arm.power = 45          # attributes are just assignable
```

### Dunder ("double underscore") methods

Special methods make your objects work with Python's operators and built-ins:

| You write | Python calls |
|---|---|
| `repr(x)`, the REPL | `x.__repr__()`: unambiguous, ideally looks like the constructor call |
| `str(x)`, `print(x)`, f-strings | `x.__str__()` (falls back to `__repr__`) |
| `x == y` | `x.__eq__(y)`: return `NotImplemented` for types you don't handle |
| `x < y`, `<=`, `>`, `>=` | `__lt__`, `__le__`, `__gt__`, `__ge__` |
| `hash(x)`, dict keys, sets | `__hash__` (defining `__eq__` sets it to `None` unless you define it) |
| `x + y`, `x - y`, `x * y` | `__add__`, `__sub__`, `__mul__`, `__truediv__`, ... |
| `3 * x` (int on the left) | `x.__rmul__(3)` after `int.__mul__` returns `NotImplemented` |
| `x += y` | `__iadd__` (falls back to `__add__`) |
| `bool(x)`, `if x:` | `__bool__` (falls back to `__len__`) |
| `len(x)` | `__len__` |
| `for i in x` | `__iter__` |
| `item in x` | `__contains__` |
| `x[k]`, `x[k] = v`, `del x[k]` | `__getitem__`, `__setitem__`, `__delitem__` |
| `x(...)` | `__call__` |
| `with x:` | `__enter__` / `__exit__` (ch 06) |

```python
class Credits:
    def __init__(self, amount: int):
        self.amount = amount
    def __repr__(self):
        return f"Credits({self.amount})"
    def __add__(self, other):
        if not isinstance(other, Credits):
            return NotImplemented          # lets Python try other.__radd__, then TypeError
        return Credits(self.amount + other.amount)
    def __eq__(self, other):
        return isinstance(other, Credits) and self.amount == other.amount
    def __hash__(self):
        return hash(self.amount)           # equal objects MUST have equal hashes
```

### Properties

A `@property` looks like an attribute but runs code. Use one for computed values, and add a
setter to validate:

```python
class Chassis:
    def __init__(self, budget):
        self.budget = budget               # goes through the setter below!

    @property
    def budget(self):
        return self._budget                # leading underscore = "internal, please don't touch"

    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("budget must be >= 0")
        self._budget = value
```

A property without a setter is read-only: assigning to it raises `AttributeError`.

### Inheritance and super()

```python
class Weapon(Implant):                     # a Weapon IS an Implant
    def __init__(self, name, slot, power, damage):
        super().__init__(name, slot, power)       # run the parent's __init__
        self.damage = damage

    def describe(self):                           # override...
        return super().describe() + f" DMG {self.damage}"   # ...and extend

isinstance(Weapon(...), Implant)   # True
issubclass(Weapon, Implant)        # True
Weapon.__mro__                     # method resolution order: Weapon → Implant → object
```

Python supports multiple inheritance. `super()` follows the MRO, which makes "mixin"
classes work.

### classmethod and staticmethod

```python
class Implant:
    @classmethod
    def from_spec(cls, spec: str):         # alternative constructor: gets the CLASS
        name, slot, power = spec.split(":")
        return cls(name, slot, int(power)) # cls, so subclasses build subclasses

    @staticmethod
    def valid_slot(slot: str) -> bool:     # just a function that lives in the class namespace
        return slot in Implant.SLOTS
```

### Odds and ends

- `vars(obj)` / `obj.__dict__`: an instance's attributes as a dict.
- `getattr(obj, "name", default)`, `setattr`, `hasattr`, `delattr`: attribute access by string.
- `__slots__ = ("name", "slot")` on a class removes the per-instance `__dict__`. It saves
  memory and blocks typo'd attributes.
- `__class__.__name__` gives you the type's name. That's useful in `__repr__` for subclasses.
- Name mangling: `self.__secret` becomes `self._ClassName__secret`. That's for avoiding
  subclass clashes, not for security.
- `dataclasses` (ch 28) write `__init__`/`__repr__`/`__eq__` for you. Learn to write them by
  hand first.

---

## ▓ THE JOB

In `job.py`, build Sable's inventory system:

1. **`Credits`**: an immutable-ish money type. It needs `repr`, a `str` like `¢1,200`, `==`, `<`,
   hashing, `+` and `-` with other `Credits`, `*` by an int on **either side**, and `bool`
   (zero is falsy).
2. **`Implant`**: `name`, `slot`, `power`, a `describe()` method, `repr`, a `from_spec()`
   classmethod, and a `valid_slot()` staticmethod. It raises `ValueError` for an unknown slot.
3. **`Weapon(Implant)`**: adds `damage` and extends `describe()` with `super()`.
4. **`Chassis`**: a container of implants with a validated `budget` property, a read-only
   `power_draw` property, `install()` (it rejects taken slots and anything over budget),
   `len()`, iteration, `in` by name, and `chassis["arm"]` lookup by slot.
