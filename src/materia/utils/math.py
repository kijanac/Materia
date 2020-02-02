from __future__ import annotations
import math
import numpy as np
import scipy.linalg
from typing import Iterable

__all__ = ["lcm", "periodicity"]


def periodicity(matrix) -> int:
    # if A is periodic, then its eigenvalues are roots of unity, and its periodicity is the lcm of the periodicities of these roots of unity
    # kth roots of unity form the vertices of a regular k-gon with internal angles 2*pi/k
    # the angle between two such vertices z1=a+jb and z2=c+jd is given by cos(theta) = a*c + b*d = Re(z1*conj(z2))
    # choose z2 = z1**2 (clearly z2 is still a root of unity); then z1*conj(z2) = exp(2*pi*j/k)*exp(-4*pi*j/k) = exp(-2*pi*j/k)
    # then Re(z1*conj(z2)) = Re(exp(-2*pi*j/k)) = cos(2*pi*j/k) = Re(z1)
    # so 2*pi*j/k = arccos(Re(z1)) -> j/k = arccos(Re(z1))/(2*pi), and k = lcm(k/j1, k/j2,...)
    evals = scipy.linalg.eigvals(matrix)
    angles = (max(min(z.real, 1), -1) for z in evals if not np.isclose(z, 1))
    # if z is close to 1, then it contributes a period of 1, which doesn't impact the lcm and therefore the final period
    periods = (int((2 * np.pi / np.arccos(angle)).round()) for angle in angles)

    try:
        return lcm(numbers=periods)
    except ValueError:  # periods must not have any values in it, so all evals must have been close to 1
        return 1


def lcm(numbers: Iterable[int]) -> int:
    a, *b = numbers
    if len(b) > 1:
        return lcm(numbers=(a, lcm(numbers=b)))
    else:
        [b] = b
        return a * b // math.gcd(a, b)
