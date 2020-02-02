import materia


def test_unit_meter():
    test_unit = materia.Unit(length=1, prefactor=1)

    assert test_unit.dimension == materia.Dimension(length=1)
    assert test_unit.prefactor == 1


def test_unit_meter_implicit():
    test_unit = materia.Unit(length=1)

    assert test_unit.dimension == materia.Dimension(length=1)
    assert test_unit.prefactor == 1


def test_unit_meter_per_second():
    test_unit = materia.Unit(length=1, time=-1)

    assert test_unit.dimension == materia.Dimension(length=1, time=-1)
    assert test_unit.prefactor == 1


def test_unit_multiply_meter():
    materia.meter = materia.Unit(length=1)

    test_result = materia.meter * materia.meter
    check_result = materia.Unit(length=2)

    assert test_result == check_result


def test_unit_multiply_meter_second():
    materia.meter = materia.Unit(length=1)
    materia.second = materia.Unit(time=1)
    test_result = materia.meter * materia.second
    check_result = materia.Unit(length=1, time=1)

    assert test_result == check_result


def test_unit_multiply_meter_second_prefactor():
    two_meters = materia.Unit(length=1, prefactor=2)
    three_seconds = materia.Unit(time=1, prefactor=3)
    test_result = two_meters * three_seconds
    check_result = materia.Unit(length=1, time=1, prefactor=6)

    assert test_result == check_result


def test_unit_multiply_meter_second_prefactor_negative_float():
    materia.meter = materia.Unit(length=1, prefactor=2.334)
    materia.second = materia.Unit(time=1, prefactor=-1.28482)
    test_result = materia.meter * materia.second
    check_result = materia.Unit(length=1, time=1, prefactor=-2.99876988)

    assert test_result == check_result


def test_unit_divide_meter():
    materia.meter = materia.Unit(length=1)
    test_result = materia.meter / materia.meter
    check_result = materia.Unit()

    assert test_result == check_result


def test_unit_divide_meter_second():
    materia.meter = materia.Unit(length=1)
    materia.second = materia.Unit(time=1)
    test_result = materia.meter / materia.second
    check_result = materia.Unit(length=1, time=-1)

    assert test_result == check_result


def test_unit_divide_meter_second_prefactor():
    materia.meter = materia.Unit(length=1, prefactor=4)
    materia.second = materia.Unit(time=1, prefactor=2)
    test_result = materia.meter / materia.second
    check_result = materia.Unit(length=1, time=-1, prefactor=2)

    assert test_result == check_result


def test_unit_divide_meter_second_prefactor_negative_float():
    materia.meter = materia.Unit(length=1, prefactor=2.334)
    materia.second = materia.Unit(time=1, prefactor=-1.28482)
    test_result = materia.meter / materia.second
    check_result = materia.Unit(length=1, time=-1, prefactor=-1.8165968773836023)

    assert test_result == check_result


def test_unit_equality_meter():
    assert materia.Unit(length=1) == materia.Unit(length=1)


def test_unit_equality_meter_vs_second():
    assert materia.Unit(length=1) != materia.Unit(time=1)


def test_unit_equality_joule_hartree():
    assert materia.joule != materia.hartree


def test_unit_print_meter():
    assert str(materia.Unit(length=1)) == "m"


def test_unit_print_meter_per_second():
    assert str(materia.Unit(length=1, time=-1)) == "(m)/(s)"


def test_unit_print_joule():
    assert str(materia.joule) == "(m^2*kg)/(s^2)"


def test_unit_print_hartree():
    assert str(materia.hartree) == f"{materia.hartree.prefactor} (m^2*kg)/(s^2)"
