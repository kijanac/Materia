import numpy as np

from materia.utils import SPDSpectrum, ASTMG173

import materia


def test_spd_spectrum_extrapolate_linear():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = 2 * x
    line = SPDSpectrum(x=x, y=y)

    x_extrap_to = materia.Qty(value=np.linspace(0, 15, 16), unit=materia.nanometer)

    line.extrapolate(x_extrap_to=x_extrap_to)

    assert line.x == x_extrap_to
    assert line.y == 2 * x_extrap_to


def test_spd_spectrum_interpolate_cubic_spline_linear():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = 2 * x
    line = SPDSpectrum(x=x, y=y)

    x_interp_to = materia.Qty(value=np.linspace(1, 10, 19), unit=materia.nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="cubic_spline")

    assert line.x == x_interp_to
    assert line.y == 2 * x_interp_to


def test_spd_spectrum_interpolate_linear_spline_linear():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = 2 * x
    line = SPDSpectrum(x=x, y=y)

    x_interp_to = materia.Qty(value=np.linspace(1, 10, 19), unit=materia.nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="linear_spline")

    assert line.x == x_interp_to
    assert line.y == 2 * x_interp_to


# def test_spd_spectrum_interpolate_sprague_linear():
#     materia.nanometer = units.Unit('materia.nanometer')
#
#     x = materia.Qty(value=np.linspace(1,10,10),unit=materia.nanometer)
#     y = 2*x
#     line = SPDSpectrum(x=x,y=y)
#
#     x_interp_to = materia.Qty(value=np.linspace(1,10,19),unit=materia.nanometer)
#     line.interpolate(x_interp_to=x_interp_to,method='sprague')
#
#     assert line.x == x_interp_to
#     assert line.y == 2*x_interp_to


def test_spd_spectrum_extrapolate_quadratic():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = x ** 2
    line = SPDSpectrum(x=x, y=y)

    x_extrap_to = materia.Qty(value=np.linspace(0, 15, 16), unit=materia.nanometer)

    line.extrapolate(x_extrap_to=x_extrap_to)

    check_result_x = x_extrap_to
    check_result_y = materia.Qty(
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
        unit=materia.nanometer ** 2,
    )

    assert line.x == check_result_x
    assert line.y == check_result_y


def test_spd_spectrum_interpolate_cubic_spline_quadratic():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = x ** 2
    line = SPDSpectrum(x=x, y=y)

    x_interp_to = materia.Qty(value=np.linspace(1, 10, 19), unit=materia.nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="cubic_spline")

    assert line.x == x_interp_to
    assert line.y == x_interp_to ** 2


def test_spd_spectrum_interpolate_linear_spline_quadratic():
    x = materia.Qty(value=np.linspace(1, 10, 10), unit=materia.nanometer)
    y = x ** 2
    line = SPDSpectrum(x=x, y=y)

    x_interp_to = materia.Qty(value=np.linspace(1, 10, 19), unit=materia.nanometer)
    line.interpolate(x_interp_to=x_interp_to, method="linear_spline")

    check_result_x = x_interp_to
    check_result_y = materia.Qty(
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
        unit=materia.nanometer ** 2,
    )

    assert line.x == check_result_x
    assert line.y == check_result_y
