import contextlib
import numpy as np


@contextlib.contextmanager
def temporary_seed(seed):
    # adapted from https://stackoverflow.com/a/49557127
    state = np.random.get_state()
    if seed is not None:
        np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(state)
