# 22 // SWARM

```
[PYTHIA-9] gap duration: 540 s ── sequential plan: 1,310 s ── verdict: IMPOSSIBLE (sequentially)
```

**Modules:** `threading`, `queue`, `concurrent.futures`, `multiprocessing`, `concurrent.interpreters`, `contextvars`, `sched`, `_thread`

Laid end to end, the plan takes twenty-two minutes. The gap lasts nine. The only way through
is to run things **at the same time**: a swarm of workers, each doing one job, all reporting
back to MONTY.

> **MONTY:** Python gives you three kinds of "at the same time", and choosing the right one
> matters. **Threads** share memory and are cheap. They're perfect when you're mostly
> *waiting*, on networks, disks or timers. **Processes** each get their own interpreter and
> memory, so they're the choice for heavy *computation*. And, new in 3.14, **subinterpreters**:
> several isolated interpreters inside one process.
>
> And whenever two workers touch the same data, you need a **lock**, or you'll get garbage.

---

## ▓ TECH BRIEFING

### `threading`

```python
import threading
t = threading.Thread(target=work, args=(1,), daemon=True)
t.start(); t.join(timeout=5)
threading.current_thread().name, threading.active_count()

lock = threading.Lock()                 # only one thread inside at a time
with lock:
    counter += 1                         # `x += 1` is NOT atomic: read, add, write
threading.RLock()                        # re-entrant: the same thread may acquire it again
threading.Event()                        # .set() / .wait() / .is_set(): a one-shot signal
threading.Condition(), threading.Semaphore(3), threading.Barrier(4)
threading.Timer(2.0, fn).start()         # run fn once after a delay
threading.local()                        # per-thread attribute storage
```

On standard CPython builds the **GIL** lets only one thread run Python bytecode at a time.
Threads speed up waiting, not arithmetic. The free-threaded build (`python3.14t`) removes the
GIL, but locks are still needed for correctness either way. `_thread` is the low-level
module `threading` is built on.

### `queue`: thread-safe hand-offs

```python
import queue
q = queue.Queue(maxsize=100)     # FIFO;  also LifoQueue, PriorityQueue, SimpleQueue
q.put(item); q.get(); q.task_done(); q.join()
q.get(timeout=1)                 # raises queue.Empty
q.shutdown()                     # 3.13+: wake everyone and stop the queue
```

Producer/consumer with a **sentinel**: put one `None` per worker to tell them to stop.

### `concurrent.futures`: the high-level API

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait, FIRST_COMPLETED

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch, urls))          # results come back in INPUT order
    futures = [ex.submit(fetch, u) for u in urls]
    for f in as_completed(futures):             # results in COMPLETION order
        f.result()                               # re-raises the worker's exception here
    done, pending = wait(futures, return_when=FIRST_COMPLETED)

with ProcessPoolExecutor() as ex:                # same API, separate processes
    ex.map(crunch, chunks)                       # functions and args must be picklable (module-level)
```

`InterpreterPoolExecutor` (3.14) is the same API again, but running on subinterpreters.

### `multiprocessing`

```python
import multiprocessing as mp
p = mp.Process(target=work, args=(1,)); p.start(); p.join()
with mp.Pool(4) as pool: pool.map(crunch, data)
mp.Queue(), mp.Pipe(), mp.Value("i", 0), mp.Array("d", 10), mp.Manager()
mp.get_start_method()            # "forkserver" is the default on Linux from 3.14, "spawn" on macOS/Windows
```

Scripts that start processes need the `if __name__ == "__main__":` guard, because children
re-import your main module.

`multiprocessing.shared_memory.SharedMemory(create=True, size=n)` gives several processes the
same block of bytes (`.buf` is a memoryview, `.name` lets another process attach). Always
`close()` it, and `unlink()` it once, in the creator.

### `concurrent.interpreters` (3.14)

```python
from concurrent import interpreters
interp = interpreters.create()
interp.call(pow, 2, 10)          # 1024, run inside the isolated interpreter
interp.exec("x = 1 + 1")
interpreters.create_queue()      # pass data between interpreters
interp.close()
```

Each interpreter has its own modules and globals, and (on 3.14) its own GIL, so they can run
Python code truly in parallel inside one process.

### `contextvars`

Like thread-locals, but they also work correctly with `asyncio` tasks:

```python
from contextvars import ContextVar, copy_context
run_id: ContextVar[str] = ContextVar("run_id", default="-")
token = run_id.set("gap-22"); ...; run_id.reset(token)
copy_context().run(func)         # run func in a COPY: its changes don't leak out
```

### `sched`

```python
import sched, time
s = sched.scheduler(time.monotonic, time.sleep)
s.enter(0.2, 1, action, argument=("b",))     # delay, priority, callable
s.enter(0.1, 1, action, argument=("a",))
s.run()                                       # runs them in time order
s.enterabs(t, priority, action)               # absolute time; priority breaks ties at the SAME t
```

---

## ▓ THE JOB

In `job.py`:

1. **`SafeCounter`** with a `Lock`, and **`hammer(counter, threads, per_thread)`** to bash it from many threads.
2. **`fan_out(funcs)`**: run zero-argument callables on a thread pool, with results in input order.
3. **`fastest(funcs)`**: the result of whichever callable finishes first.
4. **`pipeline(items, workers)`**: a `queue.Queue` producer/consumer with sentinels. Each worker doubles the items. Return the results sorted.
5. **`delayed_signal(delay)`**: a `threading.Event` that a `Timer` sets after `delay` seconds.
6. **`count_primes(numbers)`**: count the primes using a `ProcessPoolExecutor` and the module-level `is_prime`.
7. **`shm_roundtrip(data)`**: write bytes into shared memory, attach to it *by name*, read them back, and clean up.
8. **`in_subinterpreter(func, *args)`**: call a function inside a fresh subinterpreter.
9. **`with_run_id(run, func)`**: run `func` in a copied context with `RUN_ID` set, so nothing leaks.
10. **`run_schedule(events)`**: schedule `(delay, priority, name)` events with `sched` and return the order they fired in.
