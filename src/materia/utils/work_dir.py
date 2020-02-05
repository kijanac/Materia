from __future__ import annotations
import contextlib
import materia as mtr
import os
import pathlib
import tempfile
from typing import Optional

__all__ = ["mkdir", "work_dir"]


def mkdir(dir: str) -> None:
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass


@contextlib.contextmanager
def work_dir(dir: Optional[str] = None):
    # FIXME: learn how to type annotation yields
    with contextlib.nullcontext(
        mtr.expand(dir)
    ) if dir is not None else tempfile.TemporaryDirectory(dir=dir) as wd:
        try:
            mkdir(dir=wd)
            yield wd
        finally:
            pass
