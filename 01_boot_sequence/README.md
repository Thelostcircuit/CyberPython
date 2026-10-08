# 01 // BOOT SEQUENCE

```
[PYTHIA-9] cold boot ── firmware: CORRUPT ── last user: ████████ ── battery: 12%
```

The pawn stall in the Pit smelled like solder and fish sauce. The deck cost you everything in
your account: 340 credits for a scratched Pythia-9 with a cracked hinge. The old woman behind
the counter didn't haggle. She just watched you pay, and said, *"Took you long enough."*

Now you're in your hab-cube, rain hammering on the window, and the deck's screen is flickering.

```
>>> _
```

A prompt. Then text starts typing itself.

> **MONTY:** Oh, good. Hands. Lovely. I've been in this box for three weeks with nobody to
> talk to but the cooling fan, and the cooling fan is a terrible conversationalist.
>
> I'm MONTY. I'm an interpreter. I run **Python**, which is what your sister wrote me in. Yes,
> *that* sister. Iris. She left something for you on this deck, but it's locked behind my own
> boot checks, and my boot checks are... broken. She stripped out half my firmware so Ouroboros
> couldn't read it.
>
> So you're going to rebuild it. Don't look at me like that. It's easy. Python is the friendliest
> language in the city. Let's start with the basics: numbers, words, and talking to me properly.

---

## ▓ TECH BRIEFING

### Running Python

```bash
uv run python              # an interactive REPL. Type code, see results. Ctrl-D to leave.
uv run python script.py    # run a file
```

The REPL is your best friend. Every snippet in these briefings can be pasted into it.

### Variables and the core types

A variable is a name attached to a value. There are no declarations and no type keywords:

```python
battery = 12            # int: whole numbers, arbitrarily large (2 ** 1000 works fine)
voltage = 3.7           # float: 64-bit floating point
online = False          # bool: True or False (a subclass of int: True + True == 2)
owner = "Iris"          # str: immutable Unicode text, "double" or 'single' quotes
last_user = None        # None: the "no value" value, its own type (NoneType)

type(battery)           # <class 'int'>
isinstance(online, int) # True
```

Names are `snake_case` by convention. `UPPER_CASE` means "treat this as a constant".
Type hints are optional labels, not enforced at runtime:

```python
battery: int = 12
```

### Arithmetic

```python
7 + 2    # 9
7 - 2    # 5
7 * 2    # 14
7 / 2    # 3.5    true division ALWAYS gives a float
7 // 2   # 3      floor division
7 % 2    # 1      remainder (modulo)
-7 // 2  # -4     floor rounds DOWN, toward negative infinity
2 ** 10  # 1024   power
divmod(7, 2)   # (3, 1)   both at once
abs(-4)        # 4
round(3.14159, 2)  # 3.14
round(2.5)     # 2   ← "banker's rounding": ties go to the even number
0.1 + 0.2      # 0.30000000000000004   floats are binary; see ch 12 for decimal
```

Augmented assignment: `x += 1`, `x *= 2`, `x //= 3` and so on. There is no `x++`.

Conversions: `int("42")`, `float("3.5")`, `str(99)`, `int(3.9)` (→ 3, truncates), `bool(0)`
(→ False). Falsy values: `0`, `0.0`, `""`, `None`, `False`, and empty containers.
Everything else is truthy.

### Comparisons and logic

```python
3 < 5 <= 5          # True, comparisons CHAIN: means (3 < 5) and (5 <= 5)
x == y  x != y      # equality
a is None           # identity: use `is` only for None (and sentinels)
not a   a and b   a or b     # short-circuit; they return one of the operands:
"" or "default"     # "default"
```

### Strings

```python
name = "iris vale"
len(name)            # 9
name[0]              # 'i'           indexing, zero-based
name[-1]             # 'e'           negative counts from the end
name[0:4]            # 'iris'        slicing [start:stop], stop excluded
name[5:]             # 'vale'
name[::-1]           # 'elav siri'   [start:stop:step]
name.upper()  name.title()  name.capitalize()  name.swapcase()
"  pad  ".strip()    # 'pad'   also lstrip()/rstrip()
"a,b,c".split(",")   # ['a', 'b', 'c']
"-".join(["a", "b"]) # 'a-b'
"x.log".endswith(".log")   "x.log".removesuffix(".log")   # 'x'
"hello".replace("l", "L")  # 'heLLo'
"ab" * 3             # 'ababab'
"ris" in name        # True
name.find("v")       # 5   (-1 if missing; .index() raises instead)
name.count("i")      # 2
"42".isdigit()       # True
```

Strings are **immutable**. Every method returns a *new* string.

### f-strings and format specs

```python
level, temp = 7, 36.456
f"battery {level}%"                # 'battery 7%'
f"{temp:.1f}"                      # '36.5'     1 decimal place
f"{level:>4}"                      # '   7'     right-align, width 4
f"{'id':<6}|"                      # 'id    |'  left-align
f"{'x':^5}"                        # '  x  '    centre
f"{level:03d}"                     # '007'      zero-pad
f"{1234567:,}"                     # '1,234,567'
f"{0.25:.0%}"                      # '25%'
f"{level=}"                        # 'level=7'  great for debugging
```

The mini-language is `{value:[fill][align][width][,][.precision][type]}`.

### Printing and input

```python
print("a", "b", sep="-", end="!\n")   # a-b!
answer = input("pin> ")                # always returns a str
```

---

## ▓ THE JOB

Rebuild MONTY's boot checks in `job.py`. Each function has a docstring saying exactly what it
has to return.

1. **`cell_voltage(total, cells)`**: the voltage per cell, rounded to 2 decimal places.
2. **`split_credits(total, crew)`**: a tuple `(each, left_over)` after splitting credits evenly.
3. **`is_safe_level(level)`**: whether the battery is from 20 to 95 inclusive. Use a chained comparison.
4. **`callsign(first, last)`**: `"VALE, Iris"` style: surname upper-cased, first name capitalised, whitespace stripped.
5. **`status_line(name, level, temp)`**: a fixed-width status line built with format specs.
6. **`parse_reading(raw)`**: turn `"  36.6C "` or `"36.6 c"` into the float `36.6`.
7. **`mask_card(number)`**: hide everything except the last four characters with `*`.
8. **`signal_label(strength)`**: describe a signal strength, including `None` for "no signal".

Then prove it:

```bash
cd 01_boot_sequence
uv run python -m unittest -v
uv run deck.py jack-in
```
