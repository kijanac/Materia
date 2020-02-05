import numpy as np

import materia
from pytest import approx


def test_qty_add_meter_int():
    q1 = materia.Qty(value=2, unit=materia.meter)
    q2 = materia.Qty(value=3, unit=materia.meter)

    sum = q1 + q2

    assert sum.value == 5
    assert sum.unit == materia.meter


def test_qty_add_meter_negative_float():
    q1 = materia.Qty(value=2.4, unit=materia.meter)
    q2 = materia.Qty(value=-3.9, unit=materia.meter)

    sum = q1 + q2

    assert sum.value == -1.5
    assert sum.unit == materia.meter


def test_qty_add_meter_int_nparray():
    q1 = materia.Qty(value=np.array([1, 2, 3]), unit=materia.meter)
    q2 = materia.Qty(value=np.array([4, 5, 6]), unit=materia.meter)

    sum = q1 + q2

    assert np.array_equal(sum.value, np.array([5, 7, 9]))
    assert sum.unit == materia.meter


def test_qty_subtract_meter_int():
    q1 = materia.Qty(value=2, unit=materia.meter)
    q2 = materia.Qty(value=3, unit=materia.meter)

    diff = q1 - q2

    assert diff.value == -1
    assert diff.unit == materia.meter


def test_qty_subtract_meter_negative_float():
    q1 = materia.Qty(value=2.4, unit=materia.meter)
    q2 = materia.Qty(value=-3.9, unit=materia.meter)

    diff = q1 - q2

    assert diff.value == 6.3
    assert diff.unit == materia.meter


def test_qty_subtract_meter_int_nparray():
    q1 = materia.Qty(value=np.array([1, 2, 3]), unit=materia.meter)
    q2 = materia.Qty(value=np.array([4, 5, 6]), unit=materia.meter)

    diff = q1 - q2

    assert np.array_equal(diff.value, -np.array([3, 3, 3]))
    assert diff.unit == materia.meter


def test_qty_convert_debye_to_au():
    one_au_dip = materia.Qty(value=1, unit=materia.au_dipole_moment)
    one_au_dip.convert(new_unit=materia.debye)

    debye_per_au = one_au_dip.value

    assert debye_per_au == approx(2.5417464511340113)


def test_qty_convert_ev_to_joule():
    one_ev = materia.Qty(value=1, unit=materia.ev)
    one_ev.convert(new_unit=materia.joule)

    joule_per_ev = one_ev.value

    assert joule_per_ev == approx(1.6021766208e-19)


def test_qty_convert_hartree_to_joule():
    one_hartree = materia.Qty(value=1, unit=materia.hartree)
    one_hartree.convert(new_unit=materia.joule)

    joule_per_hartree = one_hartree.value

    assert joule_per_hartree == approx(4.3597446511980845e-18)


def test_qty_convert_hartree_to_ev():
    one_hartree = materia.Qty(value=1, unit=materia.hartree)
    one_hartree.convert(new_unit=materia.ev)

    ev_per_hartree = one_hartree.value

    assert ev_per_hartree == approx(27.211386026973564)


def test_qty_int_list_0():
    qty = materia.Qty(value=[], unit=materia.meter)

    assert len(qty) == 0


def test_qty_int_list_1():
    qty = materia.Qty(value=[1], unit=materia.meter)

    assert len(qty) == 1


def test_qty_int_list_10():
    qty = materia.Qty(value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], unit=materia.meter)

    assert len(qty) == 10


def test_qty_int_tuple_0():
    qty = materia.Qty(value=(), unit=materia.meter)

    assert len(qty) == 0


def test_qty_int_tuple_1():
    qty = materia.Qty(value=(1,), unit=materia.meter)

    assert len(qty) == 1


def test_qty_int_tuple_10():
    qty = materia.Qty(value=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), unit=materia.meter)

    assert len(qty) == 10


def test_qty_int_nparray_0():
    qty = materia.Qty(value=np.array([]), unit=materia.meter)

    assert len(qty) == 0


def test_qty_int_nparray_1():
    qty = materia.Qty(value=np.array([1]), unit=materia.meter)

    assert len(qty) == 1


def test_qty_int_nparray_10():
    qty = materia.Qty(
        value=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), unit=materia.meter
    )

    assert len(qty) == 10


def test_qty_int_list_index_1():
    qty = materia.Qty(value=[1], unit=materia.meter)

    assert qty.index(1) == 0


def test_qty_int_list_index_10():
    qty = materia.Qty(value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], unit=materia.meter)

    assert qty.index(5) == 4
