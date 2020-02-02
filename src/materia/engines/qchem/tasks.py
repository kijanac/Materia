from __future__ import annotations
import cclib
import contextlib
import os
import materia
import subprocess
import tempfile
from typing import Any, Iterable, Optional, Union

from ...workflow.tasks.task import Task

__all__ = [
    "ComputeKoopmanError",
    "ExecuteQChem",
    "QChemAIMD",
    "QChemLRTDDFT",
    "QChemOptimize",
    "QChemPolarizability",
    "QChemRTTDDFT",
    "QChemSinglePoint",
    "QChemSinglePointFrontier",
    "WriteQChemInput",
    "WriteQChemInputGeometryRelaxation",
    "WriteQChemInputLRTDDFT",
    "WriteQChemInputPolarizability",
    "WriteQChemInputSinglePoint",
    "WriteQChemTDSCF",
]


class QChemBaseTask(Task):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        engine: materia.QChemEngine,
        input_name: str,
        output_name: str,
        settings: Optional[materia.Settings] = None,
        log_name: str = "qchem.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.engine = engine
        self.log_name = log_name
        self.work_dir = materia.expand_path(work_dir)
        self.keep_logs = keep_logs
        self.input_name = input_name
        self.output_name = output_name

        self.settings = settings or materia.Settings()
        self.structure = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"

    def run(self, **kwargs: Any) -> Any:
        with contextlib.nullcontext(
            self.work_dir
        ) if self.keep_logs else tempfile.TemporaryDirectory(dir=self.work_dir) as wd:
            try:
                os.makedirs(wd)
            except FileExistsError:
                pass

            # FIXME: this is essentially a hotpatch to handle fragments - come up with something more elegant/sensible ASAP
            materia.QChemInput(
                molecule=self.structure
                if isinstance(self.structure, materia.Structure)
                or isinstance(self.structure, materia.QChemStructure)
                else materia.QChemFragments(structures=self.structure),
                settings=self.settings,
            ).write(filepath=os.path.join(wd, self.input_name))

            return self.engine.execute(
                os.path.join(wd, self.input_name), os.path.join(wd, self.output_name)
            )


class ComputeKoopmanError(Task):
    def run(self, omega, gs, cation_energy, anion_energy) -> None:
        # FIXME: if ea is negative, don't use it?
        gs_energy, homo, lumo = gs
        ip = cation_energy - gs_energy
        ea = gs_energy - anion_energy
        return (homo.convert(materia.eV) + ip) ** 2 + (lumo.convert(materia.eV) + ea) ** 2


