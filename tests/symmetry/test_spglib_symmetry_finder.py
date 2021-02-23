import numpy as np

import materia as mtr


class StructureTestClass(mtr.Structure):
    def __init__(self, *atoms):
        setattr(self, "atoms", atoms)

    def atoms(self):
        return self.atoms


def test_align_axes_with_molecule_he():
    ssf = mtr.SpglibSymmetryFinder()

    test_result = ssf._align_rotations_with_molecule(
        inertia_tensor=np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    )

    check_result = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    assert (test_result == check_result).all()


def test_align_axes_with_molecule_h2o_norot():
    ssf = mtr.SpglibSymmetryFinder()

    test_result = ssf._align_rotations_with_molecule(
        inertia_tensor=np.array(
            [
                [0.6148148259597002, 0.0, 0.0],
                [0.0, 1.1552667840000002, 0.0],
                [0.0, 0.0, 1.7700816099597003],
            ]
        )
    )

    check_result = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    assert (test_result == check_result).all()


def test_align_axes_with_molecule_h2o_rot():
    ssf = mtr.SpglibSymmetryFinder()

    test_result = ssf._align_rotations_with_molecule(
        inertia_tensor=np.array(
            [
                [0.6148148259597002, 0.0, 0.0],
                [0.0, 1.7700816099597003, 0.0],
                [0.0, 0.0, 1.1552667840000002],
            ]
        )
    )

    check_result = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])

    assert (test_result == check_result).all()


def test_molecular_pointgroup_h2o_norot():
    ssf = mtr.SpglibSymmetryFinder()

    o = mtr.Atom(element="O", position=(0.000, 0.000, 0.000) * mtr.angstrom)
    h1 = mtr.Atom(element="H", position=(0.757, 0.586, 0.000) * mtr.angstrom)
    h2 = mtr.Atom(element="H", position=(-0.757, 0.586, 0.000) * mtr.angstrom)
    h2o = mtr.Molecule(StructureTestClass(o, h1, h2))

    test_result = ssf.molecular_pointgroup(molecule=h2o)

    check_result = "C2v"

    assert test_result == check_result


def test_symfinder_molecular_pointgroup_h2o_rot():
    ssf = mtr.SpglibSymmetryFinder()

    o = mtr.Atom(element="O", position=(0.000, 0.000, 0.000) * mtr.angstrom)
    h1 = mtr.Atom(element="H", position=(0.757, 0.000, 0.586) * mtr.angstrom)
    h2 = mtr.Atom(element="H", position=(-0.757, 0.000, 0.586) * mtr.angstrom)
    h2o = mtr.Molecule(StructureTestClass(o, h1, h2))

    test_result = ssf.molecular_pointgroup(molecule=h2o)

    check_result = "C2v"

    assert test_result == check_result
