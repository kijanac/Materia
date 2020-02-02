import math

# import matplotlib.pyplot as plt
import scipy.optimize

from materia.utils import memoize

__all__ = ["GSSMinimizer"]


class GSSMinimizer:
    def __init__(self, objective_function):
        self.objective_function = objective_function

    @memoize
    def evaluate_objective(self, x):
        return self.objective_function(x)

    def optimize(self, delta, tolerance):
        bracket = self._find_gss_bracket(delta=delta)

        return scipy.optimize.minimize_scalar(
            fun=self.evaluate_objective, bracket=bracket, method="Golden", tol=tolerance
        )

    def _find_gss_bracket(self, delta):
        # FIXME: ugly but it works...
        phi = (1 + math.sqrt(5)) / 2

        self.evaluate_objective(x=0.0)
        self.evaluate_objective(x=delta)

        while self.evaluate_objective.cache.last_result(
            n=1
        ) <= self.evaluate_objective.cache.last_result(n=2):
            _, last1 = self.evaluate_objective.cache.last_args(n=1)
            _, last2 = self.evaluate_objective.cache.last_args(n=2)

            self.evaluate_objective(x=last1["x"] + phi * (last1["x"] - last2["x"]))

        if len(self.evaluate_objective.cache) > 2:
            _, last3 = self.evaluate_objective.cache.last_args(n=3)
            _, last1 = self.evaluate_objective.cache.last_args(n=1)
            return (last3["x"], last1["x"])
        else:
            _, last2 = self.evaluate_objective.cache.last_args(n=2)
            _, last1 = self.evaluate_objective.cache.last_args(n=1)
            return (last2["x"], last1["x"])

        return bracket

    # def plot_results(self):
    #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
    #     plt.plot(x, y)
    #     plt.show()
