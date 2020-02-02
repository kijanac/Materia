import numpy as np
import pytest

import materia


def test_timeseries_dt_uniform():
    t_value = np.linspace(0, 10, 101)
    t = materia.Qty(value=t_value, unit=materia.second)

    test_result = materia.utils.TimeSeries(x=t, y=None).dt
    check_result = materia.Qty(value=0.1, unit=materia.second)

    assert test_result == check_result


def test_timeseries_dt_nonuniform():
    t_value = np.hstack((np.linspace(0, 10, 101), np.linspace(11, 21, 101)))
    t = materia.Qty(value=t_value, unit=materia.second)

    with pytest.raises(ValueError):
        materia.utils.TimeSeries(x=t, y=None).dt


def test_timeseries_T():
    t = materia.Qty(value=np.linspace(0, 10, 101), unit=materia.second)

    test_result = materia.utils.TimeSeries(x=t, y=None).T
    check_result = materia.Qty(value=10, unit=materia.second)

    assert test_result == check_result


def test_timeseries_T_negative_start():
    t_value = np.linspace(-10, 10, 101)
    t = materia.Qty(value=t_value, unit=materia.second)

    test_result = materia.utils.TimeSeries(x=t, y=None).T
    check_result = materia.Qty(value=20, unit=materia.second)

    assert test_result == check_result
