import collections
import functools


class Cache(collections.OrderedDict):
    def last_result(self, n=1):
        return tuple(self.values())[-n]

    def last_args(self, n=1):
        args, kwarg_items = tuple(self.keys())[-n]
        return args, dict(kwarg_items)


def memoize(func):
    func.cache = Cache()

    @functools.wraps(func)
    def memoized(*args, **kwargs):
        k = (args, frozenset(kwargs.items()))
        if k not in func.cache:
            func.cache[k] = func(*args, **kwargs)

        return func.cache[k]

    return memoized
