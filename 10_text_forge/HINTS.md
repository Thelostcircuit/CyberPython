# HINTS // 10 TEXT FORGE

## Task 1: fill_blanks
<details><summary>Hint</summary>

`string.Template(template).safe_substitute(values)`. `safe_substitute` takes a mapping, or
keyword arguments.
</details>

## Task 2: safe_markup
<details><summary>Hint 1</summary>

`for part in tmpl:` gives you plain `str` pieces and `Interpolation` objects. Check with
`isinstance(part, Interpolation)`.
</details>
<details><summary>Hint 2</summary>

`text = format(convert(part.value, part.conversion), part.format_spec)`, then escape `&`
**first**. Otherwise you'd double-escape the `&` in `&lt;`.
</details>

## Task 3: wrap_quote
<details><summary>Hint</summary>

`textwrap.indent(textwrap.fill(text, width), "> ")`. The width applies before the prefix.
</details>

## Task 4: clean_block
<details><summary>Hint</summary>

`textwrap.dedent(text).strip("\n")`. Strip only newlines, so the first line's own indentation
survives.
</details>

## Task 6: edits
<details><summary>Hint</summary>

```python
diff = difflib.unified_diff(old.splitlines(), new.splitlines(), n=0, lineterm="")
[l for l in diff if l[:1] in "+-" and not l.startswith(("---", "+++"))]
```
The `@@` hunk headers get filtered out because they start with `@`.
</details>

## Task 8: ascii_fold
<details><summary>Hint</summary>

`"".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))`
</details>

## Task 9: unrot
<details><summary>Hint</summary>

`codecs.decode(text, "rot13")`. ROT13 is its own inverse, so `encode` works too.
</details>

## Task 10: short_repr / pretty
<details><summary>Hint</summary>

`reprlib.Repr(maxlist=3, maxstring=12).repr(obj)` and `pprint.pformat(obj, width=30)`.
</details>
