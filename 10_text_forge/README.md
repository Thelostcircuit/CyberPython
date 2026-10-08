# 10 // TEXT FORGE

```
[PYTHIA-9] input: coil_mail_0314.mbx ── messages: 96 ── encodings: MIXED ── legibility: poor
```

**Modules:** `string`, `string.templatelib` (t-strings), `textwrap`, `difflib`, `unicodedata`, `codecs`, `reprlib`, `pprint`, `stringprep`, `encodings`

Iris's outgoing mail from the night she was taken is a mess on purpose. Some of it is
ROT13'd. Some is written in lookalike Unicode letters to dodge keyword filters. Two messages
are near-identical copies of Ouroboros's public press release, except that she changed a few
words in each. And one of them is just a template with the blanks left empty.

> **MONTY:** She was hiding in the *shape* of the text. Clever girl. We'll need the text tools:
> templates to fill the blanks, `difflib` to spot her edits, `unicodedata` to see through the
> lookalike letters, `codecs` for the ROT13, and `textwrap` to make the result readable.
> Python's `str` is only the start. The library has a whole forge.

---

## ▓ TECH BRIEFING

### `string`: constants, Template, capwords

```python
import string
string.ascii_letters  string.ascii_lowercase  string.ascii_uppercase
string.digits  string.hexdigits  string.octdigits  string.punctuation
string.whitespace  string.printable
string.capwords("hale  voss")                 # 'Hale Voss'

t = string.Template("Subject $who in rack ${rack}X")
t.substitute(who="IV", rack="C-17")           # KeyError if a name is missing
t.safe_substitute(who="IV")                   # leaves ${rack} in place instead
```

`string.Formatter` exposes the machinery behind `str.format`, for building your own format
languages.

### t-strings: `string.templatelib` (Python 3.14)

A **t-string** looks like an f-string but with `t`, and it *doesn't* produce a string. It
produces a `Template` object that keeps the literal parts and the interpolated values apart,
so your code decides how to combine them. That's how you make HTML or SQL safe:

```python
from string.templatelib import Template, Interpolation, convert

name = "<script>"
tmpl = t"Hello {name!r:>10}!"
tmpl.strings          # ('Hello ', '!')
tmpl.values           # ('<script>',)
for part in tmpl:     # iterating gives str pieces and Interpolation objects (empty strs skipped)
    if isinstance(part, Interpolation):
        part.value, part.expression, part.conversion, part.format_spec
        # '<script>', 'name', 'r', '>10'
        text = format(convert(part.value, part.conversion), part.format_spec)
```

`convert(value, conversion)` applies `!r` / `!s` / `!a` the way an f-string would.

### `textwrap`

```python
import textwrap
textwrap.wrap(text, width=40)          # list of lines
textwrap.fill(text, width=40)          # one string with newlines
textwrap.shorten("a long line", 8)     # 'a [...]'  collapses whitespace, truncates at a word
textwrap.dedent(block)                 # remove common leading indentation
textwrap.indent(block, "> ")           # prefix every (non-blank) line
```

### `difflib`

```python
import difflib
difflib.SequenceMatcher(None, a, b).ratio()        # similarity 0.0 .. 1.0
difflib.get_close_matches("scna", ["scan", "lock"])  # ['scan']  "did you mean"
list(difflib.unified_diff(old_lines, new_lines, "a", "b", lineterm=""))  # like `diff -u`
difflib.ndiff(a, b)       # human-readable, with ? hint lines
difflib.HtmlDiff().make_table(a, b)                # side-by-side HTML
```

### `unicodedata`

Every Unicode character has a name, a category, and decompositions:

```python
import unicodedata
unicodedata.name("é")                  # 'LATIN SMALL LETTER E WITH ACUTE'
unicodedata.lookup("SNAKE")            # '🐍'
unicodedata.category("é")              # 'Ll' (letter, lowercase);  'Mn' = combining mark
unicodedata.normalize("NFKD", "ﬁé")    # 'fié'  compatibility-decomposed
unicodedata.combining("́")        # 230 (non-zero = a combining mark)
unicodedata.numeric("½")               # 0.5
```

Normal forms: **NFC** composes (`é` is one code point), **NFD** decomposes (`e` + accent),
and **NFKC**/**NFKD** also fold "compatibility" characters (`ﬁ` → `fi`, full-width `Ａ` → `A`).
Normalise before you compare user-supplied text.

`stringprep` implements the RFC 3454 tables used when preparing internet identifiers (like
usernames in some protocols). You'd only reach for it when implementing such a protocol.

### `codecs` and `encodings`

```python
import codecs
codecs.encode("Iris", "rot13")          # 'Vevf'   text-to-text codec
codecs.decode(b"4972", "hex")           # b'Ir'    bytes-to-bytes codec
codecs.lookup("utf-8").name             # 'utf-8'
codecs.BOM_UTF8                         # b'\xef\xbb\xbf'
codecs.getincrementaldecoder("utf-8")() # decode a stream chunk by chunk, split code points OK
```

The codecs themselves live in the `encodings` package (`encodings.utf_8`, `encodings.idna`,
...), and `str.encode`/`bytes.decode` find them there by name. Error handlers:
`"strict"` (the default), `"ignore"`, `"replace"`, `"backslashreplace"`,
`"surrogateescape"`.

### `reprlib` and `pprint`

```python
import reprlib, pprint
reprlib.repr(list(range(1000)))        # '[0, 1, 2, 3, 4, 5, ...]'  size-limited repr
r = reprlib.Repr(maxlist=3, maxstring=10); r.repr(obj)
@reprlib.recursive_repr()               # make __repr__ safe on self-referencing objects

pprint.pprint(big_nested_dict)          # line-wrapped, sorted dict keys
pprint.pformat(obj, width=40)           # the same, as a string
pprint.pp(obj)                          # like pprint but keeps dict insertion order
```

---

## ▓ THE JOB

In `job.py`:

1. **`fill_blanks(template, **values)`**: `string.Template.safe_substitute`.
2. **`safe_markup(tmpl)`**: render a **t-string**, escaping `& < > " '` in every interpolated value (after applying its conversion and format spec) but *not* in the literal parts.
3. **`wrap_quote(text, width)`**: wrap the text to `width` and prefix every line with `"> "`.
4. **`clean_block(text)`**: dedent an indented block and strip blank lines from both ends.
5. **`closest_command(word, commands)`**: the best "did you mean", or `None`.
6. **`edits(old, new)`**: the changed lines between two texts, via `unified_diff`.
7. **`similarity(a, b)`**: the `SequenceMatcher` ratio, rounded to 2 places.
8. **`ascii_fold(text)`**: see through lookalikes. NFKD-normalise, then drop the combining marks.
9. **`unrot(text)`**: ROT13 through `codecs`.
10. **`short_repr(obj)`** and **`pretty(obj)`**: bounded reprs with `reprlib`, and a pretty-print with `pprint`.
