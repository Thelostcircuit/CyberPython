# HINTS // 31 CODE FORGE

## token_pairs / comments
<details><summary>Hint</summary>

`tokenize.generate_tokens(io.StringIO(source).readline)` yields tokens with `.type` and
`.string`. `token.tok_name[t.type]` gives the name. Filter on `t.type in WANTED`, or on
`t.type == token.COMMENT`.
</details>

## names_used / function_names
<details><summary>Hint</summary>

`ast.walk(ast.parse(source))` visits every node. Collect `n.id` from `ast.Name` nodes into a
set. For functions, collect the `FunctionDef`/`AsyncFunctionDef` nodes, then sort them by
`(lineno, col_offset)`.
</details>

## read_literal
<details><summary>Hint</summary>

`ast.literal_eval` raises `ValueError` for non-literals like names and calls, and
`SyntaxError` for broken text. Catch the `SyntaxError` and re-raise it as `ValueError`.
</details>

## ConstantFolder
<details><summary>Hint 1</summary>

In `visit_BinOp`, call `self.generic_visit(node)` **first**. That folds the children, so
`(1 + 2) * (10 - 4)` becomes `3 * 6` before you look at it.
</details>
<details><summary>Hint 2</summary>

Use a dict from op type to function: `{ast.Add: lambda a, b: a + b, ...}`. Check
`type(c.value) in (int, float)`, which excludes `bool` because `type(True)` is `bool`.
Return `ast.Constant(result)`, or the node unchanged.
</details>

## rename
<details><summary>Hint</summary>

Define a `NodeTransformer` subclass *inside* the function with `visit_Name`, which changes
`node.id` and returns the node.
</details>

## count_opcode / function_locals
<details><summary>Hint</summary>

Look the name up in `opcode.opmap` first, so unknown names raise `KeyError`. For symtable:
loop over `top.get_children()` and match `child.get_type() == symtable.SymbolTableType.FUNCTION`
and the name. (In 3.14 the module table also has an `__annotate__` child, so check the type.)
</details>

## outline / build_pyc / build_tree / tab_trouble
<details><summary>Hint</summary>

`pyclbr.readmodule_ex(module, path=[str(directory)])` returns `{name: Class-or-Function}`.
`py_compile.compile(str(path), doraise=True)` returns the pyc path.
`compileall.compile_dir(...)` returns a truthy success value. Capture `tabnanny.check` with
`contextlib.redirect_stdout`.
</details>
