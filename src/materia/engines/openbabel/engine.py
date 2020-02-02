from __future__ import annotations
import contextlib
import os
import materia
import subprocess
import tempfile
from typing import Iterable, Optional

__all__ = ["OpenbabelEngine"]


class OpenbabelEngine:
    def __init__(
        self,
        log: Optional[str] = "openbabel.log",
        executable: Optional[str] = "obabel",
        work_dir: Optional[str] = ".",
        cleanup: Optional[bool] = False,
    ) -> None:

        self.executable = executable
        self.work_dir = materia.utils.expand_path(work_dir)

        self.log = os.path.join(work_dir, log)

        self.cleanup = cleanup

    def execute(
        self,
        structure_file: str,
        output_file: Optional[str] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> str:
        with tempfile.TemporaryDirectory(
            dir=self.work_dir
        ) if self.cleanup else contextlib.nullcontext(self.work_dir) as wd:
            try:
                os.makedirs(wd)
            except FileExistsError:
                pass

            with open(self.log, "w") as log:
                subprocess.call(
                    [self.executable, structure_file],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    cwd=wd,
                )

            with open(self.log, "r") as log:
                return "".join(log.readlines())
