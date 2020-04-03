from __future__ import annotations
from typing import Any, Iterable, Optional, Union

import cclib
import copy
import os
import materia as mtr
import numpy as np
import subprocess

from ...workflow.tasks import Task, ExternalTask, InputTask
from ...workflow.workflow import Workflow

__all__ = [
    #    "ExecuteQChem",
    "QChemAIMD",
    "QChemKoopmanError",
    "QChemLRTDDFT",
    "QChemMinimizeKoopmanError",
    "QChemOptimize",
    "QChemPolarizability",
    #    "QChemRTTDDFT",
    "QChemSinglePoint",
    "QChemSinglePointFrontier",
    "WriteQChemInput",
    "WriteQChemInputGeometryRelaxation",
    "WriteQChemInputLRTDDFT",
    "WriteQChemInputPolarizability",
    "WriteQChemInputSinglePoint",
    #    "WriteQChemTDSCF",
]


class QChemBaseTask(ExternalTask):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        raise NotImplementedError

    def parse(self, output: str) -> Any:
        raise NotImplementedError

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> Any:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)

        # FIXME: this is essentially a hotpatch to handle fragments - come up with something more elegant/sensible ASAP
        inp = mtr.QChemInput(
            molecule=structure
            if isinstance(structure, mtr.Structure)
            or isinstance(structure, mtr.QChemStructure)
            else mtr.QChemFragments(structures=structure),
            settings=self.defaults(s),
        )

        with self.io() as io:
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


# class ExecuteQChem(QChemBaseTask):
#     def run(self) -> Any:
#         with self.io() as io:
#             self.engine.execute(io.inp, io.out)


class QChemAIMD(QChemBaseTask):
    def parse(self, output: str) -> Any:
        with open(output, "r") as f:
            return "".join(f.readlines())

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "aimd"
        if ("rem", "time_step") not in settings:
            settings["rem", "time_step"] = 1
        if ("rem", "aimd_steps") not in settings:
            settings["rem", "aimd_steps"] = 10
        if ("velocity",) not in settings and (
            "rem",
            "aimd_init_veloc",
        ) not in settings:
            settings["rem", "aimd_init_veloc"] = "thermal"
        if (
            ("rem", "aimd_init_veloc") in settings
            and settings["rem", "aimd_init_veloc"].lower().strip() == "thermal"
            and ("rem", "aimd_temp") not in settings
        ):
            settings["rem", "aimd_temp"] = 300

        return settings


class QChemKoopmanError(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        gs_io: mtr.IO,
        cation_io: mtr.IO,
        anion_io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            (engine.num_threads or 1) * (engine.num_processors or 1),
            handlers=handlers,
            name=name,
        )
        self.engine = engine
        self.gs_io = gs_io
        self.cation_io = cation_io
        self.anion_io = anion_io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method") not in settings:
            settings["rem", "exchange"] = "hf"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
        num_consumers: Optional[int] = 1,
    ) -> float:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)

        # if ("structure", "charge") not in settings:
        #     settings["structure", "charge"] = 0
        #     # FIXME: rather than guessing 0, use rdkit.Chem.rdmolops.GetFormalCharge?
        # if ("structure", "multiplicity") not in settings:
        #     settings["structure", "multiplicity"] = 1

        input_settings = InputTask(self.defaults(s))

        gs = QChemSinglePointFrontier(self.engine, self.gs_io)
        gs_structure = InputTask(
            mtr.QChemStructure(structure, charge=0, multiplicity=1)
        )
        gs.requires(structure=gs_structure, settings=input_settings)

        cation = QChemSinglePoint(self.engine, self.cation_io)
        cation_structure = InputTask(
            mtr.QChemStructure(structure, charge=1, multiplicity=2)
        )
        cation.requires(structure=cation_structure, settings=input_settings)

        anion = QChemSinglePoint(self.engine, self.anion_io)
        anion_structure = InputTask(
            mtr.QChemStructure(structure, charge=-1, multiplicity=2)
        )
        anion.requires(structure=anion_structure, settings=input_settings)

        wf = Workflow(
            gs,
            cation,
            anion,
            input_settings,
            gs_structure,
            cation_structure,
            anion_structure,
        )

        out = wf.run(available_cores=self.num_cores, num_consumers=num_consumers)

        energy, homo, lumo = out[0]
        cation = out[1]
        anion = out[2]

        ea = energy - anion
        ip = cation - energy

        J_squared = (ea + lumo) ** 2 + (ip + homo) ** 2

        return np.sqrt(J_squared.convert(mtr.eV ** 2).value.item())


