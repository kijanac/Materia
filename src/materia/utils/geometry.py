import numpy as np
import scipy.linalg, scipy.spatial

import materia.utils


def closest_trio(points):
    """
    Finds the three closest points from a given list of points.

    Parameters
    ----------
    points : numpy.ndarray
        3xNp Numpy array whose columns represent points on the unit sphere, where Np is the number of points.

    Returns
    -------
    numpy.ndarray:
        3x3 Numpy array whose columns are the three closest points from the given list of points.
    """
    tree = scipy.spatial.KDTree(points.T)
    pair = points.T[min(zip(*tree.query(points.T, k=2)), key=lambda t: t[0][1])[1]].T
    return points.T[
        min(zip(*tree.query(pair[:, 0, None].T, k=3)), key=lambda t: t[0][1])[1]
    ].T


def linearly_independent(vectors, indep=None):
    # vectors is kxNv array where Nv is number of vectors
    # indep is kxNi array where Ni is number of linearly independent vectors

    if indep is None:
        indep = np.array([])

    k, *_ = vectors.shape  # dimension of vectors
    *_, n = indep.shape  # number of independent vectors

    if n == k:
        return indep
    else:
        array_generator = (np.vstack([*indep.T, v]) for v in vectors.T)
        try:
            indep = next(
                a
                for a in array_generator
                if scipy.linalg.null_space(a).shape[-1] == k - n - 1
            ).T
            return linearly_independent(vectors=vectors, indep=indep)
        except StopIteration:
            return indep


def nontrivial_vector(R, seed=None):
    """
    Generates a vector which is acted upon nontrivially (i.e. is sent to a linearly independent vector) by the given rotation matrix.

    Parameters
    ----------
    R: numpy.ndarray
        3x3 numpy array representing a rotation matrix.

    Returns
    -------
    numpy.ndarray:
        3x1 numpy array representing a vector which is acted upon nontrivially by R.
    """
    if (
        np.allclose(R, np.eye(R.shape[0]))
        or np.allclose(R, -np.eye(R.shape[0]))
        or np.allclose(R, np.zeros(R.shape[0]))
    ):
        return None

    # get the eigenvectors with real (i.e. 1 or -1) eigenvalues, since these are mapped to colinear vectors by R
    evals, evecs = scipy.linalg.eig(R)  # each column of evecs is an eigenvector of R

    real_eigenbasis = np.real(
        evecs.T[np.isclose(np.imag(evals), 0)].T
    )  # ???: why np.real(evec) instead of simply evec?

    # form the linear combination of the "trivial" eigenvectors
    # get random coefficients between 1 and 2 so that 0 is never chosen
    # the result is guaranteed to be mapped to a linearly independent vector
    # by R because the "trivial" eigenvectors do not all have the same eigenvalues #all have different eigenvalues
    # this is true because R is not proportional to the identity matrix
    with materia.utils.temporary_seed(seed=seed):
        coeffs = np.random.uniform(low=1, high=2, size=(real_eigenbasis.shape[1], 1))

    return normalize(v=real_eigenbasis @ coeffs)


def normalize(v):
    norm = scipy.linalg.norm(v)

    return v / norm if norm > 0 else v


def orthogonal_complement(v, l):
    return normalize(v - np.dot(v.T, l) * l)


def perpendicular_vector(a, b=None):
    """
    Generates a unit vector which is perpendicular to one or two given nonzero vector(s).

    Parameters
    ----------
    a: numpy.ndarray
        3x1 Numpy array representing a nonzero vector.
    b: numpy.ndarray
        3x1 Numpy array representing a nonzero vector.

    Returns
    -------
    numpy.ndarray:
        3x1 Numpy array representing a unit vector which is perpendicular to a (and b, if applicable).
    """
    if b is None:
        m = np.zeros(a.shape)

        ravel_a = np.ravel(a)  # storing in variable for reuse

        i = (ravel_a != 0).argmax()  # index of the first nonzero element of a
        j = next(
            ind for ind in range(len(ravel_a)) if ind != i
        )  # first index of a which is not i
        i, j = (
            np.unravel_index(i, a.shape),
            np.unravel_index(j, a.shape),
        )  # unravel indices for 3x1 arrays m and a

        # make m = np.array([[-ay,ax,0]]).T so np.dot(m.T,a) = -ax*ay + ax*ay = 0
        m[j] = a[i]
        m[i] = -a[j]
    else:
        m = np.cross(a.T, b.T).T

    return normalize(v=m)