class ExecuteQChem(Task):
    def __init__(
        self,
        input_name: str,
        output_name: str,
        scratch_directory: str,
        executable: str = "qchem",
        work_directory: str = ".",
        num_cores: int = 1,
        parallel: bool = False,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: str = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.input_path = materia.expand_path(os.path.join(work_directory, input_name))
        self.output_path = materia.expand_path(os.path.join(work_directory, output_name))
        self.scratch_directory = materia.expand_path(scratch_directory)

        self.executable = executable

        self.num_cores = num_cores
        self.parallel = parallel

        try:
            os.makedirs(materia.expand_path(work_directory))
        except FileExistsError:
            pass

    def run(self, **kwargs: Any) -> Any:
        os.environ["QCSCRATCH"] = self.scratch_directory
        with open(self.output_path, "w") as f:
            if self.parallel:
                subprocess.call(
                    [self.executable, "-nt", str(self.num_cores), self.input_path],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                )
            else:
                subprocess.call([self.executable, self.input_path], stdout=f)


class QChemAIMD(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        engine: materia.QChemEngine,
        input_name: str,
        output_name: str,
        settings: Optional[materia.Settings] = None,
        log_name: str = "qchem.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            engine=engine,
            input_name=input_name,
            output_name=output_name,
            settings=settings,
            log_name=log_name,
            work_dir=work_dir,
            keep_logs=keep_logs,
            handlers=handlers,
            name=name,
        )
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "aimd"
        if ("rem", "time_step") not in self.settings:
            self.settings["rem", "time_step"] = 1
        if ("rem", "aimd_steps") not in self.settings:
            self.settings["rem", "aimd_steps"] = 10
        if ("velocity",) not in self.settings and (
            "rem",
            "aimd_init_veloc",
        ) not in self.settings:
            self.settings["rem", "aimd_init_veloc"] = "thermal"
        if (
            ("rem", "aimd_init_veloc") in self.settings
            and self.settings["rem", "aimd_init_veloc"].lower().strip() == "thermal"
            and ("rem", "aimd_temp") not in self.settings
        ):
            self.settings["rem", "aimd_temp"] = 300

    def run(self, **kwargs: Any) -> Any:
        output = super().run(**kwargs)

        return output  # FIXME: is there a better return value?


class QChemLRTDDFT(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        engine: materia.QChemEngine,
        input_name: str,
        output_name: str,
        settings: Optional[materia.Settings] = None,
        log_name: str = "qchem.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            engine=engine,
            input_name=input_name,
            output_name=output_name,
            settings=settings,
            log_name=log_name,
            work_dir=work_dir,
            keep_logs=keep_logs,
            handlers=handlers,
            name=name,
        )

        if ("rem", "cis_n_roots") not in self.settings:
            self.settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in self.settings:
            self.settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in self.settings:
            self.settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in self.settings:
            self.settings["rem", "rpa"] = False

    def run(self, **kwargs: Any) -> Any:
        output = super().run(**kwargs)
        raise NotImplementedError
        try:
            polarizability = materia.Qty(
                value=cclib.io.ccread(self.output_name).polarizabilities,
                unit=materia.au_volume,
            )
        except AttributeError:
            polarizability = None

        return polarizability


class QChemOptimize(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        engine: materia.QChemEngine,
        input_name: str,
        output_name: str,
        settings: Optional[materia.Settings] = None,
        log_name: str = "qchem.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            engine=engine,
            input_name=input_name,
            output_name=output_name,
            settings=settings,
            log_name=log_name,
            work_dir=work_dir,
            keep_logs=keep_logs,
            handlers=handlers,
            name=name,
        )
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "opt"

    def run(self, **kwargs: Any) -> Any:
        output = super().run(**kwargs)

        try:
            parsed = cclib.io.ccread(os.path.join(self.work_dir, self.output_name))
            # FIXME: is this the correct unit?
            coords = materia.Qty(value=parsed.atomcoords, unit=materia.angstrom)[-1, :, :]
            zs = parsed.atomnos
        except AttributeError:
            return None
        # FIXME: is this the correct unit?
        atoms = (
            materia.Atom(element=Z, position=materia.Qty(value=p, unit=materia.angstrom))
            for Z, p in zip(zs, coords)
        )
        return materia.Structure(atoms=atoms)


class QChemPolarizability(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        engine: materia.QChemEngine,
        input_name: str,
        output_name: str,
        settings: Optional[materia.Settings] = None,
        log_name: str = "qchem.log",
        work_dir: str = ".",
        keep_logs: bool = True,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            engine=engine,
            input_name=input_name,
            output_name=output_name,
            settings=settings,
            log_name=log_name,
            work_dir=work_dir,
            keep_logs=keep_logs,
            handlers=handlers,
            name=name,
        )

        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "polarizability"

    def run(self, **kwargs: Any) -> Any:
        os.environ[
            "QCINFILEBASE"
        ] = "0"  # bug workaround for parallel polarizability calculation in Q-Chem 5.2.1
        output = super().run(**kwargs)

        try:
            polarizability = materia.Qty(
                value=cclib.io.ccread(
                    os.path.join(self.work_dir, self.output_name)
                ).polarizabilities,
                unit=materia.au_volume,
            )
        except AttributeError:
            polarizability = None

        return polarizability


class QChemRTTDDFT(Task):
    def __init__(
        self,
        structure,
        input_name,
        output_name,
        scratch_directory,
        settings=None,
        tdscf_settings=None,
        executable="qchem",
        work_directory=".",
        num_cores=1,
        parallel=False,
        handlers=None,
        name=None,
    ):
        super().__init__(handlers=handlers, name=name)
        self.work_directory = materia.utils.expand_path(work_directory)
        self.input_path = materia.utils.expand_path(
            os.path.join(work_directory, input_name)
        )
        self.output_path = materia.utils.expand_path(
            os.path.join(work_directory, output_name)
        )
        self.scratch_directory = materia.utils.expand_path(scratch_directory)
        self.executable = executable
        self.num_cores = num_cores
        self.parallel = parallel
        try:
            os.makedirs(materia.utils.expand_path(work_directory))
        except FileExistsError:
            pass
        self.settings = settings or materia.Settings()
        self.settings["molecule", "structure"] = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"
        if ("rem", "rttddft") not in self.settings:
            self.settings["rem", "rttddft"] = 1
        self.tdscf_settings = tdscf_settings or materia.Settings()

    def run(self):
        tdscf_input_path = materia.utils.expand_path(
            os.path.join(self.work_directory, "TDSCF.prm")
        )
        keys = tuple(str(next(iter(k))) for k in self.tdscf_settings)
        max_length = max(len(k) for k in keys)
        with open(materia.utils.expand_path(tdscf_input_path), "w") as f:
            f.write(
                "\n".join(
                    k + " " * (max_length - len(k) + 1) + str(self.tdscf_settings[k])
                    for k in keys
                )
            )
        materia.QChemInput(settings=self.settings).write(filepath=self.input_path)
        try:
            os.makedirs(
                materia.utils.expand_path(os.path.join(self.work_directory, "logs"))
            )
        except FileExistsError:
            pass
        os.environ["QCSCRATCH"] = self.scratch_directory
        with open(self.output_path, "w") as f:
            if self.parallel:
                subprocess.call(
                    [self.executable, "-nt", str(self.num_cores), self.input_path],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                )
            else:
                subprocess.call([self.executable, self.input_path], stdout=f)

        # FIXME: finish with output


class QChemSinglePoint(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        input_name: str,
        output_name: str,
        scratch_directory: str,
        settings: Optional[materia.Settings] = None,
        executable: Optional[str] = "qchem",
        work_directory: Optional[str] = ".",
        num_cores: Optional[int] = 1,
        parallel: Optional[bool] = False,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            input_name=input_name,
            output_name=output_name,
            scratch_directory=scratch_directory,
            settings=settings,
            executable=executable,
            work_directory=work_directory,
            num_cores=num_cores,
            parallel=parallel,
            handlers=handlers,
            name=name,
        )
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "sp"

    def run(self, **kwargs: Any) -> Any:
        super().run(**kwargs)

        try:
            energy = materia.Qty(
                value=cclib.io.ccread(self.output_path).scfenergies, unit=materia.eV
            )
        except AttributeError:
            energy = None

        return energy


class QChemSinglePointFrontier(QChemBaseTask):
    def __init__(
        self,
        structure: Union[materia.QChemStructure, materia.QChemFragments, materia.Structure],
        input_name: str,
        output_name: str,
        scratch_directory: str,
        settings: Optional[materia.Settings] = None,
        executable: Optional[str] = "qchem",
        work_directory: Optional[str] = ".",
        num_cores: Optional[int] = 1,
        parallel: Optional[bool] = False,
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            structure=structure,
            input_name=input_name,
            output_name=output_name,
            scratch_directory=scratch_directory,
            settings=settings,
            executable=executable,
            work_directory=work_directory,
            num_cores=num_cores,
            parallel=parallel,
            handlers=handlers,
            name=name,
        )
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "sp"

    def run(self, **kwargs: Any) -> Any:
        super().run(**kwargs)

        try:
            energy = materia.Qty(
                value=cclib.io.ccread(self.output_path).scfenergies, unit=materia.eV
            )
            alpha_occ, beta_occ, alpha_unocc, beta_unocc = materia.QChemOutput(
                filepath=self.output_path
            ).get("orbital_energies")
            homo = max(max(alpha_occ), max(beta_occ))
            lumo = min(min(alpha_unocc), min(beta_unocc))
        except AttributeError:
            energy = None
            homo = None
            lumo = None

        return energy, homo, lumo


class WriteQChemInput(Task):
    def __init__(
        self,
        structure: materia.Structure,
        input_name: str,
        settings: materia.Settings,
        work_directory: str = ".",
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: str = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.input_path = materia.utils.expand_path(
            os.path.join(work_directory, input_name)
        )
        self.settings = settings
        self.settings["molecule", "structure"] = structure
        try:
            os.makedirs(materia.utils.expand_path(work_directory))
        except FileExistsError:
            pass

    def run(self) -> None:
        materia.QChemInput(settings=self.settings).write(filepath=self.input_path)


class WriteQChemInputGeometryRelaxation(WriteQChemInput):
    def __init__(
        self,
        structure,
        input_name,
        settings=None,
        work_directory=".",
        handlers=None,
        name=None,
    ):
        super().__init__(
            input_name=input_name,
            input_settings=input_settings,
            work_directory=work_directory,
            handlers=handlers,
            name=name,
        )

        self.settings["molecule", "structure"] = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "opt"


class WriteQChemInputLRTDDFT(WriteQChemInput):
    def __init__(
        self,
        structure,
        input_name,
        settings=None,
        work_directory=".",
        handlers=None,
        name=None,
    ):
        super().__init__(
            input_name=input_name,
            input_settings=input_settings,
            work_directory=work_directory,
            handlers=handlers,
            name=name,
        )

        self.settings["molecule", "structure"] = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"
        if ("rem", "cis_n_roots") not in self.settings:
            self.settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in self.settings:
            self.settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in self.settings:
            self.settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in self.settings:
            self.settings["rem", "rpa"] = False


class WriteQChemInputPolarizability(WriteQChemInput):
    def __init__(
        self,
        structure,
        input_name,
        settings=None,
        work_directory=".",
        handlers=None,
        name=None,
    ) -> None:
        super().__init__(
            input_name=input_name,
            input_settings=input_settings,
            work_directory=work_directory,
            handlers=handlers,
            name=name,
        )

        self.settings["molecule", "structure"] = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in self.settings:
            self.settings["rem", "jobtype"] = "polarizability"

    def run(self) -> None:
        os.environ["QCINFILEBASE"] = "0"
        # bug workaround for parallel polarizability calculation in Q-Chem 5.2.1
        super().run()


class WriteQChemInputSinglePoint(WriteQChemInput):
    def __init__(
        self,
        structure,
        input_name,
        settings=None,
        work_directory=".",
        handlers=None,
        name=None,
    ):
        super().__init__(
            input_name=input_name,
            input_settings=input_settings,
            work_directory=work_directory,
            handlers=handlers,
            name=name,
        )

        self.settings["molecule", "structure"] = structure
        if ("rem", "exchange") not in self.settings and (
            "rem",
            "method",
        ) not in self.settings:
            self.settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in self.settings:
            self.settings["rem", "basis"] = "3-21G"


class WriteQChemTDSCF(Task):
    def __init__(
        self,
        settings: Optional[materia.Settings] = None,
        work_directory: str = ".",
        handlers: Optional[Iterable[materia.Handler]] = None,
        name: str = None,
    ):
        super().__init__(handlers=handlers, name=name)
        self.work_directory = materia.utils.expand_path(work_directory)
        self.settings = settings

        try:
            os.makedirs(materia.utils.expand_path(work_directory))
        except FileExistsError:
            pass

    def run(self) -> None:
        input_path = materia.utils.expand_path(
            os.path.join(self.work_directory, "TDSCF.prm")
        )

        keys = tuple(str(next(iter(k))) for k in self.settings)
        max_length = max(len(k) for k in keys)

        with open(materia.utils.expand_path(input_path), "w") as f:
            f.write(
                "\n".join(
                    k + " " * (max_length - len(k) + 1) + str(self.settings[k])
                    for k in keys
                )
            )


class OptimizeRangeSeparationParameter(Task):
    def __init__(
        self,
        structure,
        input_name,
        output_path,
        executable="qchem",
        work_directory=".",
        input_settings=None,
        num_cores=1,
        parallel=False,
    ):
        self.function_evals = {}

        settings = materia.Settings()

        # FIXME: add the appropriate stuff to these default settings (omega, omega2, xc_functional, etc.)
        settings["molecule", "structure"] = structure
        settings["rem", "exchange"] = "HF"
        settings["rem", "basis"] = "3-21G"

        if input_settings is not None:
            for k, v in input_settings.items():
                settings[k] = v

        self.settings["input"] = settings
        self.settings["input_path"] = materia.utils.expand_path(
            os.path.join(work_directory, input_name)
        )
        self.settings["output_path"] = materia.utils.expand_path(
            os.path.join(work_directory, output_path)
        )
        self.settings["executable"] = executable
        self.settings["work_directory"] = materia.utils.expand_path(work_directory)
        self.settings["num_cores"] = num_cores
        self.settings["parallel"] = parallel

    def run(self, **kwargs):
        def f(x):
            if x in self.function_evals:
                return self.function_evals[x]
            else:
                materia.QChemInput(settings=self.settings["input"]).write(
                    filepath=self.settings["input_path"]
                )

                with open(self.settings["output_path"], "w") as f:
                    if self.settings["parallel"]:
                        subprocess.call(
                            [
                                self.settings["executable"],
                                "-nt",
                                str(self.settings["num_cores"]),
                                self.settings["input_path"],
                            ],
                            stdout=f,
                        )
                    else:
                        subprocess.call(
                            [self.settings["executable"], self.settings["input_path"]],
                            stdout=f,
                        )

                # FIXME: get output and save result to self.function_evals
                # FIXME: maybe this shouldn't run the jobs but instead should be the successor to three jobs (gs, cation, anion - links = {0:[3],1:[3],2:[3],3:[]}) and should gather their results to compute and save the HOMO-LUMO / IP-EA error
                #        then a handler is attached to this job which adds three parent tasks with modified omega/omega2 if the error is insufficiently small?