class QChemLRTDDFT(QChemBaseTask):
    def parse(self, output: str) -> Any:
        # FIXME: implement using cclib
        raise NotImplementedError

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "cis_n_roots") not in settings:
            settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in settings:
            settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in settings:
            settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in settings:
            settings["rem", "rpa"] = False

        return settings


class QChemMinimizeKoopmanError(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            (engine.num_threads or 1) * (engine.num_processors or 1),
            handlers=handlers,
            name=name,
        )
        self.engine = engine
        self.io = io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"
        if ("rem", "exchange") not in settings:
            settings["rem", "exchange"] = "gen"
        if ("rem", "lrc_dft") not in settings:
            settings["rem", "lrc_dft"] = True
        if ("rem", "src_dft") not in settings:
            settings["rem", "src_dft"] = 2

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
        epsilon: Optional[Union[int, float]] = 1.0,
        alpha: Optional[float] = 0.2,
        num_evals: Optional[int] = 5,
    ) -> float:
        beta = 1 / epsilon - alpha

        s = self.defaults(settings)
        s["rem", "hf_sr"] = int(round(1000 * alpha))
        s["rem", "hf_lr"] = int(round(1000 * (alpha + beta)))
        s["xc_functional"] = (
            ("X", "HF", alpha),
            ("X", "wPBE", beta),
            ("X", "PBE", 1 - alpha - beta),
            ("C", "PBE", 1.0),
        )

        with self.io() as io:

            def f(omega):
                omega = int(round(1000 * omega))
                s["rem", "omega"] = s["rem", "omega2"] = omega

                wd = mtr.expand(f"{io.work_dir}/{omega}")

                gs_io = mtr.IO("gs.in", "gs.out", wd)
                cation_io = mtr.IO("cation.in", "cation.out", wd)
                anion_io = mtr.IO("anion.in", "anion.out", wd)

                ke = mtr.QChemKoopmanError(self.engine, gs_io, cation_io, anion_io)
                # FIXME: not sure the best way to handle num_consumers here...
                return ke.run(structure, s, num_consumers=3)

            return mtr.MaxLIPOTR(f).run(x_min=1e-3, x_max=1, num_evals=num_evals)


