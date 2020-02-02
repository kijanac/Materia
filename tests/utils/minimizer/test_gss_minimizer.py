import materia.utils


def test_gss_bracket_delta_01():
    s = materia.utils.GSSMinimizer(objective_function=lambda x: (x - 2) ** 2)

    assert s._find_gss_bracket(delta=0.01) == (1.2137383539249436, 3.2037886039123507)


def test_gss_bracket_delta_02():
    s = materia.utils.GSSMinimizer(objective_function=lambda x: (x - 2) ** 2)

    assert s._find_gss_bracket(delta=0.02) == (1.487902432574931, 3.947739820199816)


def test_gss_optimize_delta_01_tol_0001():
    s = materia.utils.GSSMinimizer(objective_function=lambda x: (x - 2) ** 2)

    test_result = tuple(s.optimize(delta=0.01, tolerance=0.0001).values())
    print(test_result)
    check_result = (9.646599407882878e-10, 25, 1.999968941024795, 20, True)

    assert test_result == check_result
