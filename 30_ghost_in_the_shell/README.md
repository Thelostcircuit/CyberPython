# 30 // GHOST IN THE SHELL

```
[MONTY] introspection mode ── sys.modules: 412 ── gc objects: 184,220 ── /core/first_light: still locked
```

**Modules:** `sys`, `inspect`, `gc`, `importlib.*`, `pkgutil`, `runpy`, `zipimport`, `modulefinder`, `site`, `sysconfig`, `ctypes`, `code`, `codeop`, `venv`, `ensurepip`, `pydoc`

MONTY turns the deck's full attention inward. It lists every module it has loaded, every
object in memory, every frame on the call stack, every file its import system has ever
touched. Somewhere in all that is the place Iris hid the key to `first_light`.

> **MONTY:** Python is unusually honest about itself. You can ask any object what it is, what
> it contains, and where it came from. You can see the stack of calls that got you here. You
> can import code from anywhere: files, zips, strings. And, with `ctypes`, you can call straight
> into C. Most programs never need this. Debuggers, test runners, plugin systems and
> frameworks live on it.

---

## ▓ TECH BRIEFING

### `sys`: the interpreter itself

```python
import sys
sys.version_info            # (major=3, minor=14, ...)  compare: sys.version_info >= (3, 14)
sys.platform, sys.executable, sys.argv, sys.path, sys.modules, sys.prefix, sys.base_prefix
sys.getsizeof(obj)          # shallow size in bytes
sys.getrecursionlimit(), sys.setrecursionlimit(n)
sys.stdin, sys.stdout, sys.stderr, sys.exit(code)
sys.exc_info(), sys.exception()             # the exception currently being handled
sys.intern(s), sys.getrefcount(obj), sys.flags, sys.implementation.name
sys._is_gil_enabled()       # False on a free-threaded build
sys.monitoring              # low-overhead event hooks for debuggers/profilers/coverage (3.12+)
```

A venv is active when `sys.prefix != sys.base_prefix`.

### `inspect`: look inside live objects

```python
import inspect
inspect.signature(func).parameters     # name → Parameter(kind, default, annotation)
inspect.getsource(func), inspect.getfile(obj), inspect.getdoc(obj)
inspect.getmembers(module, inspect.isfunction)
inspect.isclass / isfunction / ismethod / iscoroutinefunction / isgeneratorfunction
inspect.currentframe().f_back.f_code.co_name   # who called me?
inspect.stack()                                 # the whole call stack (slow)
```

### `gc`

Reference counting frees most objects instantly. The cycle collector cleans up objects that
point at each other:

```python
import gc
gc.collect()               # run a full collection now; returns how many unreachable objects it found
gc.get_count(), gc.disable(), gc.freeze(), gc.get_referrers(obj), gc.is_tracked(obj)
```

### The import system: `importlib` and friends

```python
import importlib, importlib.util
importlib.import_module("json.decoder")
importlib.reload(module)
spec = importlib.util.spec_from_file_location("drop", "/drops/tool.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)    # import ANY file

from importlib import resources, metadata
resources.files("mypackage").joinpath("data.txt").read_text()   # data files shipped in a package
metadata.version("requests"); metadata.distributions()          # installed-package info
```

`importlib.abc` and `importlib.machinery` let you write your own finders and loaders.
Related modules:
- `pkgutil.iter_modules(path)`: list the modules in a package.
- `runpy.run_path(path)` / `runpy.run_module(name)`: what `python file.py` / `python -m` do.
- `zipimport`: import straight from `.zip` files on `sys.path` (it's how `.pyz` apps work).
- `modulefinder.ModuleFinder`: work out which modules a script imports.
- `site`: sets up `site-packages` at startup (`python -m site` shows the paths).
- `sysconfig.get_paths()`, `sysconfig.get_config_var(...)`: where things are installed, and
  how Python was built.

### `ctypes`: calling C

```python
import ctypes, ctypes.util
libc = ctypes.CDLL(ctypes.util.find_library("c"))   # Unix
libc.abs(-5)                                        # 5
class Header(ctypes.Structure):
    _fields_ = [("magic", ctypes.c_char * 4), ("version", ctypes.c_uint8), ("length", ctypes.c_uint32)]
ctypes.sizeof(Header)       # 12: C alignment pads the struct
ctypes.create_string_buffer(16), ctypes.byref(x), ctypes.POINTER(ctypes.c_int)
```

`ctypes` can crash the interpreter if you get a signature wrong, so be careful with it.

### `code` and `codeop`: build your own REPL

```python
import code, codeop
codeop.compile_command("if x:")      # None: incomplete, the REPL shows "..." and waits for more
codeop.compile_command("x = 1")      # a code object: complete
code.interact(local={"deck": deck})  # drop into an interactive console in your program
```

### Environments and docs: `venv`, `ensurepip`, `pydoc`

```python
import venv
venv.create("/tmp/env", with_pip=False)   # what `python -m venv` does (uv does it faster)
# ensurepip bootstraps pip into an environment:  python -m ensurepip
import pydoc
pydoc.render_doc(len, renderer=pydoc.plaintext)   # what help() shows; `python -m pydoc -b` browses
```

(`pydoc_data` holds the topic text `help()` uses.)

---

## ▓ THE JOB

In `job.py`:

1. **`runtime_facts()`**: a few facts from `sys`.
2. **`in_venv()`**: whether this interpreter is running in a virtual environment.
3. **`who_called()`**: the name of the function that called *the function that called this one*.
4. **`params(func)`**: `[(name, kind, default)]` from `inspect.signature`.
5. **`own_functions(module)`**: the names of functions *defined in* that module (not imported ones).
6. **`cycle_is_collected()`**: build a reference cycle, drop it, and prove `gc` frees it (with a `weakref` witness).
7. **`load_file(name, path)`**: import a module from any file path.
8. **`submodules(package)`**: `pkgutil`.
9. **`run_and_get(path, var)`**: `runpy.run_path` and read one of the resulting globals.
10. **`import_from_zip(zip_path, module)`**: import a module that lives inside a zip.
11. **`package_data(package, name)`**: `importlib.resources`.
12. **`installed_version(dist)`**: `importlib.metadata`, or `None`.
13. **`Header`**: a `ctypes.Structure`, and **`c_abs(n)`**: call libc's `abs`.
14. **`is_complete(source)`**: `codeop`.
15. **`fresh_venv(path)`**: create a venv, and return the path of its Python.
16. **`doc_text(obj)`**: `pydoc` plain-text help.
