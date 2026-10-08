# 09 // PATTERN HUNTER

```
[PYTHIA-9] input: ouroboros_facilities.log ── 14,203,551 lines ── 2.3 GB ── structure: "some"
```

**Modules:** `re`

The janitor's log dump is exactly what Mother Adder promised: an avalanche. Door events,
HVAC alarms, badge swipes, coffee-machine faults, and, buried among them, Coil intake records
written by forty different systems in forty different formats.

> **DEX:** I tried searching for "rack". Four million hits. I tried "Iris". Zero.
>
> **MONTY:** Because you searched for *words*. You want to search for *shapes*. "Two capital
> letters, a dash, three more, a dash, four digits." That's a **regular expression**, a tiny
> language for describing patterns in text, and Python has it in the `re` module. It looks
> like line noise at first. Give it an hour and it'll look like a scalpel.

---

## ▓ TECH BRIEFING

### The functions

```python
import re
re.search(r"\d+", "rack 17")        # first match anywhere → Match object or None
re.match(r"\d+", "17 racks")        # only at the START of the string
re.fullmatch(r"\d+", "17")          # the WHOLE string must match
re.findall(r"\d+", "a1 b22")        # ['1', '22']  all matches as strings
re.finditer(r"\d+", "a1 b22")       # iterator of Match objects (lazy, has positions)
re.sub(r"\d", "#", "a1b2")          # 'a#b#'   replace
re.subn(r"\d", "#", "a1b2")         # ('a#b#', 2)   ...and count
re.split(r"[,;]\s*", "a, b;c")      # ['a', 'b', 'c']
re.escape("1.5+x")                  # '1\\.5\\+x'  make text safe to embed in a pattern
```

Always use **raw strings** `r"..."` for patterns, so `\d` reaches `re` unmangled.

### The pattern language

| Pattern | Matches |
|---|---|
| `.` | any char except newline (any char at all with `re.DOTALL`) |
| `\d` `\w` `\s` | digit, word char `[A-Za-z0-9_]` plus Unicode letters, whitespace |
| `\D` `\W` `\S` | the opposites |
| `[abc]` `[a-z0-9]` `[^x]` | character class, range, negated class |
| `^` `$` | start and end of string (of each line with `re.MULTILINE`) |
| `\b` | word boundary |
| `*` `+` `?` | 0+, 1+, 0 or 1 (all **greedy**) |
| `{3}` `{2,5}` `{2,}` | exact, range, at least |
| `*?` `+?` `??` | **lazy** versions: match as little as possible |
| `a\|b` | alternation |
| `(...)` | capturing group |
| `(?:...)` | non-capturing group |
| `(?P<name>...)` | named group |
| `\1` `(?P=name)` | backreference inside the pattern |
| `(?=...)` `(?!...)` | lookahead: followed by / not followed by (consumes nothing) |
| `(?<=...)` `(?<!...)` | lookbehind |

### Match objects

```python
m = re.search(r"(?P<rack>[A-Z])-(?P<num>\d+)", "moved to C-17 at 22:10")
m.group()          # 'C-17'   the whole match (same as m.group(0))
m.group(1)         # 'C'
m["num"]           # '17'
m.groups()         # ('C', '17')
m.groupdict()      # {'rack': 'C', 'num': '17'}
m.start(), m.end(), m.span()     # (9, 13) ...
```

`findall` returns strings when the pattern has no groups, a string per match with one group,
and **tuples of groups** when there are several. It surprises everyone once.

### Compiling and flags

```python
RACK = re.compile(r"""
    (?P<wing>[A-Z])       # wing letter
    -
    (?P<slot>\d{2})       # two-digit slot
""", re.VERBOSE)          # VERBOSE ignores whitespace and allows comments

RACK.findall(text)
re.compile(p, re.IGNORECASE | re.MULTILINE)   # flags combine with |
```

`re.I` / `re.IGNORECASE`, `re.M` / `re.MULTILINE`, `re.S` / `re.DOTALL`, `re.X` / `re.VERBOSE`,
`re.A` / `re.ASCII`. Inline form: `(?i)` at the start of a pattern.

### Replacements

```python
re.sub(r"(\d+)/(\d+)", r"\2-\1", "3/14")              # '14-3'    group references
re.sub(r"(?P<d>\d+)", r"<\g<d>>", "a1")                # 'a<1>'
re.sub(r"\d+", lambda m: str(int(m[0]) * 2), "a5 b7")  # 'a10 b14' function replacement
```

### When not to use regex

`str` methods (`in`, `startswith`, `split`, `replace`) are faster and clearer for fixed text.
Regex can't properly parse nested structures like HTML or JSON; use a parser (ch 18, 27, 34).
Watch out for patterns like `(a+)+`: on bad input they can take exponential time.

Under the hood, `re` uses the private helpers `sre_compile`, `sre_parse` and `sre_constants`
(the public names are deprecated aliases; you never import them yourself).

---

## ▓ THE JOB

The log format is described in `job.py`. Write:

1. **`subject_ids(text)`**: every subject ID like `OS-ENG-4471`, in order.
2. **`parse_line(line)`**: pull the timestamp, level, rack and subject out of a log line with named groups. Return `None` if the line doesn't match.
3. **`redact_emails(text)`**: replace every email address with `[REDACTED]`.
4. **`squash_ws(text)`**: collapse every run of whitespace to one space, and strip the ends.
5. **`iso_dates(text)`**: rewrite `DD/MM/YYYY` dates as `YYYY-MM-DD` with a backreference replacement.
6. **`strong_passphrase(s)`**: `fullmatch` plus lookaheads. At least 12 characters, with an upper, a lower, a digit, and no whitespace.
7. **`tokens(expr)`**: split an expression like `rack_count*2 + 17.5` into numbers, names and operators.
8. **`split_fields(line)`**: split on commas or semicolons, eating any spaces around them.
9. **`censor(text, words)`**: replace whole words (case-insensitive) with `*` of the same length.
