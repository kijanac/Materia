import numpy as np
import scipy


def interpolate(x, y, x_interp_to, method="cubic_spline"):
    if method == "sprague":
        return interpolate_sprague(x=x, y=y, x_interp_to=x_interp_to)
    elif method == "cubic_spline":
        return interpolate_cubic_spline(x=x, y=y, x_interp_to=x_interp_to)
    elif method == "linear_spline":
        return interpolate_linear_spline(x=x, y=y, x_interp_to=x_interp_to)
    else:
        raise ValueError(f"Interpolation method {method} not recognized.")


def interpolate_cubic_spline(x, y, x_interp_to):
    x_lb, *_, x_ub = x
    x_interp = x_interp_to[(x_interp_to >= x_lb) & (x_interp_to <= x_ub)]
    y_interp = scipy.interpolate.CubicSpline(x=x, y=y)(x_interp)

    return x_interp, y_interp


def interpolate_linear_spline(x, y, x_interp_to):
    x_lb, *_, x_ub = x
    x_interp = x_interp_to[(x_interp_to >= x_lb) & (x_interp_to <= x_ub)]
    y_interp = np.interp(x=x_interp, xp=x, fp=y)

    return x_interp, y_interp


def interpolate_sprague(x, y, x_interp_to):
    # FIXME: this implementation of Sprague interpolation is broken somehow!
    # data taken from https://link.springer.com/content/pdf/10.1007/978-3-642-27851-8_366-1.pdf
    # FIXME: we have to convert spec to wavelength spec with nanometer units first
    interp_coeffs = np.array(
        [
            [0, 0, 24, 0, 0, 0],
            [2, -16, 0, 16, -2, 0],
            [-1, -16, -30, 16, -1, 0],
            [-9, 39, 70, 66, -33, 7],
            [13, -64, 126, -124, 61, -12],
            [-5, 25, -50, 50, -25, 5],
        ]
    )
    # Sprague boundary points
    sbp1 = np.dot([884, -1960, 3033, -2648, 1080, 180], y[:6]) / 209
    sbp2 = np.dot([508, -540, 488, -367, 144, -24], y[:6]) / 209
    sbp3 = np.dot([-24, 144, -367, 488, -540, 508], y[-6:]) / 209
    sbp4 = np.dot([-180, 1080, -2648, 3033, -1960, 884], y[-6:]) / 209

    sprague_y = np.hstack([[sbp1, sbp2], y, [sbp3, sbp4]])[:, None]

    poly_c_mat = np.hstack(
        [
            (interp_coeffs @ np.roll(sprague_y, -i)[:6])
            for i in range(len(sprague_y) - 5)
        ]
    )  # [::-1]

    def interp(x_to):
        lower_bound_indices = np.searchsorted(x, x_to) - 1
        scaled_x = (x_to - x[lower_bound_indices]) / (
            x[lower_bound_indices + 1] - x[lower_bound_indices]
        )
        scaled_x_powers = np.vander(x=scaled_x, N=6)
        poly_coeffs = poly_c_mat[:, lower_bound_indices]
        # print(poly_coeffs.shape)
        # print(scaled_x.shape)
        return np.array(
            [
                np.polyval(p=coeffs[::-1], x=X)
                for coeffs, X in zip(poly_coeffs.T, scaled_x)
            ]
        )
        return (scaled_x_powers * poly_coeffs.T).sum(axis=1)

    y_interp = interp(x=x_interp_to)

    return x_interp_to, y_interp
