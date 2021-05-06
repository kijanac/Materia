import materia as mtr
import numpy as np


def test_order():
    assert mtr.Identity().order == 1
    assert mtr.Inversion().order == 2
    assert mtr.Reflection([1, 0, 0]).order == 2
    assert mtr.Reflection([0, 1, 1]).order == 2
    assert mtr.Reflection([1, 1, 1]).order == 2
    assert mtr.ProperRotation(axis=[1, 0, 0], order=2).order == 2
    assert mtr.ProperRotation(axis=[1, 0, 0], order=3).order == 3
    assert mtr.ProperRotation(axis=[1, 0, 0], order=7).order == 7
    assert mtr.ProperRotation(axis=[1, 0, 0], order=13).order == 13
    assert mtr.ProperRotation(axis=[0, 1, 1], order=2).order == 2
    assert mtr.ProperRotation(axis=[0, 1, 1], order=3).order == 3
    assert mtr.ProperRotation(axis=[0, 1, 1], order=7).order == 7
    assert mtr.ProperRotation(axis=[0, 1, 1], order=13).order == 13
    assert mtr.ProperRotation(axis=[1, 1, 1], order=2).order == 2
    assert mtr.ProperRotation(axis=[1, 1, 1], order=3).order == 3
    assert mtr.ProperRotation(axis=[1, 1, 1], order=7).order == 7
    assert mtr.ProperRotation(axis=[1, 1, 1], order=13).order == 13
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=2).order == 2
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=3).order == 6
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=7).order == 14
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=13).order == 26
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=2).order == 2
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=3).order == 6
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=7).order == 14
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=13).order == 26
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=2).order == 2
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=3).order == 6
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=7).order == 14
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=13).order == 26


def test_determinant():
    assert mtr.Identity().det == 1
    assert mtr.Inversion().det == -1
    assert mtr.Reflection([1, 0, 0]).det == -1
    assert mtr.Reflection([0, 1, 1]).det == -1
    assert mtr.Reflection([1, 1, 1]).det == -1
    assert mtr.ProperRotation(axis=[1, 0, 0], order=2).det == 1
    assert mtr.ProperRotation(axis=[1, 0, 0], order=3).det == 1
    assert mtr.ProperRotation(axis=[1, 0, 0], order=7).det == 1
    assert mtr.ProperRotation(axis=[1, 0, 0], order=13).det == 1
    assert mtr.ProperRotation(axis=[0, 1, 1], order=2).det == 1
    assert mtr.ProperRotation(axis=[0, 1, 1], order=3).det == 1
    assert mtr.ProperRotation(axis=[0, 1, 1], order=7).det == 1
    assert mtr.ProperRotation(axis=[0, 1, 1], order=13).det == 1
    assert mtr.ProperRotation(axis=[1, 1, 1], order=2).det == 1
    assert mtr.ProperRotation(axis=[1, 1, 1], order=3).det == 1
    assert mtr.ProperRotation(axis=[1, 1, 1], order=7).det == 1
    assert mtr.ProperRotation(axis=[1, 1, 1], order=13).det == 1
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=2).det == -1
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=3).det == -1
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=7).det == -1
    assert mtr.ImproperRotation(axis=[1, 0, 0], order=13).det == -1
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=2).det == -1
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=3).det == -1
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=7).det == -1
    assert mtr.ImproperRotation(axis=[0, 1, 1], order=13).det == -1
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=2).det == -1
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=3).det == -1
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=7).det == -1
    assert mtr.ImproperRotation(axis=[1, 1, 1], order=13).det == -1


def test_trace():
    assert np.isclose(mtr.Identity().tr, 3)
    assert np.isclose(mtr.Inversion().tr, -3)
    assert np.isclose(mtr.Reflection([1, 0, 0]).tr, 1)
    assert np.isclose(mtr.Reflection([0, 1, 1]).tr, 1)
    assert np.isclose(mtr.Reflection([1, 1, 1]).tr, 1)
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 0, 0], order=2).tr, 1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 0, 0], order=3).tr, 1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 0, 0], order=7).tr, 1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 0, 0], order=13).tr, 1 + 2 * np.cos(2 * np.pi / 13)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[0, 1, 1], order=2).tr, 1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[0, 1, 1], order=3).tr, 1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[0, 1, 1], order=7).tr, 1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[0, 1, 1], order=13).tr, 1 + 2 * np.cos(2 * np.pi / 13)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 1, 1], order=2).tr, 1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 1, 1], order=3).tr, 1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 1, 1], order=7).tr, 1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ProperRotation(axis=[1, 1, 1], order=13).tr, 1 + 2 * np.cos(2 * np.pi / 13)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 0, 0], order=2).tr, -1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 0, 0], order=3).tr, -1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 0, 0], order=7).tr, -1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 0, 0], order=13).tr,
        -1 + 2 * np.cos(2 * np.pi / 13),
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[0, 1, 1], order=2).tr, -1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[0, 1, 1], order=3).tr, -1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[0, 1, 1], order=7).tr, -1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[0, 1, 1], order=13).tr,
        -1 + 2 * np.cos(2 * np.pi / 13),
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 1, 1], order=2).tr, -1 + 2 * np.cos(2 * np.pi / 2)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 1, 1], order=3).tr, -1 + 2 * np.cos(2 * np.pi / 3)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 1, 1], order=7).tr, -1 + 2 * np.cos(2 * np.pi / 7)
    )
    assert np.isclose(
        mtr.ImproperRotation(axis=[1, 1, 1], order=13).tr,
        -1 + 2 * np.cos(2 * np.pi / 13),
    )
