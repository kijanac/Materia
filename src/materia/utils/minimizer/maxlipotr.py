import dlib

# import matplotlib.pyplot as plt

from materia.utils import memoize

__all__ = ["MaxLIPOTRMinimizer"]


class MaxLIPOTRMinimizer:
    def __init__(self, objective_function):
        self.objective_function = objective_function

    @memoize
    def evaluate_objective(self, *args):
        return self.objective_function(*args)

    def optimize(self, x_min, x_max, num_evals):

        return dlib.find_min_global(
            self.evaluate_objective,
            x_min if isinstance(x_min, list) else [x_min],
            x_max if isinstance(x_max, list) else [x_max],
            num_evals,
        )

    # def plot_results(self):
    #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
    #     plt.plot(x, y)
    #     plt.show()
