from __future__ import annotations
import pathlib
from typing import Optional

__all__ = ["expand"]


def expand(path: str, dir: Optional[str] = None) -> str:
    p = pathlib.Path(path).expanduser()
    if dir is not None:
        p = pathlib.Path(dir).joinpath(p)
    return str(p.expanduser().resolve())
