# HINTS // 38 ID FORGE

## Badge fields
<details><summary>Hint</summary>

```python
badge_id: str = Field(pattern=r"^OS-[A-Z]{3}-\d{4}$")
name: str = Field(min_length=1)
clearance: int = Field(ge=1, le=7)
wings: list[str] = Field(default_factory=list)
issued: date
expires: date
```
</details>

## Validators
<details><summary>Hint</summary>

`@field_validator("wings")` on top of `@classmethod`, which gets `(cls, v)` and returns the new
value. `@model_validator(mode="after")` gets `self` (already validated) and must `return self`.
</details>

## is_admin
<details><summary>Hint</summary>

`@computed_field` stacked on `@property`, returning `self.clearance >= 6`.
</details>

## check
<details><summary>Hint</summary>

Catch `ValidationError as e`. Each item in `e.errors()` has a `"loc"` tuple, which is empty
for model-level errors. Build a set, then sort it.
</details>

## public_json / load_json
<details><summary>Hint</summary>

`badge.model_dump_json(exclude={"name"})` and `Badge.model_validate_json(text)`.
</details>

## Visit
<details><summary>Hint</summary>

`model_config = ConfigDict(extra="forbid", frozen=True)`. Declare `badge: Badge` and pydantic
validates the nested dict for you. `purpose: Literal["maintenance", "audit", "delivery"]`.
</details>

## ports / required_fields
<details><summary>Hint</summary>

`TypeAdapter(list[Port]).validate_python(values)`, and
`sorted(model.model_json_schema().get("required", []))`.
</details>
