import numpy as np


def extrapolate(x, y, x_extrap_to):
    # simple linear extrapolation
    x_lb, x_nlb, *_, x_nub, x_ub = x
    y_lb, y_nlb, *_, y_nub, y_ub = y

    # extrapolate down
    m_lb = (y_nlb - y_lb) / (x_nlb - x_lb)
    x_down = x_extrap_to[np.where(x_extrap_to < x_lb)]
    y_down = y_lb + m_lb * (x_down - x_lb)

    # extrapolate up
    m_ub = (y_ub - y_nub) / (x_ub - x_nub)
    x_up = x_extrap_to[np.where(x_extrap_to > x_ub)]
    y_up = y_ub + m_ub * (x_up - x_ub)

    return np.hstack((x_down, x, x_up)), np.hstack((y_down, y, y_up))
