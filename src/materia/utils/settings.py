from __future__ import annotations
from .nested_dictionary import NestedDictionary

__all__ = ["Settings"]


class Settings(NestedDictionary):
    def update(self, settings: Settings) -> None:
        for k, v in settings.items():
            self.__setitem__(keys=k, value=v)
