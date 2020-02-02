from __future__ import annotations
import contextlib
import numpy as np
import os
import materia
import subprocess
import tempfile
from typing import Iterable, Optional, Tuple, Union
from ...workflow.tasks.task import Task
import uuid

__all__ = ["PackmolSolvate"]


# class PackShells(Task):
#     def __init__(
#         self,
#         structure: Union[materia.Structure, str],
#         shells: int,
#         tolerance: float,
#         number_density: Optional[materia.Qty] = None,
#         mass_density: Optional[materia.Qty] = None,
#         input_name: str = "packmol.inp",
#         output_name: str = "packmol.out",
#         executable: str = "packmol",
#         work_dir: str = ".",
#         handlers=None,
#     ) -> None:
#         super().__init__(handlers=handlers)

#         self.structure = (
#             materia.Structure.read(
#                 materia.utils.expand_path(os.path.join(work_dir, input_name))
#             )
#             if isinstance(structure, str)
#             else structure
#         )
#         self.shells = shells
#         self.number_density = number_density
#         self.mass_density = mass_density

#         self.tolerance = tolerance

#         self.input_path = materia.utils.expand_path(
#             os.path.join(work_dir, input_name)
#         )
#         self.output_path = materia.utils.expand_path(
#             os.path.join(work_dir, output_name)
#         )

#         self.executable = executable
#         self.work_dir = materia.utils.expand_path(work_dir)

#         try:
#             os.makedirs(self.work_dir)
#         except FileExistsError:
#             pass

#     def run(self):
#         if self.number_density is None:
#             if self.mass_density is None:
#                 raise ValueError(
#                     "Either mass density or number density required to pack shells."
#                 )

#             number_density = self.mass_density / self.structure.mass
#         else:
#             number_density = self.number_density

#         ideal_gas_separation = (2 * np.pi * number_density) ** (-1 / 3)
#         sphere_radius = self.shells * ideal_gas_separation
#         n = int(
#             ((4 * np.pi / 3) * number_density * sphere_radius ** 3).convert(1).value
#         )
#         structures = (self.structure, self.structure)
#         numbers = (1, n - 1)
#         structure_instructions = (
#             ["fixed 0. 0. 0. 0. 0. 0."],
#             [f"inside sphere 0. 0. 0. {sphere_radius.convert(materia.angstrom).value}"],
#         )

#         with tempfile.TemporaryDirectory(dir=self.work_dir) as tmpdir:
#             output_file_name = materia.utils.expand_path(os.path.join(tmpdir, "packed"))
#             materia.PackmolInput(
#                 tolerance=self.tolerance,
#                 filetype="xyz",
#                 output_name=output_file_name,
#                 structures=structures,
#                 numbers=numbers,
#                 structure_instructions=structure_instructions,
#             ).write(self.input_path)
#             # materia.ExecutePackmol(input_name=self.input_path)
#             with open(self.input_path, "r") as f_in:
#                 with open(self.output_path, "w") as f_out:
#                     subprocess.call([self.executable], stdin=f_in, stdout=f_out)

#             return materia.Structure.read(output_file_name + ".xyz")


class PackmolSolvate(Task):
    def __init__(
        self,
        solute: Union[materia.Structure, str],
        solvent: Union[materia.Structure, str],
        shells: int,
        tolerance: float,
        engine: materia.FragItEngine,
        number_density: Optional[materia.Qty] = None,
        mass_density: Optional[materia.Qty] = None,
        input_name: str = "packmol.inp",
        log_name: str = "packmol.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)

        self.solute = (
            materia.Structure.read(solute) if isinstance(solute, str) else solute
        )

        self.solvent = (
            materia.Structure.read(solvent) if isinstance(solvent, str) else solvent
        )

        self.shells = shells
        self.number_density = number_density
        self.mass_density = mass_density

        self.tolerance = tolerance

        self.input_name = input_name
        self.log_name = log_name
        self.work_dir = materia.expand_path(work_dir)
        self.keep_logs = keep_logs

        self.engine = engine

    def _packing_params(self) -> Tuple[int, materia.Qty]:
        if self.number_density is None:
            if self.mass_density is None:
                raise ValueError(
                    "Either mass density or number density required to pack shells."
                )

            number_density = self.mass_density / self.solvent.mass
        else:
            number_density = self.number_density

        # these are the ideal gas packing values:
        n = int((2 / 3) * self.shells ** 3)
        sphere_radius = self.shells * (2 * np.pi * number_density) ** (-1 / 3)

        return n, sphere_radius

    def run(self) -> materia.Structure:
        n, sphere_radius = self._packing_params()

        with contextlib.nullcontext(
            self.work_dir
        ) if self.keep_logs else tempfile.TemporaryDirectory(dir=self.work_dir) as wd:
            try:
                os.makedirs(wd)
            except FileExistsError:
                pass

            inp = materia.PackmolInput(
                tolerance=self.tolerance,
                filetype="xyz",
                output_name=materia.expand_path(os.path.join(wd, "packed")),
            )

            while isinstance(self.solute, materia.Structure):
                filepath = materia.expand_path(
                    os.path.join(wd, f"{uuid.uuid4().hex}.xyz")
                )
                try:
                    self.solute.write(filepath)
                    inp.add_structure(
                        structure_filepath=filepath,
                        number=1,
                        instructions=["fixed 0. 0. 0. 0. 0. 0."],
                    )
                    break
                except FileExistsError:
                    continue

            while isinstance(self.solvent, materia.Structure):
                filepath = materia.expand_path(
                    os.path.join(wd, f"{uuid.uuid4().hex}.xyz")
                )
                try:
                    self.solvent.write(filepath)
                    inp.add_structure(
                        structure_filepath=filepath,
                        number=n - 1,
                        instructions=[
                            f"inside sphere 0. 0. 0. {sphere_radius.convert(materia.angstrom).value}"
                        ],
                    )
                    break
                except FileExistsError:
                    continue

            input_filepath = materia.expand_path(os.path.join(wd, self.input_name))

            inp.write(input_filepath)

            self.engine.execute(
                input_filepath=input_filepath,
                log_filepath=materia.expand_path(os.path.join(wd, self.log_name)),
            )

            return materia.Structure.read(
                materia.expand_path(os.path.join(wd, "packed.xyz"))
            )
