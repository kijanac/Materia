from materia.units import Dimension


def test_dimension_str_length():
    length = Dimension(length=1)

    assert str(length) == "L"


def test_dimension_str_mass():
    mass = Dimension(mass=1)

    assert str(mass) == "M"


def test_dimension_str_time():
    time = Dimension(time=1)

    assert str(time) == "T"


def test_dimension_mul():
    length = Dimension(length=1)
    time = Dimension(time=1)

    assert (length * time).dimension_dict == {
        "length": 1,
        "time": 1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_rmul():
    length = Dimension(length=1)
    time = Dimension(time=1)

    assert (time.__rmul__(length)).dimension_dict == {
        "length": 1,
        "time": 1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_imul():
    length = Dimension(length=1)
    time = Dimension(time=1)
    length *= time

    assert length.dimension_dict == {
        "length": 1,
        "time": 1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_truediv():
    length = Dimension(length=1)
    time = Dimension(time=1)

    assert (length / time).dimension_dict == {
        "length": 1,
        "time": -1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_rtruediv():
    length = Dimension(length=1)
    time = Dimension(time=1)

    assert (time.__rtruediv__(length)).dimension_dict == {
        "length": 1,
        "time": -1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_itruediv():
    length = Dimension(length=1)
    time = Dimension(time=1)
    length /= time

    assert length.dimension_dict == {
        "length": 1,
        "time": -1,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_pow():
    length = Dimension(length=1)

    assert (length ** 2).dimension_dict == {
        "length": 2,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_pow_negative():
    length = Dimension(length=1)

    assert (length ** (-2)).dimension_dict == {
        "length": -2,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_pow_zero():
    length = Dimension(length=1)

    assert (length ** 0).dimension_dict == {
        "length": 0,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_ipow():
    length = Dimension(length=1)
    length **= 2
    assert length.dimension_dict == {
        "length": 2,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_ipow_negative():
    length = Dimension(length=1)
    length **= -2

    assert length.dimension_dict == {
        "length": -2,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_ipow_zero():
    length = Dimension(length=1)
    length **= 0

    assert length.dimension_dict == {
        "length": 0,
        "time": 0,
        "mass": 0,
        "electric_current": 0,
        "absolute_temperature": 0,
        "number": 0,
        "luminous_intensity": 0,
    }


def test_dimension_eq_length():
    length = Dimension(length=1)

    assert length == length


def test_dimension_neq_length_time():
    length = Dimension(length=1)
    time = Dimension(time=1)

    assert length != time


def test_dimension_neq_length_lengthsq():
    length = Dimension(length=1)
    lengthsq = Dimension(length=2)

    assert length != lengthsq