class QChemOptimize(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            parsed = cclib.io.ccread(output)
            # FIXME: is this the correct unit?
            coords = parsed.atomcoords[-1, :, :] * mtr.angstrom
            zs = parsed.atomnos
        except AttributeError:
            return None
        # FIXME: is this the correct unit?
        atoms = (
            mtr.Atom(element=Z, position=p * mtr.angstrom) for Z, p in zip(zs, coords)
        )
        return mtr.Structure(*atoms)

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "opt"

        return settings


class QChemPolarizability(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            polarizability = (
                cclib.io.ccread(output).polarizabilities[-1] * mtr.au_volume
            )
        except AttributeError:
            polarizability = None

        return polarizability

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "polarizability"

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> Any:
        # NOTE: bug workaround for parallel polarizability calculation in Q-Chem 5.2.1
        os.environ["QCINFILEBASE"] = "0"
        return super().run(structure, settings)


# class QChemRTTDDFT(Task):
#     def __init__(
#         self,
#         structure,
#         input_name,
#         output_name,
#         scratch_directory,
#         settings=None,
#         tdscf_settings=None,
#         executable="qchem",
#         work_directory=".",
#         num_cores=1,
#         parallel=False,
#         handlers=None,
#         name=None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.work_directory = mtr.expand(work_directory)
#         self.input_path = mtr.expand(os.path.join(work_directory, input_name))
#         self.output_path = mtr.expand(os.path.join(work_directory, output_name))
#         self.scratch_directory = mtr.expand(scratch_directory)
#         self.executable = executable
#         self.num_cores = num_cores
#         self.parallel = parallel
#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass
#         settings = settings or mtr.Settings()
#         settings["molecule", "structure"] = structure
#         if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
#             settings["rem", "exchange"] = "HF"
#         if ("rem", "basis") not in settings:
#             settings["rem", "basis"] = "3-21G"
#         if ("rem", "rttddft") not in settings:
#             settings["rem", "rttddft"] = 1
#         self.tdscf_settings = tdscf_settings or mtr.Settings()

#     def run(self):
#         tdscf_input_path = mtr.expand(os.path.join(self.work_directory, "TDSCF.prm"))
#         keys = tuple(str(next(iter(k))) for k in self.tdscf_settings)
#         max_length = max(len(k) for k in keys)
#         with open(mtr.expand(tdscf_input_path), "w") as f:
#             f.write(
#                 "\n".join(
#                     k + " " * (max_length - len(k) + 1) + str(self.tdscf_settings[k])
#                     for k in keys
#                 )
#             )
#         mtr.QChemInput(settings=settings).write(filepath=self.input_path)
#         try:
#             os.makedirs(mtr.expand(os.path.join(self.work_directory, "logs")))
#         except FileExistsError:
#             pass
#         os.environ["QCSCRATCH"] = self.scratch_directory
#         with open(self.output_path, "w") as f:
#             if self.parallel:
#                 subprocess.call(
#                     [self.executable, "-nt", str(self.num_cores), self.input_path],
#                     stdout=f,
#                     stderr=subprocess.STDOUT,
#                 )
#             else:
#                 subprocess.call([self.executable, self.input_path], stdout=f)

#         # FIXME: finish with output


class QChemSinglePoint(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            energy = cclib.io.ccread(output).scfenergies * mtr.eV
        except AttributeError:
            energy = None

        return energy

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings


class QChemSinglePointFrontier(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            out = cclib.io.ccread(output)
            energy = out.scfenergies * mtr.eV
            moenergies = out.moenergies
            homo_indices = out.homos

            homos = []
            lumos = []

            for moe, h in zip(moenergies, homo_indices):
                homo, lumo = moe[h : h + 2]
                homos.append(homo)
                lumos.append(lumo)

            homo = max(homos) * mtr.eV
            lumo = min(lumos) * mtr.eV
        except AttributeError:
            energy = None
            homo = None
            lumo = None

        return energy, homo, lumo

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method") not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings


class WriteQChemInput(Task):
    def __init__(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: str = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.io = io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> None:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)
        # FIXME: this is essentially a hotpatch to handle fragments - come up with something more elegant/sensible ASAP
        inp = mtr.QChemInput(
            molecule=structure
            if isinstance(structure, mtr.Structure)
            or isinstance(structure, mtr.QChemStructure)
            else mtr.QChemFragments(structures=structure),
            settings=self.defaults(s),
        )

        with self.io() as io:
            inp.write(io.inp)


class WriteQChemInputGeometryRelaxation(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "opt"

        return settings


class WriteQChemInputLRTDDFT(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "cis_n_roots") not in settings:
            settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in settings:
            settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in settings:
            settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in settings:
            settings["rem", "rpa"] = False

        return settings


class WriteQChemInputPolarizability(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "polarizability"

        return settings


class WriteQChemInputSinglePoint(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"

        return settings


# class WriteQChemTDSCF(Task):
#     def __init__(
#         self,
#         settings: Optional[mtr.Settings] = None,
#         work_directory: str = ".",
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: str = None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.work_directory = mtr.expand(work_directory)
#         settings = settings

#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass

#     def run(self) -> None:
#         input_path = mtr.expand(os.path.join(self.work_directory, "TDSCF.prm"))

#         keys = tuple(str(next(iter(k))) for k in settings)
#         max_length = max(len(k) for k in keys)

#         with open(mtr.expand(input_path), "w") as f:
#             f.write(
#                 "\n".join(
#                     k + " " * (max_length - len(k) + 1) + str(settings[k]) for k in keys
#                 )
#             )
