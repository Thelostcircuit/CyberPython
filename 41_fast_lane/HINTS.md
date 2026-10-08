# HINTS // 41 FAST LANE

## Transfer
<details><summary>Hint</summary>

Just like ch 38: `subject_id: str = Field(pattern=...)`, `rack: str = Field(pattern=r"^[A-Z]-\d+$")`,
`priority: int = Field(default=3, ge=1, le=5)`.
</details>

## require_token
<details><summary>Hint</summary>

`def require_token(x_token: Annotated[str | None, Header()] = None)`. FastAPI maps the
parameter `x_token` to the `X-Token` header. Raise `HTTPException(status_code=401,
detail="bad token")`.
</details>

## create
<details><summary>Hint</summary>

`@app.post("/transfers", status_code=201, dependencies=[Depends(require_token)])` and
`async def create_transfer(transfer: Transfer, background: BackgroundTasks)`. Add the audit
entry with `background.add_task(AUDIT.append, f"transfer {transfer.subject_id}")`.
</details>

## list
<details><summary>Hint</summary>

`limit: Annotated[int, Query(ge=1, le=100)] = 50`. Sort with
`key=lambda t: (t.priority, t.subject_id)`. Returning pydantic models inside a dict works,
because FastAPI serialises them.
</details>

## delete
<details><summary>Hint</summary>

`STORE.pop(subject_id, None)` returns `None` if the id was missing, so raise 404 then.
Otherwise `return Response(status_code=204)` for an empty body.
</details>
