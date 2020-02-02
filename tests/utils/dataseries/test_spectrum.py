import numpy as np

from materia.utils import Spectrum, ASTMG173

from materia.units import nanometer, Qty


def test_spectrum_extrapolate_linear():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = 2 * x
    line = Spectrum(x=x, y=y)

    x_extrap_to = Qty(value=np.linspace(0, 15, 16), unit=nanometer)

    line.extrapolate(x_extrap_to=x_extrap_to)

    assert line.x == x_extrap_to
    assert line.y == 2 * x_extrap_to


def test_spectrum_interpolate_cubic_spline_linear():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = 2 * x
    line = Spectrum(x=x, y=y)

    x_interp_to = Qty(value=np.linspace(1, 10, 19), unit=nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="cubic_spline")

    assert line.x == x_interp_to
    assert line.y == 2 * x_interp_to


def test_spectrum_interpolate_linear_spline_linear():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = 2 * x
    line = Spectrum(x=x, y=y)

    x_interp_to = Qty(value=np.linspace(1, 10, 19), unit=nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="linear_spline")

    assert line.x == x_interp_to
    assert line.y == 2 * x_interp_to


# def test_spectrum_interpolate_sprague_linear():
#     x = Qty(value=np.linspace(1,10,10),unit=nanometer)
#     y = 2*x
#     line = Spectrum(x=x,y=y)
#
#     x_interp_to = Qty(value=np.linspace(1,10,19),unit=nanometer)
#     line.interpolate(x_interp_to=x_interp_to,method='sprague')
#
#     assert line.x == x_interp_to
#     assert line.y == 2*x_interp_to


def test_spectrum_extrapolate_quadratic():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = x ** 2
    line = Spectrum(x=x, y=y)

    x_extrap_to = Qty(value=np.linspace(0, 15, 16), unit=nanometer)

    line.extrapolate(x_extrap_to=x_extrap_to)

    check_result_x = x_extrap_to
    check_result_y = Qty(
        value=np.array(
            [
                -2.0,
                1.0,
                4.0,
                9.0,
                16.0,
                25.0,
                36.0,
                49.0,
                64.0,
                81.0,
                100.0,
                119.0,
                138.0,
                157.0,
                176.0,
                195.0,
            ]
        ),
        unit=nanometer ** 2,
    )

    assert line.x == check_result_x
    assert line.y == check_result_y


def test_spectrum_interpolate_cubic_spline_quadratic():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = x ** 2
    line = Spectrum(x=x, y=y)

    x_interp_to = Qty(value=np.linspace(1, 10, 19), unit=nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="cubic_spline")

    assert line.x == x_interp_to
    assert line.y == x_interp_to ** 2


def test_spectrum_interpolate_linear_spline_quadratic():
    x = Qty(value=np.linspace(1, 10, 10), unit=nanometer)
    y = x ** 2
    line = Spectrum(x=x, y=y)

    x_interp_to = Qty(value=np.linspace(1, 10, 19), unit=nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="linear_spline")

    check_result_x = x_interp_to
    check_result_y = Qty(
        value=np.array(
            [
                1.0,
                2.5,
                4.0,
                6.5,
                9.0,
                12.5,
                16.0,
                20.5,
                25.0,
                30.5,
                36.0,
                42.5,
                49.0,
                56.5,
                64.0,
                72.5,
                81.0,
                90.5,
                100.0,
            ]
        ),
        unit=nanometer ** 2,
    )

    assert line.x == check_result_x
    assert line.y == check_result_y


def test_spectrum_extrapolate_ASTMG173():
    astmg173 = ASTMG173()
    original_x_unit, original_y_unit = astmg173.x.unit, astmg173.y.unit
    x_extrap_to = Qty(value=np.linspace(200, 5000, 6000), unit=nanometer)

    astmg173.extrapolate(x_extrap_to)

    assert astmg173.x.value[0] == 200.0
    assert astmg173.x.value[-1] == 5000.0
    assert astmg173.x.unit == original_x_unit

    assert astmg173.y.value[0] == -1.8929525100000004e-19
    assert astmg173.y.value[-1] == -0.014035700000000047
    assert astmg173.y.unit == original_y_unit
