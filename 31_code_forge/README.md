# 31 // CODE FORGE

```
[MONTY] target: unlock (compiled, no source) ── bytecode: 214 instructions ── intent: UNKNOWN
```

**Modules:** `ast`, `dis`, `opcode`, `tokenize`, `token`, `keyword`, `symtable`, `pyclbr`, `py_compile`, `compileall`, `tabnanny`

Everything you've written has gone through the same forge. Source text is **tokenized** into
names, numbers and operators, the tokens are **parsed** into an abstract syntax tree, and
the tree is **compiled** into bytecode, which the interpreter runs one instruction at a time.
Python exposes every one of those stages.

> **MONTY:** Iris's `unlock` is bytecode, so we start at the bottom and read the instructions.
> But the forge runs both ways. With `ast` you can take code apart, *change* it, and put it
> back together. Linters, formatters, test frameworks and type checkers all work this way.
> You're about to learn how the tools you use are built.

---

## ▓ TECH BRIEFING

### `tokenize`, `token`, `keyword`

```python
import io, tokenize, token, keyword
for tok in tokenize.generate_tokens(io.StringIO("x = 1  # hi\n").readline):
    token.tok_name[tok.type], tok.string        # NAME 'x', OP '=', NUMBER '1', COMMENT '# hi', ...
keyword.iskeyword("for")      # True;  keyword.kwlist
keyword.issoftkeyword("match")   # True: only a keyword in some positions ('match', 'case', 'type', '_')
```

Tokenizing keeps comments and exact spelling, which the AST throws away.

### `ast`: the syntax tree

```python
import ast
tree = ast.parse("total = price * 2")
print(ast.dump(tree, indent=2))              # Module(body=[Assign(targets=[Name('total')], value=BinOp(...))])
for node in ast.walk(tree):                  # every node, any order
    if isinstance(node, ast.Name): node.id
ast.literal_eval("{'a': [1, 2]}")            # SAFE: only literals, never runs code (use instead of eval)
ast.unparse(tree)                            # back to source

class Doubler(ast.NodeTransformer):          # rewrite trees
    def visit_Constant(self, node):
        if isinstance(node.value, int):
            return ast.Constant(node.value * 2)
        return node
new = ast.fix_missing_locations(Doubler().visit(tree))
compile(new, "<forge>", "exec")              # a code object from a tree
```

`ast.NodeVisitor` walks without changing anything: define `visit_FunctionDef`,
`visit_Call`... and call `self.generic_visit(node)` to keep going deeper.

### `dis` and `opcode`: bytecode

```python
import dis
dis.dis(func)                                  # a human-readable listing
[i.opname for i in dis.get_instructions(func)] # ['RESUME', 'LOAD_FAST...', 'BINARY_OP', 'RETURN_VALUE']
func.__code__.co_varnames, co_consts, co_names

import opcode
opcode.opmap["RETURN_VALUE"], opcode.opname[n]
```

Bytecode is a CPython implementation detail. It changes between versions (3.14 has instructions
3.10 never had), so treat it as something to read, not something to depend on.

### `symtable`: scopes

```python
import symtable
top = symtable.symtable(source, "<src>", "exec")
for child in top.get_children():             # a table per function/class
    child.get_name(), child.get_type()
    child.get_locals()                        # for functions: parameters + assigned names
    child.lookup("x").is_global()
```

### Compiling files: `py_compile`, `compileall`

```python
import py_compile, compileall
py_compile.compile("tool.py", doraise=True)   # → __pycache__/tool.cpython-314.pyc
compileall.compile_dir("pkg/", quiet=1)       # a whole tree (what installers do)
```

### `pyclbr` and `tabnanny`

```python
import pyclbr
pyclbr.readmodule_ex("tool", path=["dir"])    # classes and functions WITHOUT importing (it reads the source)

import tabnanny
tabnanny.check("file.py")                     # reports ambiguous tab/space indentation
```

(The regex engine's `sre_*` internals were covered back in ch 09.)

---

## ▓ THE JOB

In `job.py`:

1. **`token_pairs(source)`**: `(type name, text)` for every NAME, OP, NUMBER and STRING token.
2. **`comments(source)`**: every comment's text.
3. **`reserved(word)`**: `"keyword"`, `"soft keyword"`, or `"no"`.
4. **`names_used(source)`**: every variable name read or written, sorted.
5. **`function_names(source)`**: every `def`, including nested ones, in source order.
6. **`read_literal(text)`**: parse a Python literal **safely**. Anything that isn't a literal raises `ValueError`.
7. **`fold_constants(source)`**: a `NodeTransformer` that pre-computes `+ - *` between two numeric constants, applied until nothing changes. Return the unparsed source.
8. **`rename(source, old, new)`**: rename a variable everywhere.
9. **`opnames(func)`** and **`count_opcode(func, name)`**: `dis`.
10. **`function_locals(source, func)`**: `symtable`.
11. **`outline(dir, module)`**: `pyclbr`, with no importing.
12. **`build_pyc(path)`** / **`build_tree(dir)`**: `py_compile` / `compileall`.
13. **`tab_trouble(path)`**: whether `tabnanny` complains about a file.
