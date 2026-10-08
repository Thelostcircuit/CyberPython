# 08 // MONTY'S TOOLKIT

```
[PYTHIA-9] self-diagnostic ── MONTY core: OPEN ── builtins: 71 ── modules on disk: 300+
```

Back in the Adder's Nest after closing. Shutters down, the green neon snake buzzing outside.

> **MONTY:** Everything you've written so far has used my **built-ins**: the functions and
> types that are always there without importing anything. A good runner knows every one.
> After that come **modules**, files of Python you pull in with `import`.
>
> Iris used to say Python comes with **batteries included**. She wasn't exaggerating. Once you
> can open a toolbox, I'll start handing you the tools. All of them.

---

## ▓ TECH BRIEFING

### Every built-in function

They live in the `builtins` module, which is the "B" in LEGB. Don't shadow them
(`list = [1, 2]` breaks `list()` for the rest of that scope).

| Group | Built-ins |
|---|---|
| Types | `bool` `int` `float` `complex` `str` `bytes` `bytearray` `memoryview` `list` `tuple` `dict` `set` `frozenset` `range` `slice` `object` `type` |
| Numbers | `abs` `divmod` `pow` `round` `sum` `min` `max` |
| Text | `str` `repr` `ascii` `format` `chr` `ord` `bin` `oct` `hex` |
| Iteration | `iter` `next` `aiter` `anext` `enumerate` `zip` `map` `filter` `reversed` `sorted` `len` `all` `any` |
| Objects | `getattr` `setattr` `hasattr` `delattr` `dir` `vars` `id` `hash` `isinstance` `issubclass` `callable` `super` `property` `classmethod` `staticmethod` |
| Code and scopes | `globals` `locals` `compile` `eval` `exec` `__import__` |
| Interaction | `print` `input` `open` `help` `breakpoint` |

A few worth a closer look:

```python
pow(3, 200, 7)          # modular power, fast: 2
pow(3, -1, 7)           # modular inverse: 5
bin(10), oct(10), hex(255)      # '0b1010', '0o12', '0xff'
int("ff", 16), int("0b101", 0)  # 255, 5   (base 0 reads the prefix)
format(255, "08b")      # '11111111'
chr(65), ord("A")       # 'A', 65
ascii("café")           # "'caf\\xe9'"
id(x)                   # identity (the address, in CPython)
hash("abc")             # used by dicts/sets; str hashes change per process
vars(obj)               # obj.__dict__
dir(obj)                # every attribute name, including inherited ones
callable(len)           # True
getattr(obj, "name", None)
slice(1, 10, 2)         # what xs[1:10:2] builds under the hood
```

`eval`, `exec` and `compile` run Python source code from strings. Never feed them text you
didn't write yourself. Chapter 31's `ast.literal_eval` is the safe way to read literals.

### bytes, bytearray, memoryview

Text is `str` (Unicode). Raw data is `bytes`: an immutable sequence of ints 0–255.

```python
b = b"ICE\x00\xff"          # bytes literal
b[0]                        # 73  indexing gives an int
b[:3]                       # b'ICE'  slicing gives bytes
"café".encode("utf-8")      # b'caf\xc3\xa9'
b"caf\xc3\xa9".decode()     # 'café'
bytes([1, 2, 3])            # b'\x01\x02\x03'
bytes.fromhex("dead beef")  # b'\xde\xad\xbe\xef'
b"\xde\xad".hex()           # 'dead'
int.from_bytes(b"\x01\x00", "big")   # 256
(256).to_bytes(2, "little")          # b'\x00\x01'

buf = bytearray(b"hello")   # the MUTABLE version
buf[0] = ord("J")           # bytearray(b'Jello')

view = memoryview(buf)      # a zero-copy window onto another object's memory
view[1:3] = b"EL"           # writes straight into buf, no copying
```

### Modules and imports

A module is any `.py` file. Importing runs it once and caches it in `sys.modules`.

```python
import math                     # use as math.sqrt
import math as m                # alias
from math import sqrt, pi       # pull names in directly
from os import path as ospath
```

Python searches `sys.path` for modules: the script's folder first, then the standard library,
then `site-packages`.

A **package** is a folder of modules with an `__init__.py`:

```
crew/
    __init__.py          # runs on `import crew`; can re-export names
    roster.py            # import crew.roster  /  from crew.roster import members
    ranks.py             # inside the package: from .ranks import rank_of   (relative import)
```

`__all__ = ["members"]` in a module controls what `from module import *` exports.

To import a module whose name you only know at runtime, use `importlib.import_module("json")`
(more in ch 30).

### `__name__` and `__main__`

Every module has a `__name__`. When a file is run directly, its `__name__` is `"__main__"`;
when it's imported, it's the module's name. So:

```python
def main():
    ...

if __name__ == "__main__":      # only when run as a script, never on import
    main()
```

`python -m package.module` runs a module as a script. A package can have a `__main__.py` so
that `python -m package` works.

---

## ▓ THE JOB

In `job.py`:

1. **`radix_report(n)`**: `{"bin": ..., "oct": ..., "hex": ...}` using the built-ins.
2. **`rot(text, k)`**: rotate letters by `k` places with `ord`/`chr`, keeping case. Everything else stays put.
3. **`xor_bytes(data, key)`**: XOR each byte with the key, repeating the key as needed. Return `bytes`.
4. **`patch_in_place(buf, offset, patch)`**: overwrite part of a `bytearray` through a `memoryview`. Return the number of bytes written.
5. **`public_api(obj)`**: a dict of the public attribute names, each marked `"method"` or `"value"`.
6. **`dispatch(obj, command, *args)`**: call the method named `command`, or raise `AttributeError` with a clear message.
7. **`load_attr(spec)`**: `"math:sqrt"` → the real `math.sqrt` object, via `importlib`.
8. **`main()`**: print the deck banner. Add the `if __name__ == "__main__":` guard, so running the file prints it and importing it doesn't.
