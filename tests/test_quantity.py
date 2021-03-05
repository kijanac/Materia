import materia as mtr
import numpy as np
from pytest import approx


def test_dimension_str_length():
    length = mtr.Dimension(L=1)

    assert str(length) == "L"


def test_dimension_str_mass():
    mass = mtr.Dimension(M=1)

    assert str(mass) == "M"


def test_dimension_str_time():
    time = mtr.Dimension(T=1)

    assert str(time) == "T"


def test_dimension_mul():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)

    assert (length * time)._d == dict(L=1, T=1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_rmul():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)

    assert (time.__rmul__(length))._d == dict(L=1, T=1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_imul():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)
    length *= time

    assert length._d == dict(L=1, T=1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_truediv():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)

    assert (length / time)._d == dict(L=1, T=-1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_rtruediv():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)

    assert (time.__rtruediv__(length))._d == dict(L=1, T=-1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_itruediv():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)
    length /= time

    assert length._d == dict(L=1, T=-1, M=0, A=0, K=0, N=0, J=0)


def test_dimension_pow():
    length = mtr.Dimension(L=1)

    assert (length ** 2)._d == dict(L=2, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_pow_negative():
    length = mtr.Dimension(L=1)

    assert (length ** (-2))._d == dict(L=-2, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_pow_zero():
    length = mtr.Dimension(L=1)

    assert (length ** 0)._d == dict(L=0, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_ipow():
    length = mtr.Dimension(L=1)
    length **= 2
    assert length._d == dict(L=2, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_ipow_negative():
    length = mtr.Dimension(L=1)
    length **= -2

    assert length._d == dict(L=-2, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_ipow_zero():
    length = mtr.Dimension(L=1)
    length **= 0

    assert length._d == dict(L=0, T=0, M=0, A=0, K=0, N=0, J=0)


def test_dimension_eq_length():
    length = mtr.Dimension(L=1)

    assert length == length


def test_dimension_neq_length_time():
    length = mtr.Dimension(L=1)
    time = mtr.Dimension(T=1)

    assert length != time


def test_dimension_neq_length_lengthsq():
    length = mtr.Dimension(L=1)
    lengthsq = mtr.Dimension(L=2)

    assert length != lengthsq


def test_qty_add_meter_int():
    q1 = 2 * mtr.meter
    q2 = 3 * mtr.meter

    sum = q1 + q2

    assert sum.value == 5
    assert sum.unit == mtr.meter


def test_qty_add_meter_negative_float():
    q1 = 2.4 * mtr.meter
    q2 = -3.9 * mtr.meter

    sum = q1 + q2

    assert sum.value == -1.5
    assert sum.unit == mtr.meter


def test_qty_add_meter_int_nparray():
    q1 = np.array([1, 2, 3]) * mtr.meter
    q2 = np.array([4, 5, 6]) * mtr.meter

    sum = q1 + q2

    assert np.array_equal(sum.value, np.array([5, 7, 9]))
    assert sum.unit == mtr.meter


def test_qty_subtract_meter_int():
    q1 = 2 * mtr.meter
    q2 = 3 * mtr.meter
    print(q1)
    print(q2)
    diff = q1 - q2
    print(diff)
    assert diff.value == -1
    assert diff.unit == mtr.meter


def test_qty_subtract_meter_negative_float():
    q1 = 2.4 * mtr.meter
    q2 = -3.9 * mtr.meter

    diff = q1 - q2

    assert diff.value == 6.3
    assert diff.unit == mtr.meter


def test_qty_subtract_meter_int_nparray():
    q1 = np.array([1, 2, 3]) * mtr.meter
    q2 = np.array([4, 5, 6]) * mtr.meter

    diff = q1 - q2

    assert np.array_equal(diff.value, -np.array([3, 3, 3]))
    assert diff.unit == mtr.meter


def test_qty_convert_debye_to_au():
    one_au_dip = mtr.au_dipole_moment.convert(convert_to=mtr.debye)

    debye_per_au = one_au_dip.value

    assert debye_per_au == approx(2.5417464511340113)


def test_qty_convert_ev_to_joule():
    one_ev = mtr.ev.convert(convert_to=mtr.joule)

    joule_per_ev = one_ev.value

    assert joule_per_ev == approx(1.6021766208e-19)


def test_qty_convert_hartree_to_joule():
    one_hartree = mtr.hartree.convert(convert_to=mtr.joule)

    joule_per_hartree = one_hartree.value

    assert joule_per_hartree == approx(4.3597446511980845e-18)


def test_qty_convert_hartree_to_ev():
    one_hartree = mtr.hartree.convert(convert_to=mtr.ev)

    ev_per_hartree = one_hartree.value

    assert ev_per_hartree == approx(27.211386026973564)


def test_qty_int_list_0():
    qty = [] * mtr.meter

    assert len(qty) == 0


def test_qty_int_list_1():
    qty = [1] * mtr.meter

    assert len(qty) == 1


def test_qty_int_list_10():
    qty = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * mtr.meter

    assert len(qty) == 10


def test_qty_int_tuple_0():
    qty = () * mtr.meter

    assert len(qty) == 0


def test_qty_int_tuple_1():
    qty = (1,) * mtr.meter

    assert len(qty) == 1


def test_qty_int_tuple_10():
    qty = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) * mtr.meter

    assert len(qty) == 10


def test_qty_int_nparray_0():
    qty = np.array([]) * mtr.meter

    assert len(qty) == 0


def test_qty_int_nparray_1():
    qty = np.array([1]) * mtr.meter

    assert len(qty) == 1


def test_qty_int_nparray_10():
    qty = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) * mtr.meter

    assert len(qty) == 10


def test_qty_int_list_index_1():
    qty = [1] * mtr.meter

    assert qty.index(1 * mtr.meter) == 0


def test_qty_int_list_index_10():
    qty = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * mtr.meter

    assert qty.index(5 * mtr.meter) == 4


# def test_unit_meter():
#     test_unit = mtr.Unit(L=1, value=1)

#     assert test_unit.dimension == mtr.Dimension(L=1)
#     assert test_unit.value == 1


# def test_unit_meter_implicit():
#     test_unit = mtr.Unit(L=1)

#     assert test_unit.dimension == mtr.Dimension(L=1)
#     assert test_unit.value == 1


# def test_unit_meter_per_second():
#     test_unit = mtr.Unit(L=1, T=-1)

#     assert test_unit.dimension == mtr.Dimension(L=1, T=-1)
#     assert test_unit.value == 1


# def test_unit_multiply_meter():
#     mtr.meter = mtr.Unit(L=1)

#     test_result = mtr.meter * mtr.meter
#     check_result = mtr.Unit(L=2)

#     assert test_result == check_result


# def test_unit_multiply_meter_second():
#     mtr.meter = mtr.Unit(L=1)
#     mtr.second = mtr.Unit(T=1)
#     test_result = mtr.meter * mtr.second
#     check_result = mtr.Unit(L=1, T=1)

#     assert test_result == check_result


# def test_unit_multiply_meter_second_value():
#     two_meters = mtr.Unit(L=1, value=2)
#     three_seconds = mtr.Unit(T=1, value=3)
#     test_result = two_meters * three_seconds
#     check_result = mtr.Unit(L=1, T=1, value=6)

#     assert test_result == check_result


# def test_unit_multiply_meter_second_value_negative_float():
#     mtr.meter = mtr.Unit(L=1, value=2.334)
#     mtr.second = mtr.Unit(T=1, value=-1.28482)
#     test_result = mtr.meter * mtr.second
#     check_result = mtr.Unit(L=1, T=1, value=-2.99876988)

#     assert test_result == check_result


# def test_unit_divide_meter():
#     mtr.meter = mtr.Unit(L=1)
#     test_result = mtr.meter / mtr.meter
#     check_result = mtr.Unit()

#     assert test_result == check_result


# def test_unit_divide_meter_second():
#     mtr.meter = mtr.Unit(L=1)
#     mtr.second = mtr.Unit(T=1)
#     test_result = mtr.meter / mtr.second
#     check_result = mtr.Unit(L=1, T=-1)

#     assert test_result == check_result


# def test_unit_divide_meter_second_value():
#     mtr.meter = mtr.Unit(L=1, value=4)
#     mtr.second = mtr.Unit(T=1, value=2)
#     test_result = mtr.meter / mtr.second
#     check_result = mtr.Unit(L=1, T=-1, value=2)

#     assert test_result == check_result


# def test_unit_divide_meter_second_value_negative_float():
#     mtr.meter = mtr.Unit(L=1, value=2.334)
#     mtr.second = mtr.Unit(T=1, value=-1.28482)
#     test_result = mtr.meter / mtr.second
#     check_result = mtr.Unit(L=1, T=-1, value=-1.8165968773836023)

#     assert test_result == check_result


# def test_unit_equality_meter():
#     assert mtr.Unit(L=1) == mtr.Unit(L=1)


# def test_unit_equality_meter_vs_second():
#     assert mtr.Unit(L=1) != mtr.Unit(T=1)


# def test_unit_equality_joule_hartree():
#     assert mtr.joule != mtr.hartree


# def test_unit_print_meter():
#     assert str(mtr.Unit(L=1)) == "m"


# def test_unit_print_meter_per_second():
#     assert str(mtr.Unit(L=1, T=-1)) == "(m)/(s)"


# def test_unit_print_joule():
#     assert str(mtr.joule) == "(m^2*kg)/(s^2)"


# def test_unit_print_hartree():
#     assert str(mtr.hartree) == f"{mtr.hartree.value} (m^2*kg)/(s^2)"
