import materia as mtr
import numpy as np
import pytest


def test_timeseries_dt_uniform():
    t = np.linspace(0, 10, 101) * mtr.s

    test_result = mtr.TimeSeries(x=t, y=None).dt
    check_result = 0.1 * mtr.s

    assert test_result == check_result


def test_timeseries_dt_nonuniform():
    t_value = np.hstack((np.linspace(0, 10, 101), np.linspace(11, 21, 101)))
    t = t_value * mtr.s

    with pytest.raises(ValueError):
        mtr.TimeSeries(x=t, y=None).dt


def test_timeseries_T():
    t = np.linspace(0, 10, 101) * mtr.s

    test_result = mtr.TimeSeries(x=t, y=None).T
    check_result = 10 * mtr.s

    assert test_result == check_result


def test_timeseries_T_negative_start():
    t = np.linspace(-10, 10, 101) * mtr.s

    test_result = mtr.TimeSeries(x=t, y=None).T
    check_result = 20 * mtr.s

    assert test_result == check_result
