from __future__ import annotations
import os

__all__ = ["expand_path"]  # FIXME: change to simply 'expand'


def expand_path(path: str) -> str:  # FIXME: change to simply 'expand'
    return os.path.abspath(os.path.expanduser(path))
