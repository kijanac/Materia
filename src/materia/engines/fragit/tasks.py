from __future__ import annotations
from typing import Iterable, Optional, Tuple, Union

import contextlib
import materia

# FIXME: replace os with pathlib
import os
import re
import tempfile
import uuid

from ...workflow.tasks import ExternalTask

__all__ = ["FragItFragmentStructure"]


class FragItFragmentStructure(ExternalTask):
    """
    Task to fragment a structure using FragIt.

    Attributes:
        engine (materia.FragItEngine): Engine which will be used to fragment structure.
    """

    def run(
        self, structure: Union[str, materia.Structure]
    ) -> Tuple[str, Iterable[materia.Structure]]:
        with self.io() as io:
            if isinstance(structure, str):
                filepath = materia.expand(structure)
            else:
                while isinstance(structure, materia.Structure):
                    filepath = materia.expand(
                        os.path.join(io.work_dir, f"{uuid.uuid4().hex}.xyz")
                    )
                    try:
                        structure.write(filepath)
                        break
                    except FileExistsError:
                        continue

            self.engine.execute(
                structure_filepath=filepath, log_filepath=io.out, work_dir=io.work_dir,
            )

            name, _ = os.path.splitext(os.path.basename(filepath))
            pat = re.compile(rf"(?P<file_name>{name}_fragment_\d*\.xyz)")
            matches = (pat.match(s) for s in os.listdir(io.work_dir))

            return tuple(
                materia.Structure.read(os.path.join(io.work_dir, m.group("file_name")))
                for m in matches
                if m is not None
            )
