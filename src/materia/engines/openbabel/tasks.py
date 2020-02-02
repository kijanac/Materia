from __future__ import annotations
import os
import materia
import rdkit
import re
import tempfile
from typing import Iterable, Optional, Union

from ...workflow.tasks.task import Task

__all__ = [
    "OpenbabelConvertToMol",
    "OpenbabelConvertToPDB",
    "OpenbabelConvertToSMILES",
    "OpenbabelConvertToSDF",
    "OpenbabelGetBonds",
]


class OpenbabelConvertToMol(Task):
    def __init__(
        self,
        engine: materia.OpenbabelEngine,
        output_name: Optional[str] = None,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.engine = engine
        self.output_name = output_name

    def run(self, structure: Union[str, materia.Structure]) -> None:
        arguments = (
            ["-omol", self.output_name] if self.output_name is not None else ["-omol"]
        )
        with contextlib.nullcontext(structure) if isinstance(
            structure, str
        ) else tempfile.NamedTemporaryFile(suffix=".xyz") as fp:
            return self.engine.execute(
                structure_file=fp.name,
                output_file=self.output_name + ".mol",
                arguments=arguments,
            )


class OpenbabelConvertToPDB(Task):
    def __init__(
        self,
        engine: materia.OpenbabelEngine,
        output_name: Optional[str] = None,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.engine = engine
        self.output_name = output_name

    def run(self, structure: Union[str, materia.Structure]) -> None:
        arguments = (
            ["-opdb", self.output_name] if self.output_name is not None else ["-opdb"]
        )
        with contextlib.nullcontext(structure) if isinstance(
            structure, str
        ) else tempfile.NamedTemporaryFile(suffix=".xyz") as fp:
            return self.engine.execute(
                structure_file=fp.name,
                output_file=self.output_name + ".pdb"
                if self.output_name is not None
                else None,
                arguments=arguments,
            )


class OpenbabelConvertToSDF(Task):
    def __init__(
        self,
        engine: materia.OpenbabelEngine,
        output_name: Optional[str] = None,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.engine = engine
        self.output_name = output_name

    def run(self, structure: Union[str, materia.Structure]) -> None:
        arguments = (
            ["-osdf", self.output_name] if self.output_name is not None else ["-osdf"]
        )
        with contextlib.nullcontext(structure) if isinstance(
            structure, str
        ) else tempfile.NamedTemporaryFile(suffix=".xyz") as fp:
            return self.engine.execute(
                structure_file=fp.name,
                output_file=self.output_name + ".sdf",
                arguments=arguments,
            )


class OpenbabelConvertToSMILES(Task):
    def __init__(
        self,
        engine: materia.OpenbabelEngine,
        output_name: Optional[str] = None,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.engine = engine
        self.output_name = output_name

    def run(self, structure: Union[str, materia.Structure]) -> None:
        arguments = (
            ["-osmi", self.output_name] if self.output_name is not None else ["-osmi"]
        )
        with contextlib.nullcontext(structure) if isinstance(
            structure, str
        ) else tempfile.NamedTemporaryFile(suffix=".xyz") as fp:
            output = self.engine.execute(
                structure_file=fp.name,
                output_file=self.output_name + ".smi",
                arguments=arguments,
            )

        smiles, *_ = re.search(r"([^\s]*).*", output).groups()
        return smiles


class OpenbabelGetBonds(Task):
    def __init__(
        self, executable: Optional[str] = "obabel", work_directory: Optional[str] = "."
    ) -> None:
        self.executable = executable
        self.work_directory = materia.utils.expand_path(work_directory)

    def run(self, structure: materia.Structure):
        mol_block = OpenbabelStructureToMolBlock(
            executable=self.executable, work_directory=self.work_directory
        ).run(structure=structure)
        rdkit_mol = rdkit.Chem.MolFromMolBlock(mol_block, removeHs=False)
        conf = rdkit_mol.GetConformer()

        d = {}
        for a in rdkit_mol.GetAtoms():
            pos = conf.GetAtomPosition(a.GetIdx())
            d[a.GetIdx()] = next(
                i
                for i, a2 in enumerate(structure.atoms)
                if tuple(a2.position) == (pos.x, pos.y, pos.z)
            )

        d2 = {}
        for a in rdkit_mol.GetAtoms():
            d2[d[a.GetIdx()]] = tuple(
                d[b.GetOtherAtomIdx(a.GetIdx())] for b in a.GetBonds()
            )

        return d2
