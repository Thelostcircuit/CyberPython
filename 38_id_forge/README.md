# 38 // ID FORGE

```
[CHEESE SHOP] purchase: pydantic ── target: intake-dock badge schema v9 ── tolerance for errors: ZERO
```

**Package:** [`pydantic`](https://docs.pydantic.dev/latest/): data validation and settings, driven by type hints.

R. Okonkwo can register the crew as a maintenance contractor visit. The dock will then check
every visitor record against its schema: badge IDs in the right format, clearance in range,
dates that make sense, no unexpected fields. A record that fails even one check locks the dock
down. So before anything goes to Okonkwo, MONTY wants a replica of the dock's validator, to
make sure every record passes *first time*.

> **WENSLEYDALE:** Pydantic takes the type hints you already know from ch 28 and *enforces* them,
> sir. It checks, converts ("7" becomes 7 where that's safe), and reports exactly what's wrong
> and where. FastAPI is built on it. So is half the configuration code in this city.
>
> **MONTY:** Dataclasses *describe* data. Pydantic *guards* it.

---

## ▓ TECH BRIEFING

### Models

```python
from datetime import date
from pydantic import BaseModel, Field, ValidationError

class Badge(BaseModel):
    badge_id: str = Field(pattern=r"^OS-[A-Z]{3}-\d{4}$")
    name: str = Field(min_length=1)
    clearance: int = Field(ge=1, le=7)
    wings: list[str] = Field(default_factory=list)
    issued: date

b = Badge(badge_id="OS-MNT-0311", name="R. Okonkwo", clearance="3", issued="2091-01-02")
b.clearance            # 3: the string was converted ("lax" mode)
b.issued               # datetime.date(2091, 1, 2)
```

### Validation errors

```python
try:
    Badge(badge_id="nope", name="", clearance=9, issued="soon")
except ValidationError as e:
    e.error_count()                            # 4
    [err["loc"] for err in e.errors()]         # [('badge_id',), ('name',), ('clearance',), ('issued',)]
    print(e)                                   # a readable report
```

### Custom validators and computed fields

```python
from pydantic import field_validator, model_validator, computed_field

class Badge(BaseModel):
    ...
    @field_validator("wings")
    @classmethod
    def upper_wings(cls, v: list[str]) -> list[str]:
        if any(len(w) != 1 for w in v):
            raise ValueError("wings are single letters")
        return [w.upper() for w in v]            # a validator can also TRANSFORM the value

    @model_validator(mode="after")
    def dates_in_order(self):
        if self.expires <= self.issued:
            raise ValueError("expires must be after issued")
        return self

    @computed_field
    @property
    def is_admin(self) -> bool:
        return self.clearance >= 6
```

### In and out

```python
Badge.model_validate({"badge_id": ...})       # from a dict
Badge.model_validate_json('{"badge_id": ...}')# from JSON text (fast: parsed in Rust)
b.model_dump()                                 # → dict (computed fields included)
b.model_dump(exclude={"name"}, mode="json")    # JSON-safe values (dates as strings)
b.model_dump_json()
b.model_copy(update={"clearance": 4})          # note: updates are NOT re-validated
Badge.model_json_schema()                      # a JSON Schema for the model
```

### Configuration, nesting, and bare types

```python
from typing import Annotated, Literal
from pydantic import ConfigDict, TypeAdapter

class Visit(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)   # unknown fields are errors; immutable
    badge: Badge                                            # nested models are validated too
    purpose: Literal["maintenance", "audit", "delivery"]

Port = Annotated[int, Field(ge=1, le=65535)]
TypeAdapter(list[Port]).validate_python(["80", 443])      # [80, 443]: validate non-model types
```

`strict=True` (on a field, or in `model_config`) turns off conversions. `pydantic-settings` (a
separate package) loads models from environment variables.

---

## ▓ THE JOB

In `job.py`, using **pydantic v2**:

1. **`Badge`**: the fields and rules in the docstring, including a field validator for `wings`, a model validator for the dates, and a computed `is_admin` field.
2. **`check(data)`**: return the `Badge`, or the sorted list of field names that failed.
3. **`public_json(badge)`**: JSON without the `name` field.
4. **`load_json(text)`**: validate straight from JSON text.
5. **`Visit`**: a frozen model that rejects extra fields, with a nested `Badge`, a `Literal` purpose and a `datetime`.
6. **`ports(values)`**: validate a list of ports with a `TypeAdapter`.
7. **`required_fields(model)`**: the sorted names of the required fields, from the JSON schema.
