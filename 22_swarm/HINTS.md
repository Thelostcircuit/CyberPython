# HINTS // 22 SWARM

## SafeCounter / hammer
<details><summary>Hint</summary>

`self._lock = threading.Lock()` in `__init__`, and `with self._lock: self.value += 1`.
In `hammer`, make the threads, `start()` them all, then `join()` them all.
</details>

## fan_out
<details><summary>Hint</summary>

`ex.map(lambda f: f(), funcs)` keeps the input order. Wrap it in `list()` while the pool is
still open.
</details>

## fastest
<details><summary>Hint</summary>

`done, pending = wait(futures, return_when=FIRST_COMPLETED)`, then
`next(iter(done)).result()`. Call `ex.shutdown(wait=False, cancel_futures=True)` in a
`finally`. A `with` block would wait for the slow one.
</details>

## pipeline
<details><summary>Hint</summary>

The worker loop: `while (item := inbox.get()) is not None: outbox.put(item * 2)`.
One `None` per worker, after all the real items.
</details>

## delayed_signal
<details><summary>Hint</summary>

`event = threading.Event(); threading.Timer(delay, event.set).start(); return event`
</details>

## count_primes
<details><summary>Hint</summary>

`with ProcessPoolExecutor() as ex: return sum(ex.map(is_prime, numbers))`. Booleans sum as
0 and 1. `is_prime` has to be defined at module level so the child processes can import it.
</details>

## shm_roundtrip
<details><summary>Hint</summary>

`owner = shared_memory.SharedMemory(create=True, size=len(data))`,
`owner.buf[:len(data)] = data`, then `other = shared_memory.SharedMemory(name=owner.name)`.
Copy the bytes out with `bytes(other.buf[:len(data)])` *before* closing. Close both, then
`owner.unlink()`.
</details>

## in_subinterpreter
<details><summary>Hint</summary>

`interp = interpreters.create()`, then `try: return interp.call(func, *args)` with
`finally: interp.close()`.
</details>

## with_run_id
<details><summary>Hint</summary>

Define `inner()` that does `RUN_ID.set(run)` and returns `func()`, then
`copy_context().run(inner)`.
</details>
