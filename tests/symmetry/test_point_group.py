import materia.symmetry
import numpy as np


def test_point_group_C1():
    ctable = materia.symmetry.C1().cayley_table()

    assert (ctable == np.array([[0]])).all()


def test_point_group_Ci():
    ctable = materia.symmetry.Ci().cayley_table()

    assert (ctable == np.array([[0, 1], [1, 0]])).all()
