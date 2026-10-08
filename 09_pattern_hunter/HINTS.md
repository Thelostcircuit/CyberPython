# HINTS // 09 PATTERN HUNTER

## Task 1: subject_ids
<details><summary>Hint</summary>

`re.findall(r"\bOS-[A-Z]{3}-\d{4}\b", text)`. The `\b` at each end stops it matching inside
a longer token.
</details>

## Task 2: parse_line
<details><summary>Hint 1</summary>

Build one pattern from adjacent raw strings (Python glues them together), with a named group
for each field: `(?P<level>INFO|WARN|ERROR)`. Remember to escape the brackets: `\[` `\]`.
</details>
<details><summary>Hint 2</summary>

Use `re.fullmatch(pattern, line.strip())`, and return `m.groupdict() if m else None`.
`(?P<msg>.*)` happily matches an empty string.
</details>

## Task 3: redact_emails
<details><summary>Hint</summary>

`[\w.+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}`. The repeated non-capturing group eats `ouro.`
and `corp.`, then the final label needs at least two letters.
</details>

## Task 5: iso_dates
<details><summary>Hint</summary>

Three groups, `(\d{2})/(\d{2})/(\d{4})`, and a replacement of `r"\3-\2-\1"`. Wrap it in `\b`
so that `1/3/2091` doesn't partly match.
</details>

## Task 6: strong_passphrase
<details><summary>Hint</summary>

Lookaheads at the start check "somewhere ahead there's an X" without consuming anything:
`(?=.*[A-Z])(?=.*[a-z])(?=.*\d)`. Then `\S{12,}` consumes the whole thing, and forbids
whitespace while it's at it.
</details>

## Task 7: tokens
<details><summary>Hint</summary>

`findall` with an alternation, most specific first:
`\d+(?:\.\d+)?|[A-Za-z_]\w*|[-+*/()]`. Inside a class, put `-` first so it's literal.
</details>

## Task 9: censor
<details><summary>Hint</summary>

Build `r"\b(?:" + "|".join(map(re.escape, words)) + r")\b"`, then
`re.sub(pattern, lambda m: "*" * len(m[0]), text, flags=re.IGNORECASE)`.
Handle an empty `words` list first, or the pattern would match every word boundary.
</details>
