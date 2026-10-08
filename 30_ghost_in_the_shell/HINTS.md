# HINTS // 30 GHOST IN THE SHELL

## who_called
<details><summary>Hint</summary>

`inspect.currentframe()` is *your* frame. `.f_back` is whoever called you, and `.f_back.f_back`
is their caller. Read `.f_code.co_name`. (`del frame` in a `finally` avoids a reference
cycle.)
</details>

## params
<details><summary>Hint</summary>

`inspect.signature(func).parameters.values()` gives `Parameter` objects. `p.kind.name` is the
kind as a string, and `p.default is inspect.Parameter.empty` means there's no default.
</details>

## own_functions
<details><summary>Hint</summary>

`inspect.getmembers(module, inspect.isfunction)` gives `(name, func)` pairs. Keep those where
`func.__module__ == module.__name__`.
</details>

## cycle_is_collected
<details><summary>Hint</summary>

`witness = weakref.ref(a)`, then `del a, b`, then `gc.collect()`. A dead weakref returns `None`
when called.
</details>

## load_file
<details><summary>Hint</summary>

```python
spec = importlib.util.spec_from_file_location(name, path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```
</details>

## submodules / run_and_get
<details><summary>Hint</summary>

`pkgutil.iter_modules(importlib.import_module(package).__path__)` yields objects with a
`.name`. `runpy.run_path(str(path))` returns the script's globals dict.
</details>

## import_from_zip / package_data / installed_version
<details><summary>Hint</summary>

`sys.path.insert(0, str(zip_path))` inside `try`, and `sys.path.remove(...)` in `finally`.
`importlib.resources.files(package).joinpath(name).read_text()`. Catch
`importlib.metadata.PackageNotFoundError`.
</details>

## Header / c_abs
<details><summary>Hint</summary>

`class Header(ctypes.Structure): _fields_ = [("magic", ctypes.c_char * 4), ...]`.
`ctypes.CDLL(ctypes.util.find_library("c")).abs(n)`.
</details>

## is_complete / fresh_venv / doc_text
<details><summary>Hint</summary>

`codeop.compile_command(source) is not None`. `venv.create(path, with_pip=False)`, then build
the `bin/python` path. `pydoc.render_doc(obj, renderer=pydoc.plaintext)`.
</details>
