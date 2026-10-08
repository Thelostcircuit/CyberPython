# 43 // OUROBOROS

```
[03:14:00 TST] ── THE GAP IS OPEN ── T-minus 9:00 ── wing C door: held by R. Okonkwo
```

The dock lights flicker as the camera loop engages. Sable walks the crew through the loading
bay like she still works there. Dex rides the freight lift down with the deck in his arms. At
the wing C door, a tired woman with a WORLD'S OKAYEST AUNT mug looks at you for one long
second, and swipes her badge.

Inside, the racks hum at 3.2 hertz. Rack C-17 is warm to the touch.

> **MONTY:** The intake port is ready. It runs **SNAKE-1**, Ouroboros's little stack machine.
> Iris wrote the release program in SNAKE-1 assembly. We assemble it, we run it on our own VM
> to prove what it does, and then we send it through. Everything you've learned goes into this
> one: parsing, data structures, classes, errors, testing.
>
> Nine minutes. Let's build a computer.

---

## ▓ THE MACHINE: SNAKE-1

SNAKE-1 is a **stack machine**. Instructions push integers onto a stack and pop them off. It
also has named variables, a program counter, and a call stack for subroutines.

### Assembly syntax

```
; a comment runs to the end of the line
start:          ; a label marks the next instruction's address (a label can share a line)
    PUSH 3      ; one instruction per line, with an optional argument
loop: DUP
    JNZ loop
    HALT
```

Opcodes are case-insensitive. Labels are case-sensitive names (`[A-Za-z_]\w*`) followed by `:`.

### Instructions

| Op | Arg | Effect |
|---|---|---|
| `PUSH n` | int | push n |
| `POP` | | discard the top |
| `DUP` | | duplicate the top |
| `SWAP` | | swap the top two |
| `ADD` `SUB` `MUL` `DIV` `MOD` | | pop b, pop a, push a∘b (`DIV`/`MOD` floor, like `//` and `%`) |
| `EQ` `LT` | | pop b, pop a, push 1 if a == b (or a < b), else 0 |
| `LOAD x` | name | push variable x |
| `STORE x` | name | pop into variable x |
| `JMP L` | label | jump to L |
| `JZ L` / `JNZ L` | label | pop. Jump if it was zero / non-zero |
| `CALL L` | label | push the return address onto the call stack, then jump to L |
| `RET` | | pop the return address and jump there |
| `PRINT` | | pop and append to the output |
| `RELEASE` | | pop a subject number and append it to the released list |
| `HALT` | | stop |

Running off the end of the program also stops the machine.

---

## ▓ THE JOB

In `job.py`:

1. **`parse_line(line)`**: split one source line into `(label, op, arg)`, with any part possibly `None`.
2. **`assemble(source)`**: two passes. First record the label addresses, then build a list of `Instr(op, arg)` with labels turned into addresses and numbers into ints. Report problems as `AsmError` with the **line number**: unknown opcodes, a missing or unwanted argument, a bad number, an unknown or duplicate label.
3. **`disassemble(program)`**: print a program back out as text, one instruction per line.
4. **`VM.run(program, max_steps)`**: execute. Return a `Result` holding the output, the released subjects, and the variables. Raise `VMError` for stack underflow, an unknown variable, division by zero, a `RET` with no caller, or running more than `max_steps` instructions (so an infinite loop can't hang the port).
5. **`run_source(source)`**: assemble and run in one call.

The tests end by running Iris's actual release program. Then the deck decrypts the ending.

Every module you need is in the standard library. This is the only job in the course without
hints about *how*. `HINTS.md` has a few nudges, but you've done every piece of this before.
