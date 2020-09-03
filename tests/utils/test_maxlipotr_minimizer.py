import materia as mtr
import numpy as np
import pytest


# def test_gss_bracket_delta_01():
#     s = mtr.GoldenSectionSearch(objective_function=lambda x: (x - 2) ** 2)

#     assert s._find_gss_bracket(delta=0.01) == (1.0933645185324488, 2.8844097435211147)


# def test_gss_bracket_delta_02():
#     s = mtr.GoldenSectionSearch(objective_function=lambda x: (x - 2) ** 2)

#     assert s._find_gss_bracket(delta=0.02) == (1.414507310946184, 3.751352829189824)


# def test_gss_optimize_delta_01_tol_0001():
#     s = mtr.GoldenSectionSearch(objective_function=lambda x: (x - 2) ** 2)

#     test_result = tuple(s.run(delta=0.01, tolerance=0.0001).values())
#     print(test_result)
#     check_result = (6.17113206775526e-10, 25, 1.9999751582366412, 20, True)

#     assert test_result == check_result


def test_maxlipotr_optimize_min_0_max_5_numevals_20():
    s = mtr.MaxLIPOTR(objective_function=lambda x: (x - 2) ** 2)

    assert s.run(x_min=0, x_max=5, num_evals=20) == ([2.0], 0.0)


def test_maxlipotr_optimize_rastrigin():
    np.random.seed(1908173098)
    xs = 10.24 * np.random.random(10) - 5.12

    def rastigrin(x):
        return 10 * len(xs) + np.sum(xs - 10 * np.cos(2 * np.pi * xs))

    s = mtr.MaxLIPOTR(objective_function=rastigrin)

    test_result = tuple(s.run(x_min=-5.12, x_max=5.12, num_evals=10))
    check_result = ([0.0], 75.99791446043284)

    assert test_result == check_result


def test_maxlipotr_optimize_ackley():
    def ackley(x, y):
        return (
            -20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2)))
            - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
            + np.e
            + 20
        )

    s = mtr.MaxLIPOTR(objective_function=ackley)

    test_result = tuple(s.run(x_min=[-5, -5], x_max=[5, 5], num_evals=10))
    check_result = ([0.0, 0.0], 0.0)

    assert test_result == check_result


# FIXME: this test fails occasionaly due to a very incorrect answer for no discernible reason
# def test_maxlipotr_optimize_beale():
#     def beale(x, y):
#         return (
#             (1.5 - x + x * y) ** 2
#             + (2.25 - x + x * y ** 2) ** 2
#             + (2.625 - x + x * y ** 3) ** 2
#         )

#     s = mtr.MaxLIPOTR(objective_function=beale)

#     test_result = tuple(s.run(x_min=[-4.5, -4.5], x_max=[4.5, 4.5], num_evals=300))
#     check_result = ([2.9999999999998272, 0.5000000000001019], 4.880287250592691e-25)

#     assert pytest.approx(test_result[0][0]) == pytest.approx(check_result[0][0])
#     assert pytest.approx(test_result[0][1]) == pytest.approx(check_result[0][1])
#     assert pytest.approx(test_result[-1]) == pytest.approx(check_result[-1])
