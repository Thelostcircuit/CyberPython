"""41 // FAST LANE: the holding server's transfer API, in FastAPI.

  Transfer (pydantic model):
      subject_id: str matching ^OS-[A-Z]{3}-\\d{4}$
      rack: str matching ^[A-Z]-\\d+$
      priority: int from 1 to 5, default 3

  require_token dependency: reads header X-Token; anything but TOKEN -> 401 {"detail": "bad token"}

  GET    /health                  -> {"ok": true, "transfers": <count>}
  POST   /transfers               -> requires the token. Body: Transfer.
                                     subject_id already stored -> 409 {"detail": "duplicate"}
                                     else store it, add a BACKGROUND task that appends
                                     f"transfer {subject_id}" to AUDIT, and return 201 with the
                                     transfer as JSON.
  GET    /transfers/{subject_id}  -> the transfer, or 404 {"detail": "not found"}
  GET    /transfers?wing=C&limit=N-> {"transfers": [...]} sorted by (priority, subject_id);
                                     wing filters on rack's first letter; limit is 1..100
                                     (default 50; out of range -> 422)
  DELETE /transfers/{subject_id}  -> requires the token; 204 with no body, or 404
  All handlers are `async def`.
"""

from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Query, Response
from pydantic import BaseModel, Field

TOKEN = "k-4471"
STORE: dict[str, "Transfer"] = {}
AUDIT: list[str] = []

app = FastAPI(title="Holding Server")


def reset() -> None:
    STORE.clear()
    AUDIT.clear()


# TODO: the Transfer model, require_token, and the routes
