from typing import TypeVar

T = TypeVar("T")


def Optional_or(value: T | None, default: T) -> T:
    return value if value is not None else default
