# HINTS // 21 STREET INTERFACE

## build_parser
<details><summary>Hint 1</summary>

Global options go on the main parser *before* you call `add_subparsers(dest="command",
required=True)`. Each subcommand gets its own parser from `sub.add_parser("call")`.
</details>
<details><summary>Hint 2</summary>

`call.add_argument("--floor", type=int, required=True, choices=range(-9, 31))`. `type`
converts first, then `choices` checks the result.
</details>

## legacy_opts
<details><summary>Hint</summary>

`opts, rest = getopt.getopt(argv, "vf:", ["verbose", "floor="])`. Loop over `opts` and
match both the short and the long spelling of each option.
</details>

## read_code
<details><summary>Hint</summary>

The prompt function is passed in, so tests can fake it. Call it, `.strip()`, and raise if
the result is empty.
</details>

## LiftShell
<details><summary>Hint 1</summary>

Write a helper, `def say(self, text): self.stdout.write(text + "\n")`. `cmd.Cmd` sets
`self.stdout` from the constructor argument.
</details>
<details><summary>Hint 2</summary>

In `do_floor`, try `int(arg)` and catch `ValueError`, then range-check. `do_quit` returns
`True`, which is what makes `onecmd` return `True` and `cmdloop` stop.
</details>
<details><summary>Hint 3</summary>

`complete_status(self, text, line, begidx, endidx)` returns
`[o for o in ("json", "brief") if o.startswith(text)]`.
</details>

## make_completer
<details><summary>Hint</summary>

Inside the closure: `matches = [w for w in words if w.startswith(text)]`, then return
`matches[state]` if it exists, else `None`.
</details>
