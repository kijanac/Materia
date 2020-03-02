import numpy as np

import materia as mtr

yz_swap = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
xy_plane_reflection = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])


def geometry_perpendicular_vector():
    # FIXME: expand
    assert (
        mtr.perpendicular_vector(a=np.array([[1, 0, 0]]).T) == np.array([[0, 1, 0]]).T
    ).all()


def test_geometry_rotation_matrix_m_to_n():
    assert (
        mtr.rotation_matrix_m_to_n(
            m=np.array([[1.0, 0, 0]]).T, n=np.array([[1.0, 0, 0]]).T
        )
        == np.eye(3)
    ).all()
    assert (
        mtr.rotation_matrix_m_to_n(
            m=np.array([[1.0, 0, 0]]).T, n=np.array([[0, 1.0, 0]]).T
        )
        == np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    ).all()


def test_geometry_nontrivial_vector():
    v = mtr.nontrivial_vector(R=yz_swap, seed=42809437)
    assert not (yz_swap @ v == v).all()

    v = mtr.nontrivial_vector(R=xy_plane_reflection, seed=42809437)
    assert not (xy_plane_reflection @ v == v).all()

    v = mtr.nontrivial_vector(R=yz_swap, seed=139856018)
    assert not (yz_swap @ v == v).all()

    v = mtr.nontrivial_vector(R=xy_plane_reflection, seed=139856018)
    assert not (xy_plane_reflection @ v == v).all()


def test_geometry_closest_trio():
    # FIXME: expand
    points = np.array([[1, 0, 0], [0, 0, 0], [1e-4, 0, 0], [1e-3, 0, 0]]).T
    assert (mtr.closest_trio(points=points) == points[:, 1:]).all()
