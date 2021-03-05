import collections
import unittest.mock as mock
import numpy as np
import pytest

import materia as mtr


class StructureTestClass(mtr.Structure):
    def __init__(self, *atoms):
        self.atoms = atoms

    def atoms(self):
        return self.atoms


def test_structure_he():
    he = StructureTestClass(
        mtr.Atom(
            element="He",
            position=(0.000, 0.000, 0.000) * mtr.angstrom,
        )
    )

    check_result_center_of_mass = np.array([[0.0, 0.0, 0.0]]).T * mtr.angstrom

    check_result_inertia_tensor = (
        np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        * mtr.amu
        * mtr.angstrom ** 2
    )

    assert he.center_of_mass == check_result_center_of_mass
    assert np.allclose(he.inertia_tensor.value, check_result_inertia_tensor.value)


def test_structure_h2o():
    h1 = mtr.Atom(
        element="H",
        position=(0.757, 0.586, 0.000) * mtr.angstrom,
    )
    h2 = mtr.Atom(
        element="H",
        position=(-0.757, 0.586, 0.000) * mtr.angstrom,
    )
    o = mtr.Atom(
        element="O",
        position=(0.000, 0.000, 0.000) * mtr.angstrom,
    )
    h2o = StructureTestClass(h1, h2, o)

    check_result_center_of_mass = (
        np.array([[0.0, 0.06557735220649459, 0.0]]).T * mtr.angstrom
    )

    check_result_inertia_tensor = (
        np.array(
            [
                [0.61481483, 0.0, 0.0],
                [0.0, 1.15526678, 0.0],
                [0.0, 0.0, 1.77008161],
            ]
        )
        * mtr.amu
        * mtr.angstrom ** 2
    )

    assert np.allclose(h2o.center_of_mass.value, check_result_center_of_mass.value)
    assert pytest.approx(h2o.center_of_mass.prefactor) == pytest.approx(
        check_result_center_of_mass.prefactor
    )
    assert h2o.center_of_mass.dimension == check_result_center_of_mass.dimension
    assert np.allclose(h2o.inertia_tensor.value, check_result_inertia_tensor.value)
    assert pytest.approx(h2o.inertia_tensor.prefactor) == pytest.approx(
        check_result_inertia_tensor.prefactor
    )
    assert h2o.inertia_tensor.dimension == check_result_inertia_tensor.dimension


def test_structure_generate_no_kwargs():
    try:
        mtr.Structure.generate()
        assert False
    except ValueError:
        assert True


def test_structure_retrieve_no_kwargs():
    try:
        mtr.Structure.retrieve()
        assert False
    except ValueError:
        assert True


def test_structure_retrieve_smiles():
    Atom = collections.namedtuple("Atom", ["element", "x", "y", "z"])
    Compound = collections.namedtuple("Compound", ["atoms"])

    C = Atom(element="C", x=0, y=0, z=0)
    H1 = Atom(element="H", x=1, y=0, z=0)
    H2 = Atom(element="H", x=0, y=1, z=0)
    H3 = Atom(element="H", x=0, y=0, z=1)
    H4 = Atom(element="H", x=0, y=1, z=1)
    methane = Compound(atoms=(C, H1, H2, H3, H4))

    mock_pcp_get_cids = mock.MagicMock(
        side_effect=lambda identifier, identifier_type: [
            1,
        ]
    )
    mock_pcp_from_cid = mock.MagicMock(
        side_effect=lambda cid, record_type="3d": methane
    )
    mock_pcp_get_properties = mock.MagicMock(
        side_effect=lambda properties, identifier, namespace: "C"
    )

    with mock.patch("pubchempy.get_cids", mock_pcp_get_cids):
        with mock.patch("pubchempy.Compound.from_cid", mock_pcp_from_cid):
            with mock.patch("pubchempy.get_properties", mock_pcp_get_properties):
                structure = mtr.Structure.retrieve(smiles="C")

    assert np.allclose(
        structure.atomic_positions.value,
        np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1]]),
    )
    assert structure.atomic_positions.unit == mtr.angstrom
    assert structure.atomic_symbols == ("C", "H", "H", "H", "H")


# FIXME: output of the following test is stochastic, specifically the atomic positions!
# in particular, output sometimes changes when new tests are added
# def test_structure_generate_smiles():
#     structure = mtr.Structure.generate(smiles="C")
#     print(structure.atomic_positions.value)
#     assert False
#     assert np.allclose(
#         structure.atomic_positions.value,
#         np.array(
#             [
#                 [-0.0054988, -0.6511159, -0.42682758, 0.10940617, 0.9740361],
#                 [-0.00553635, -0.84701178, 0.92029355, 0.09999218, -0.16773759],
#                 [0.00735998, -0.25430294, -0.40297592, 1.09967445, -0.44975557],
#             ]
#         ),
#     )
#     assert structure.atomic_positions.unit == mtr.angstrom
#     assert structure.atomic_symbols == ("C", "H", "H", "H", "H")
