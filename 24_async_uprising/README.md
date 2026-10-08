# 24 // ASYNC UPRISING

```
[PYTHIA-9] Coil internal network: ~40,000 endpoints ── response times: 20–900 ms ── threads available: 1
```

**Modules:** `asyncio`

The Coil's internal network is enormous and slow: forty thousand endpoints, each taking a
fraction of a second to answer. During the gap you need to check hundreds of them: door
states, camera feeds, rack health, the release port. Threads won't scale that far. BASILISK
doesn't use threads.

> **MONTY:** Here's the trick. Most of a network program's time is spent *waiting*. With
> `async`/`await`, a single thread runs thousands of **coroutines**. Each one runs until it
> would wait (on the network, a timer, a queue) and then *yields* control, and the **event
> loop** runs something else. Nobody blocks. Everything stays responsive.
>
> The one rule: **never block the loop.** A single `time.sleep()` or slow computation inside a
> coroutine freezes *everything*.

---

## ▓ TECH BRIEFING

### Coroutines and the event loop

```python
import asyncio

async def probe(host: str) -> str:       # `async def` makes a coroutine function
    await asyncio.sleep(0.1)             # `await` = pause here, let others run
    return f"{host}: ok"

asyncio.run(probe("door-3"))             # start an event loop, run it, close it
```

Calling `probe("x")` doesn't run anything. It creates a coroutine object, which runs only when
awaited or wrapped in a task.

### Running things concurrently

```python
results = await asyncio.gather(probe("a"), probe("b"))    # concurrently; results in order

task = asyncio.create_task(probe("c"))   # schedule it now, await it later
await task

async with asyncio.TaskGroup() as tg:    # structured concurrency (3.11+)
    t1 = tg.create_task(probe("a"))
    t2 = tg.create_task(probe("b"))
# all tasks are done here; if one failed, the others were cancelled and you get an ExceptionGroup

done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for t in pending: t.cancel()             # cancellation raises CancelledError inside the task
for coro in asyncio.as_completed(aws): result = await coro
```

### Timeouts

```python
async with asyncio.timeout(2):           # raises TimeoutError if the block takes longer
    await slow()
await asyncio.wait_for(slow(), 2)        # the older spelling
```

### Synchronisation and queues

```python
sem = asyncio.Semaphore(10)              # at most 10 at once
async with sem: ...
lock, event = asyncio.Lock(), asyncio.Event()
q = asyncio.Queue(); await q.put(x); x = await q.get(); q.task_done(); await q.join()
```

### Async iteration and context managers

```python
async def ticks(n):                      # an ASYNC GENERATOR: yield inside async def
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async for t in ticks(3): ...
[t async for t in ticks(3)]              # async comprehension

class Session:
    async def __aenter__(self): ...; return self
    async def __aexit__(self, *exc): ...
async with Session() as s: ...
```

`aiter()` and `anext()` are the async versions of `iter()` and `next()`.

### Blocking code and threads

```python
await asyncio.to_thread(blocking_function, arg)   # run it in a worker thread, await the result
loop.run_in_executor(executor, func)              # the older, more general version
```

### Networking: streams

```python
server = await asyncio.start_server(handle, "127.0.0.1", 0)   # port 0 = pick a free one
port = server.sockets[0].getsockname()[1]

async def handle(reader, writer):
    data = await reader.readline()
    writer.write(data.upper()); await writer.drain()
    writer.close(); await writer.wait_closed()

reader, writer = await asyncio.open_connection("127.0.0.1", port)
```

There's more: subprocesses (`asyncio.create_subprocess_exec`), `asyncio.Runner`, debug mode
(`PYTHONASYNCIODEBUG=1`) and `python -m asyncio` (an async REPL). In 3.14, `python -m asyncio
ps PID` / `pstree PID` inspect a running program's tasks.

---

## ▓ THE JOB

In `job.py`, everything is `async` unless it says otherwise:

1. **`probe(name, delay)`**: sleep, then return `name`.
2. **`probe_all(delays)`**: probe every `(name, delay)` concurrently with `gather`, results in input order.
3. **`probe_within(name, delay, limit)`**: the result, or `"TIMEOUT"` (use `asyncio.timeout`).
4. **`sweep(targets)`**: a `TaskGroup` that probes everything and returns `{name: result}`.
5. **`first_answer(delays)`**: the first name to answer. Cancel the rest, and return the names that were cancelled too.
6. **`throttled(count, limit)`**: run `count` jobs, never more than `limit` at once (`Semaphore`). Return the peak concurrency you saw.
7. **`relay(items)`**: an `asyncio.Queue` with one producer and one consumer, where the consumer upper-cases the items.
8. **`ticks(n)`** (an async generator) and **`collect(agen)`**.
9. **`offload(func, *args)`**: run a blocking function via `to_thread`.
10. **`echo_upper(message)`**: start a local stream server that upper-cases one line, connect to it, and return the reply.
11. **`VaultSession`**: an async context manager that logs `"open"`/`"close"`.
