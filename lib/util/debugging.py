from typing import Any
import json
from pathlib import Path


def json_dump(obj: Any, name: str) -> None:
    with Path(f"{name}.dump").open("w") as fp:
        json.dump(obj, fp=fp)
