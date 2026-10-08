# HINTS // 15 DEAD DROP

## write_note
<details><summary>Hint</summary>

`folder = Path(folder)` first, so strings work too. Then `folder.mkdir(parents=True,
exist_ok=True)` and `(folder / name).write_text(text, encoding="utf-8")`.
</details>

## find
<details><summary>Hint</summary>

`root.rglob(pattern)` recurses. Keep `p.is_file()` hits and turn each into
`p.relative_to(root).as_posix()`. Sort at the end.
</details>

## tree_size
<details><summary>Hint</summary>

`for dirpath, dirnames, filenames in os.walk(root):` then add up
`os.path.getsize(os.path.join(dirpath, name))`.
</details>

## compare_dirs
<details><summary>Hint</summary>

`d = filecmp.dircmp(a, b)` has the attributes `left_only`, `right_only` and `diff_files`.
</details>

## lock_down
<details><summary>Hint</summary>

`os.chmod(path, 0o600)` (or `stat.S_IRUSR | stat.S_IWUSR`), then
`stat.filemode(os.stat(path).st_mode)`.
</details>

## scratch_roundtrip
<details><summary>Hint</summary>

Keep the directory name from `with tempfile.TemporaryDirectory() as tmp:`, and check
`Path(tmp).exists()` *after* the `with` block ends.
</details>

## stitched
<details><summary>Hint</summary>

```python
with fileinput.input(files=[...], encoding="utf-8") as stream:
    for line in stream:
        stream.filename(), stream.filelineno()
```
</details>

## upper_stream
<details><summary>Hint</summary>

Write into `out = io.StringIO()`, then `out.seek(0)` before returning, or the reader
starts at the end.
</details>

## windows_parts
<details><summary>Hint</summary>

`p = PureWindowsPath(path)`, then `p.drive`, `p.parent.name`, `p.stem`, `p.suffix`.
</details>
