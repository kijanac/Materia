from __future__ import annotations
from typing import Iterable, Optional, Union

import materia as mtr

from ...workflow.tasks import ExternalTask

__all__ = [
    "MultiwfnVolume"
]  # "ExecuteMultiwfn", "MultiwfnVolume", "WriteMultiwfnInput"]


class MultiwfnBaseTask(ExternalTask):
    def commands(self) -> Iterable[Union[str, int, float]]:
        raise NotImplementedError

    def parse(self, output: str) -> Any:
        raise NotImplementedError

    def run(self, filepath: str) -> Any:
        inp = mtr.MultiwfnInput(mtr.expand(filepath), *self.commands(), -10,)

        with self.io() as io:
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


# class ExecuteMultiwfn(Task):
#     def __init__(
#         self,
#         input_path: str,
#         engine: materia.MultiwfnEngine,
#         handlers: Optional[Iterable[materia.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = input_path
#         self.engine = engine

#     def run(self) -> None:
#         self.engine.execute(input_path=self.input_path)


class MultiwfnVolume(MultiwfnBaseTask):
    def commands(self):
        integration_mesh_exp = 9  #: int = 9,
        density_isosurface = 1e-3  #: float = 0.001,
        box_size_factor = 1.7  #: float = 1.7
        return (
            100,
            3,
            f"{integration_mesh_exp},{density_isosurface},{box_size_factor}",
            "0,0,0",
            0,
        )

    def parse(self, output: str) -> mtr.Qty:
        return mtr.MultiwfnOutput(output).get("volume")


# class WriteMultiwfnInput(Task):
#     def __init__(
#         self,
#         input_name: str,
#         in_filepath: str,  # FIXME: awful name for this variable, fix here and analogous issues throughout this file
#         commands: Iterable[str],
#         work_directory: str = ".",
#         handlers: Iterable[Handler] = None,
#         name: str = None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = materia.expand(os.path.join(work_directory, input_name))
#         self.in_filepath = materia.expand(in_filepath)
#         self.commands = commands

#         try:
#             os.makedirs(materia.expand(work_directory))
#         except FileExistsError:
#             pass

#     def run(self):
#         materia.MultiwfnInput(self.in_filepath, *self.commands).write(self.input_path)
