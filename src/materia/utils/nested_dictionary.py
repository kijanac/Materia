from __future__ import annotations
import collections

__all__ = ["NestedDictionary"]


class NestedDictionary(collections.abc.MutableMapping):
    def __init__(self, *args, **kwargs) -> None:
        self.d = dict(*args, **kwargs)

    def __getitem__(self, keys) -> NestedDictionary:
        if not isinstance(keys, tuple):
            keys = (keys,)

        branch = self.d
        for k in keys:
            branch = branch[k]

        return NestedDictionary(branch) if isinstance(branch, dict) else branch

    def __setitem__(self, keys, value) -> None:
        if not isinstance(keys, tuple):
            keys = (keys,)

        *most_keys, last_key = keys

        branch = self.d
        for k in most_keys:
            if k not in branch:
                branch[k] = {}
            branch = branch[k]

        branch[last_key] = value

    def __delitem__(self, keys) -> None:
        if not isinstance(keys, tuple):
            keys = (keys,)

        *most_keys, last_key = keys

        branch = self.d
        for k in most_keys:
            # FIXME: does this really need to be here? if we're deleting the item, we shouldn't ever need to make branches on the way to the item...
            if k not in branch:
                branch[k] = {}
            branch = branch[k]

        del branch[last_key]

    def __iter__(self, d=None, prepath=()):
        if d == None:
            d = self.d
        for k, v in d.items():
            if hasattr(v, "items"):
                for keys in self.__iter__(d=v, prepath=prepath + (k,)):
                    yield keys
            else:
                yield prepath + (k,)

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __str__(self) -> str:
        return str(self.d)

    def __repr__(self) -> str:
        return repr(self.d)
