# HINTS // 43 OUROBOROS

Nudges, not answers. You've done every piece of this before.

## parse_line
<details><summary>Nudge</summary>

Cut the comment off first (`split(";", 1)[0]`). A regex like `([A-Za-z_]\w*)\s*:` at the start
of the line catches the label (ch 09). Whatever's left is split on whitespace.
</details>

## assemble
<details><summary>Nudge</summary>

Pass 1 walks the lines keeping a count of *instructions* seen so far. That count is the
address a label points to. Pass 2 needs the line numbers too, so keep `(line_no, op, arg)`
triples from pass 1. `OPCODES[op]` tells you what kind of argument to expect.
</details>

## VM.run
<details><summary>Nudge 1</summary>

The state is a stack (a list), a call stack (another list), the variables (a dict), a program
counter and a step counter. Advance `pc` *before* executing, so jumps simply overwrite it.
</details>
<details><summary>Nudge 2</summary>

`match op:` (ch 02) with one `case` per instruction keeps it readable. For binary operators,
pop **b first, then a**. A small `pop()` helper that raises `VMError` on an empty stack
covers underflow everywhere.
</details>
<details><summary>Nudge 3</summary>

Build a new `Result()` inside `run()`, not in `__init__`, so every run starts fresh.
</details>
