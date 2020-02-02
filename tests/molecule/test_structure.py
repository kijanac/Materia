import collections
import unittest.mock as mock
import numpy as np

import materia
from materia import Structure


class StructureTestClass(materia.Structure):
    def __init__(self, *atoms):
        self.atoms = atoms

    def atoms(self):
        return self.atoms


def test_structure_he():
    he = StructureTestClass(
        materia.Atom(
            element="He",
            position=materia.Qty(value=(0.000, 0.000, 0.000), unit=materia.angstrom),
        )
    )

    check_result_center_of_mass = materia.Qty(
        np.array([[0.0, 0.0, 0.0]]).T, unit=materia.angstrom
    )
    check_result_inertia_tensor = materia.Qty(
        value=np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]),
        unit=materia.amu * materia.angstrom ** 2,
    )

    assert he.center_of_mass == check_result_center_of_mass
    assert np.allclose(he.inertia_tensor.value, check_result_inertia_tensor.value)
    assert he.inertia_tensor.unit == check_result_inertia_tensor.unit


def test_structure_h2o():
    h1 = materia.Atom(
        element="H",
        position=materia.Qty(value=(0.757, 0.586, 0.000), unit=materia.angstrom),
    )
    h2 = materia.Atom(
        element="H",
        position=materia.Qty(value=(-0.757, 0.586, 0.000), unit=materia.angstrom),
    )
    o = materia.Atom(
        element="O",
        position=materia.Qty(value=(0.000, 0.000, 0.000), unit=materia.angstrom),
    )
    h2o = StructureTestClass(h1, h2, o)

    check_result_center_of_mass = materia.Qty(
        value=np.array([[0.0, 0.06557735220649459, 0.0]]).T, unit=materia.angstrom
    )
    check_result_inertia_tensor = materia.Qty(
        value=np.array(
            [
                [0.6148148259597, 0.0, 0.0],
                [0.0, 1.1552667840000002, 0.0],
                [0.0, 0.0, 1.7700816099597003],
            ]
        ),
        unit=materia.amu * materia.angstrom ** 2,
    )

    assert h2o.center_of_mass == check_result_center_of_mass
    assert np.allclose(h2o.inertia_tensor.value, check_result_inertia_tensor.value)
    assert h2o.inertia_tensor.unit == check_result_inertia_tensor.unit


def test_structure_generate_no_kwargs():
    try:
        materia.Structure.generate()
        assert False
    except ValueError:
        assert True


def test_structure_retrieve_no_kwargs():
    try:
        materia.Structure.retrieve()
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
        side_effect=lambda identifier, identifier_type: [1,]
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
                structure = materia.Structure.retrieve(smiles="C")

    assert np.allclose(
        structure.atomic_positions.value,
        np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1]]),
    )
    assert structure.atomic_positions.unit == materia.angstrom
    assert structure.atomic_symbols == ("C", "H", "H", "H", "H")


def test_structure_generate_smiles():
    structure = materia.Structure.generate(smiles="C")

    assert np.allclose(
        structure.atomic_positions.value,
        np.array(
            [
                [-0.0054988, -0.6511159, -0.42682758, 0.10940617, 0.9740361],
                [-0.00553635, -0.84701178, 0.92029355, 0.09999218, -0.16773759],
                [0.00735998, -0.25430294, -0.40297592, 1.09967445, -0.44975557],
            ]
        ),
    )
    assert structure.atomic_positions.unit == materia.angstrom
    assert structure.atomic_symbols == ("C", "H", "H", "H", "H")
