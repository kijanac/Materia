from __future__ import annotations
from typing import Any, Callable, Iterable, Optional

import functools
import materia as mtr
import subprocess

__all__ = ["ExternalTask", "FunctionTask", "InputTask", "ShellCommand", "Task"]


class Task:
    def __init__(
        self,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.handlers = handlers or []
        self.name = name or ""
        self.requirements = ([], {})

    def requires(self, *args: Task, **kwargs: Task) -> None:
        self.requirements = (args, kwargs)

    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class ExternalTask(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.engine = engine
        self.io = io
        super().__init__(handlers=handlers, name=name)


class FunctionTask(Task):
    def __init__(
        self,
        f: Callable,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.f = f

    def run(self, **kwargs) -> None:
        return self.f(**kwargs)


class InputTask(Task):
    def __init__(
        self,
        value: Any,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.value = value

    def run(self) -> Any:
        return self.value


class ShellCommand(Task):
    def __init__(
        self,
        command: str,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.command = command

    def run(self) -> None:
        subprocess.call(self.command.split())


def task(
    f: Callable = None,
    handlers: Optional[Iterable[Handler]] = None,
    name: Optional[str] = None,
) -> FunctionTask:
    # FIXME: this is incomptabile with mtr.Workflow.run(thread=False) (i.e. with multiprocessing) because FunctionTask cannot be serialized!
    if f is None:
        return functools.partial(task, handlers=handlers, name=name)

    return FunctionTask(f=f, handlers=handlers, name=name)
