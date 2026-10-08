# 21 // STREET INTERFACE

```
[PYTHIA-9] target: freight lift 3 maintenance console ── interface: CLI ── users: bored technicians
```

**Modules:** `argparse`, `getopt`, `optparse`, `shlex`, `getpass`, `cmd`, `readline`, `rlcompleter`, `curses`

Iris photographed the lift console's manual page by page. It's a text interface: you type
`liftctl call --floor -6`, or you open an interactive shell and type `floor -6`, `status`,
`quit`. The console logs everything, so whatever you send has to look *exactly* like what a
technician would send.

> **MONTY:** A command-line interface is how most real tools talk to people and scripts.
> Arguments, flags, subcommands, help text, quoting rules, interactive shells with tab
> completion. Python can do all of it. We'll write the lift's client ourselves, so our
> commands come out letter-perfect.

---

## ▓ TECH BRIEFING

### `sys.argv` and the raw input

```python
import sys
sys.argv            # ['liftctl.py', 'call', '--floor', '-6']  (argv[0] is the script)
sys.stdin.read()    # piped input;  sys.stdin.isatty() tells you if a human is typing
sys.exit(2)         # exit status: 0 = success, anything else = failure
```

### `argparse`: the standard way

```python
import argparse
p = argparse.ArgumentParser(prog="liftctl", description="Freight lift control")
p.add_argument("-v", "--verbose", action="count", default=0)   # -vv → 2
p.add_argument("--dry-run", action="store_true")               # a flag → args.dry_run
sub = p.add_subparsers(dest="command", required=True)

call = sub.add_parser("call", help="send the lift to a floor")
call.add_argument("--floor", type=int, required=True, choices=range(-9, 31))
call.add_argument("--priority", choices=["low", "normal", "high"], default="normal")

status = sub.add_parser("status")
status.add_argument("--json", action="store_true")

args = p.parse_args(["-v", "call", "--floor", "-6"])
args.command, args.floor, args.verbose            # 'call', -6, 1
```

Also: positional arguments (`p.add_argument("target")`), `nargs="+"`, `default=`,
`metavar=`, `mutually_exclusive_group()`, `type=` any function (`type=Path`), and
`parse_known_args`. `--help` is generated for you. On bad input argparse prints usage and
raises `SystemExit(2)`.

### `getopt` and `optparse`

The older parsers. You'll meet them in legacy code:

```python
import getopt
opts, rest = getopt.getopt(["-v", "--floor=3", "go"], "vf:", ["verbose", "floor="])
# opts = [('-v', ''), ('--floor', '3')], rest = ['go']     (C-style: a colon means "takes a value")

import optparse                          # deprecated in favour of argparse, but still around
parser = optparse.OptionParser()
parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
options, args = parser.parse_args(argv)
```

### `shlex`: shell-style splitting and quoting

```python
import shlex
shlex.split('liftctl call --note "cargo, fragile"')  # ['liftctl', 'call', '--note', 'cargo, fragile']
shlex.quote("it's here")                            # "'it'\"'\"'s here'"  safe for a shell
shlex.join(["echo", "a b"])                         # "echo 'a b'"
```

Use `shlex.split` to parse a command line, and `shlex.quote`/`join` whenever you *build* one.

### `getpass`

```python
import getpass
code = getpass.getpass("access code: ")   # reads WITHOUT echoing to the screen
getpass.getuser()                         # the login name
```

### `cmd`: build an interactive shell

```python
import cmd
class LiftShell(cmd.Cmd):
    prompt = "lift> "
    def do_floor(self, arg):              # handles "floor -6"; arg is the rest of the line
        """floor N: send the lift to floor N"""   # the docstring becomes `help floor`
        ...
    def complete_floor(self, text, line, begidx, endidx):   # tab completion for `floor`
        return [...]
    def do_quit(self, arg):
        return True                       # returning True stops cmdloop()
    def default(self, line): ...          # unknown commands

LiftShell().cmdloop()                     # or .onecmd("floor -6") to drive it from code
```

Output goes to `self.stdout`, which you can pass in (`LiftShell(stdout=buffer)`) to test it.

### `readline` and `rlcompleter`

On Unix, importing `readline` gives `input()` and `cmd` line editing, history and tab
completion. `readline.set_completer(fn)` installs a completer: a function `fn(text, state)`
that returns the `state`-th completion for `text`, or `None` when there are no more.
`rlcompleter` provides the completer the interactive Python REPL uses for names and
attributes.

### `curses`

`curses` (Unix) builds full-screen terminal UIs: windows, colours, raw key input.
`curses.wrapper(main)` sets the terminal up and restores it even if `main` crashes. Tools
like `htop` work this way. Tests can't easily drive a real terminal, so this job leaves it
out. Write a tiny `curses.wrapper` app of your own to try it.

---

## ▓ THE JOB

In `job.py`:

1. **`build_parser()`**: the `liftctl` argparse parser described in the docstring.
2. **`legacy_opts(argv)`**: parse the old console's options with `getopt`.
3. **`optparse_quiet(argv)`**: an `optparse` parser with `-q/--quiet`, returning `(quiet, args)`.
4. **`split_line(line)`** / **`join_args(args)`**: `shlex`.
5. **`read_code(prompt=getpass.getpass)`**: ask for the access code without echoing it, strip it, and reject empty input.
6. **`LiftShell`**: a `cmd.Cmd` shell with `floor`, `status` and `quit` commands, a `default` handler, and tab completion for `status`.
7. **`make_completer(words)`**: a readline-style `(text, state)` completer.
