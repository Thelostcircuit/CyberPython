# 41 // FAST LANE

```
[CHEESE SHOP] purchase: fastapi ── target: holding-server transfer API ── load at gap: 9,402 transfers / 120 s
```

**Package:** [`FastAPI`](https://fastapi.tiangolo.com/): modern, async, typed web APIs, built on pydantic (ch 38) and Starlette. (Tests use its `TestClient`, which runs on `httpx2`.)

The release program will hammer the holding server with transfer records, one per mind, as
fast as the Coil can emit them. Every record has to be validated, and duplicates refused. The
crew needs to query progress live, and every change must be audited. The Flask front door
isn't built for that.

> **WENSLEYDALE:** In FastAPI, sir, the **type hints are the API**. Declare that a route takes
> a `Transfer` model and a `limit: int` between 1 and 100, and FastAPI parses the JSON,
> validates it, converts the query string, rejects bad input with a proper 422 error, and
> writes interactive documentation, all from the annotations. And the handlers can be `async`.
>
> **MONTY:** Everything from ch 24 and ch 38, combined. Lovely.

---

## ▓ TECH BRIEFING

### Routes from type hints

```python
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, Path, Header, Depends, BackgroundTasks, status
from pydantic import BaseModel, Field

app = FastAPI(title="Holding Server")

class Transfer(BaseModel):
    subject_id: str = Field(pattern=r"^OS-[A-Z]{3}-\d{4}$")
    rack: str
    priority: int = Field(default=3, ge=1, le=5)

@app.get("/health")
async def health():                       # async def (or plain def, which runs in a thread pool)
    return {"ok": True}

@app.post("/transfers", status_code=201)
async def create(t: Transfer):            # a pydantic parameter = the JSON body, validated
    return t                              # returned models are serialised to JSON

@app.get("/transfers/{subject_id}")       # path parameter
async def get_one(subject_id: str):
    raise HTTPException(status_code=404, detail="not found")

@app.get("/transfers")
async def listing(wing: str | None = None,
                  limit: Annotated[int, Query(ge=1, le=100)] = 50):   # validated query params
    ...
```

Invalid input produces **422 Unprocessable Content**, with a JSON explanation of what failed.
`response_model=SomeModel` filters and documents what a route returns.

### Dependencies

`Depends` injects shared logic (auth, database sessions, settings) into any route:

```python
def require_token(x_token: Annotated[str | None, Header()] = None) -> str:   # reads the X-Token header
    if x_token != "k-4471":
        raise HTTPException(status_code=401, detail="bad token")
    return x_token

@app.delete("/transfers/{subject_id}", status_code=204, dependencies=[Depends(require_token)])
async def delete(subject_id: str): ...
```

### Background tasks, docs, testing

```python
@app.post("/transfers")
async def create(t: Transfer, background: BackgroundTasks):
    background.add_task(AUDIT.append, f"transfer {t.subject_id}")   # runs AFTER the response is sent

# interactive docs at /docs (Swagger UI) and /redoc; the schema at /openapi.json (app.openapi())

from fastapi.testclient import TestClient
client = TestClient(app)
client.post("/transfers", json={...}, headers={"X-Token": "k-4471"}).status_code
```

To serve it for real: `uv run fastapi dev job.py` (development), or an ASGI server such as
uvicorn.

---

## ▓ THE JOB

In `job.py`, build the module-level **`app`**. The routes and rules are in the docstring:
a `Transfer` model, `/health`, create (auth, 201, 409 on duplicates, background audit), fetch
(404), list (a wing filter plus a validated `limit`), delete (auth, 204), and a `require_token`
dependency. `reset()` clears the in-memory store between tests.
