# HINTS // 24 ASYNC UPRISING

## probe_all
<details><summary>Hint</summary>

`await asyncio.gather(*(probe(n, d) for n, d in delays))` returns a list in argument order.
</details>

## probe_within
<details><summary>Hint</summary>

```python
try:
    async with asyncio.timeout(limit):
        return await probe(name, delay)
except TimeoutError:
    return "TIMEOUT"
```
</details>

## sweep
<details><summary>Hint</summary>

Create the tasks inside `async with asyncio.TaskGroup() as tg:` and keep them in a dict. After
the block they're all finished, so read `task.result()`.
</details>

## first_answer
<details><summary>Hint 1</summary>

`asyncio.create_task(coro, name=n)` lets you get the name back later with `task.get_name()`.
</details>
<details><summary>Hint 2</summary>

After `wait(..., return_when=asyncio.FIRST_COMPLETED)`, cancel each pending task, then
`await asyncio.gather(*pending, return_exceptions=True)` so the cancellations actually finish.
</details>

## throttled
<details><summary>Hint</summary>

Use `nonlocal active, peak` inside the job. Update the counters *inside* `async with sem:`.
</details>

## relay
<details><summary>Hint</summary>

The consumer loop: `while (item := await q.get()) is not None: out.append(item.upper())`.
Run both with `asyncio.gather(producer(), consumer())`.
</details>

## ticks / collect
<details><summary>Hint</summary>

An async generator is an `async def` containing `yield`. Collect with `[x async for x in agen]`.
</details>

## echo_upper
<details><summary>Hint</summary>

The server's port is `server.sockets[0].getsockname()[1]`. Use `async with server:` so it
closes afterwards. Remember to `await writer.drain()` after writing, and to
`writer.close(); await writer.wait_closed()` on both ends.
</details>

## VaultSession
<details><summary>Hint</summary>

`async def __aenter__(self)` and `async def __aexit__(self, exc_type, exc, tb)`. Returning
`None` from `__aexit__` means "don't suppress".
</details>
