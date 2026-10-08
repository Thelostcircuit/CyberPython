# 02 // SIGNAL FLOW

```
[PYTHIA-9] location: THE PIT, level -4 ── rain: heavy ── drone traffic: HIGH
```

The Pit is what Coilhaven built on top of when it ran out of up. Forty metres below the
waterline, pumps roaring, every surface slick with runoff and neon. Somewhere down here is a
noodle bar with a green snake on the sign.

Between you and it: the patrol drones. Ouroboros **Watchers**, fist-sized, silent, with red
scanning eyes. They fly fixed routes, and they flag anything that walks through a scan cone.

> **MONTY:** Drones are just programs with propellers. They follow **control flow**: if this,
> then that, loop until something happens. Learn to read their logic and you can walk right
> through it. Learn to *write* that logic and you can make me do the walking.
>
> Let's teach me to make decisions.

---

## ▓ TECH BRIEFING

### Blocks are indentation

Python has no braces. A colon opens a block, and the block is everything indented under it
(4 spaces by convention):

```python
if battery < 20:
    print("low")
    dim_screen()
print("always runs")
```

### if / elif / else, and conditional expressions

```python
if level >= 90:
    state = "hot"
elif level >= 50:
    state = "warm"
else:
    state = "cold"

state = "hot" if level >= 90 else "cold"      # one-line conditional expression
```

### while loops

```python
fuel = 3
while fuel > 0:
    print("burn", fuel)
    fuel -= 1
```

`while True:` with a `break` inside is a normal, idiomatic loop.

### for loops and range

`for` walks over any *iterable*: lists, strings, ranges, dicts, files...

```python
for ch in "abc": ...
for i in range(5):          # 0 1 2 3 4
for i in range(2, 10, 3):   # 2 5 8
for i in range(5, 0, -1):   # 5 4 3 2 1
for i, drone in enumerate(["w1", "w2"]):     # (0, 'w1'), (1, 'w2')
for name, level in zip(names, levels):       # pairs up two sequences
```

### break, continue, and the loop `else`

```python
for reading in readings:
    if reading is None:
        continue            # skip to the next item
    if reading > 100:
        break               # leave the loop now
else:
    print("no break")       # runs only if the loop finished WITHOUT break
```

The `else` on a loop is unusual but handy for search loops: "looked everywhere, didn't find it".

### The walrus operator

`:=` assigns inside an expression. It's handy in `while` conditions:

```python
while (cmd := next_command()) != "quit":
    run(cmd)
```

### match: structural pattern matching

`match` compares a value against **patterns**, and patterns can take structures apart:

```python
match command.split():
    case ["go", direction]:                 # a 2-item list starting with "go"
        move(direction, 1)
    case ["go", direction, steps]:          # captures bind names
        move(direction, int(steps))
    case ["hack", *targets]:                # *rest captures the remainder as a list
        hack(targets)
    case ["wait"] | ["idle"]:               # | means "or"
        pass
    case _:                                 # wildcard: matches anything
        print("unknown")
```

Patterns can match literals, sequences, mappings, classes, and have `if` guards:

```python
match event:
    case {"type": "drone", "id": drone_id} if drone_id.startswith("W"):
        ...                                  # dict pattern: extra keys are allowed
    case {"type": "alarm", "zone": 1 | 2 | 3 as zone}:
        ...                                  # `as` binds the matched sub-value
    case int(n) if n > 0:                    # class pattern + guard
        ...
    case None:
        ...
```

A bare name in a pattern **captures**. It never compares. To compare against a constant, use
a literal or a dotted name (`Color.RED`).

### pass

`pass` is the "do nothing" statement for places where Python needs a block.

---

## ▓ THE JOB

In `job.py`:

1. **`threat_level(scans)`**: `"clear"`, `"watch"`, or `"run"`, depending on how many scans hit you.
2. **`countdown(n)`**: a `while` loop that builds `"3..2..1..GO"`.
3. **`patrol_path(start, step, count, grid)`**: the positions a drone visits on a looping track.
4. **`first_blind_spot(coverage)`**: the index of the first `0` in a coverage list, or `-1`. Use `for`/`else`.
5. **`scan_code(n)`**: FizzBuzz, drone-style: `"SCAN"`, `"LOCK"`, `"SCANLOCK"`, or the number as a string.
6. **`longest_quiet(readings, threshold)`**: the longest run of consecutive readings below a threshold. Skip `None` readings entirely.
7. **`walk(commands)`**: follow movement commands with `match` and return where you end up.
8. **`drone_response(event)`**: react to a drone event dict using mapping patterns and guards.
