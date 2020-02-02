import numpy as np

import materia


def test_property_dipole():
    d = materia.Dipole(
        dipole_moment=materia.Qty(value=(1, 4, 3), unit=materia.au_dipole_moment)
    )

    check_result = materia.Qty(value=5.0990195135927845, unit=materia.au_dipole_moment)

    assert d.norm == check_result


def test_property_polarizability():
    # FIXME: find a logical system for rounding accuracy in assert statements!
    polarizability_tensor = materia.Qty(
        value=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        unit=materia.au_dipole_moment / (materia.volt / materia.meter),
    )
    p = materia.Polarizability(polarizability_tensor=polarizability_tensor)

    check_result_isotropic = materia.Qty(
        value=5, unit=materia.au_dipole_moment / (materia.volt / materia.meter)
    )
    check_result_anisotropy = materia.Qty(
        value=np.sqrt(186), unit=materia.au_dipole_moment / (materia.volt / materia.meter)
    )
    check_result_eigenvalues = materia.Qty(
        value=(16.116843969807043, -1.1168439698070416, -9.759184829871139e-16),
        unit=materia.au_dipole_moment / (materia.volt / materia.meter),
    )

    assert np.allclose(p.isotropic.value, check_result_isotropic.value)
    assert p.isotropic.unit == check_result_isotropic.unit
    assert np.allclose(p.anisotropy.value, check_result_anisotropy.value)
    assert p.anisotropy.unit == check_result_anisotropy.unit
    assert np.allclose(p.eigenvalues.value, check_result_eigenvalues.value)
    assert p.eigenvalues.unit == check_result_eigenvalues.unit
