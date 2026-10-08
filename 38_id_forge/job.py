"""38 // ID FORGE: a replica of the intake dock's validator, built with pydantic v2."""

from datetime import date, datetime
from typing import Annotated, Any, Literal

from pydantic import (BaseModel, ConfigDict, Field, TypeAdapter, ValidationError,
                      computed_field, field_validator, model_validator)


class Badge(BaseModel):
    """Fields:
      badge_id: str matching ^OS-[A-Z]{3}-\\d{4}$
      name: str, at least 1 character
      clearance: int from 1 to 7 inclusive
      wings: list[str], default empty (a fresh list per badge). A field_validator upper-cases
             each entry and raises ValueError if any entry isn't exactly one character.
      issued: date
      expires: date. A model_validator (mode="after") raises ValueError unless expires > issued.
    Computed field:
      is_admin: bool, True when clearance >= 6 (appears in model_dump()).
    """

    pass  # TODO: fields, validators, computed field


def check(data: dict[str, Any]) -> Badge | list[str]:
    """Badge.model_validate(data). On ValidationError return the sorted, de-duplicated list of
    the FIRST element of each error's "loc" (errors from the model validator have an empty loc:
    report those as "__model__")."""
    raise NotImplementedError("TODO")


def public_json(badge: Badge) -> str:
    """model_dump_json without the "name" field."""
    raise NotImplementedError("TODO")


def load_json(text: str) -> Badge:
    """Validate directly from JSON text."""
    raise NotImplementedError("TODO")


# Visit: extra fields forbidden, frozen. Fields: badge: Badge, purpose: one of
# "maintenance" / "audit" / "delivery", at: datetime.
Visit = None  # TODO


Port = Annotated[int, Field(ge=1, le=65535)]


def ports(values: list[Any]) -> list[int]:
    """Validate with TypeAdapter(list[Port]); ValidationError propagates."""
    raise NotImplementedError("TODO")


def required_fields(model: type[BaseModel]) -> list[str]:
    """Sorted "required" names from model.model_json_schema()."""
    raise NotImplementedError("TODO")
