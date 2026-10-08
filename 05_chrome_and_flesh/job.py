"""05 // CHROME AND FLESH: model Sable's cyberware before the cleanup team arrives."""

from __future__ import annotations

from typing import Iterator


class Credits:
    """Money in whole credits.

    Credits(1200)                 repr -> "Credits(1200)",  str -> "¢1,200"
    Credits(5) + Credits(3)       -> Credits(8)      (only Credits + Credits; else TypeError)
    Credits(5) - Credits(3)       -> Credits(2)
    Credits(5) * 3, 3 * Credits(5) -> Credits(15)    (only int multipliers; else TypeError)
    ==, <, and hash() work by amount;  Credits(0) is falsy.
    """

    def __init__(self, amount: int):
        self.amount = amount

    pass  # TODO: write the dunder methods described in the docstring


class Implant:
    """One piece of chrome.

    SLOTS lists the valid slot names. Creating an Implant with any other slot raises ValueError.
    describe() -> "Gorilla Arm [arm] 40W"
    repr       -> "Implant('Gorilla Arm', 'arm', 40)"   (use the real class name, so a
                   subclass's repr shows ITS name)
    Implant.from_spec("Kiroshi Optics:eye:12") builds an Implant (or a subclass, if called on one)
    Implant.valid_slot("eye") -> True
    """

    SLOTS = ("arm", "eye", "spine", "heart", "leg")

    def __init__(self, name: str, slot: str, power: int):
        raise NotImplementedError("TODO")

    def describe(self) -> str:
        raise NotImplementedError("TODO")

    def __repr__(self) -> str:
        raise NotImplementedError("TODO")

    @classmethod
    def from_spec(cls, spec: str) -> Implant:
        raise NotImplementedError("TODO")

    @staticmethod
    def valid_slot(slot: str) -> bool:
        raise NotImplementedError("TODO")


class Weapon(Implant):
    """An Implant with `damage`.

    Weapon("Mantis Blades", "arm", 30, damage=80).describe()
        -> "Mantis Blades [arm] 30W DMG 80"
    Its repr can stay the inherited one: "Weapon('Mantis Blades', 'arm', 30)".
    """

    pass  # TODO: __init__ with damage, and describe()


class Chassis:
    """A body that holds implants, at most one per slot.

    Chassis(budget=100)
      .budget        property; setting it below 0 raises ValueError (including in __init__)
      .power_draw    read-only property: total power of installed implants
      .install(imp)  ValueError if that slot is taken, or if power_draw would exceed budget
      len(c)         number of implants
      iter(c)        implants in installation order
      "Gorilla Arm" in c   True if an installed implant has that NAME
      c["arm"]       the implant in that slot; KeyError if empty
    """

    def __init__(self, budget: int):
        raise NotImplementedError("TODO")

    pass  # TODO: budget/power_draw properties, install(), and the container dunders