def rotation_matrix(axis, cos_theta):
    """
    Generates a matrix which rotates a vector a given angle about a given axis.

    Parameters
    ----------
    axis: numpy.ndarray
        3x1 Numpy array representing the vector whose direction is the axis of rotation.
    cos_theta: float
        Cosine of angle of rotation about the axis of rotation.

    Returns
    -------
    numpy.ndarray:
        3x3 Numpy array representing the rotation matrix which rotates a vector by the given angle about the given axis.
    """
    u1, u2, u3 = np.ravel(normalize(v=axis))

    K = np.array([[0, -u3, u2], [u3, 0, -u1], [-u2, u1, 0]])

    sin_theta = np.sqrt(1 - cos_theta ** 2)

    return (np.eye(3) + sin_theta * K + (1 - cos_theta) * (K @ K)).astype("float64")


def rotation_matrix_m_to_n(m, n):
    """
    Generates a matrix which rotates one given vector to another.

    Parameters
    ----------
    m: numpy.ndarray
        3x1 Numpy array representing the vector to be rotated.
    n: numpy.ndarray
        3x1 Numpy array representing the vector after rotation, i.e. the target vector.

    Returns
    -------
    numpy.ndarray:
        3x3 Numpy array representing the rotation matrix which maps m to n.
    """
    # make rotation axis, which is perpendicular to both m and n
    # no need to normalize, since rotation_matrix will do that for us
    u = np.cross(m.T, n.T).T

    # cosine of the angle between m and n
    c = np.dot(normalize(v=m).T, normalize(v=n))

    return rotation_matrix(axis=u, cos_theta=c)


def sample_spherical_triangle(A, B, C, sin_alpha, sin_beta, sin_gamma, seed=None):
    # see https://www.graphics.cornell.edu/pubs/1995/Arv95c.pdf
    # a, b, and c are cross products of normal vectors, so their magnitudes
    # are the sine of the angles between these normal vectors; these angles
    # are also the angles between planes and therefore the great arcs which
    # define the legs of the triangle; therefore, these angles are also
    # the internal angles of the triangle
    eps = np.finfo(float).eps  # machine precision

    with materia.utils.temporary_seed(seed=seed):
        fraction, cos_theta = np.random.uniform(low=eps, high=1, size=2)

    cos_alpha, cos_beta, cos_gamma = np.sqrt(
        (1 - sin_alpha ** 2, 1 - sin_beta ** 2, 1 - sin_gamma ** 2)
    )

    area = fraction * spherical_excess(
        cos_alpha=cos_alpha, cos_beta=cos_beta, cos_gamma=cos_gamma
    )
    cos_area, sin_area = np.cos(area), np.sin(area)

    s = sin_area * cos_alpha - cos_area * sin_alpha  # sin(area - alpha)
    t = cos_area * cos_alpha + sin_area * sin_alpha  # cos(area - alpha)
    u = t - cos_alpha
    v = s + (cos_gamma + cos_beta * cos_alpha) / sin_beta  # spherical law of cosines

    q = ((v * t - u * s) * cos_alpha - v) / ((v * s + u * t) * sin_alpha)
    C_prime = q * A + np.sqrt(1 - q ** 2) * orthogonal_complement(v=C, l=A)

    z = 1 - cos_theta * (1 - np.dot(C_prime.T, B))
    return z * B + np.sqrt(1 - z ** 2) * orthogonal_complement(v=C_prime, l=B)


def spherical_excess(cos_alpha, cos_beta, cos_gamma):
    # Girard's formula for spherical excess
    return np.arccos((cos_alpha, cos_beta, cos_gamma)).sum() - np.pi


# def plot_lune(self, samples):
#     import matplotlib.pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D
#     xs,ys,zs = samples
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     phigrid,thetagrid = np.mgrid[0.0:np.pi:100j,0.0:2.0*np.pi:100j]
#     xgrid = np.sin(phigrid)*np.cos(thetagrid)
#     ygrid = np.sin(phigrid)*np.sin(thetagrid)
#     zgrid = np.cos(phigrid)
#     ax.plot_surface(xgrid,ygrid,zgrid,rstride=1,cstride=1,color='c',alpha=0.1,linewidth=0)
#     ax.scatter(xs,ys,zs)
#     ax.quiver([0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,-1,0,0],[0,1,0,0,-1,0],[0,0,1,0,0,-1],arrow_length_ratio=0.1,linewidths=[2,2,2,2,2,2])
#     #ax.set_aspect('equal')
#     ax.xaxis._axinfo['juggled'] = (0,0,0)
#     ax.yaxis._axinfo['juggled'] = (1,1,1)
#     ax.zaxis._axinfo['juggled'] = (2,2,2)
#     plt.show(block=True)
