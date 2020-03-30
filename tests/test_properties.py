import materia as mtr
import numpy as np


def test_property_dipole():
    d = mtr.Dipole(dipole_moment=(1, 4, 3) * mtr.au_dipole_moment)

    check_result = 5.0990195135927845 * mtr.au_dipole_moment

    assert d.norm == check_result


def test_property_polarizability():
    # FIXME: find a logical system for rounding accuracy in assert statements!
    x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    polarizability_tensor = x * mtr.au_dipole_moment / (mtr.volt / mtr.meter)
    p = mtr.Polarizability(polarizability_tensor=polarizability_tensor)

    check_result_isotropic = 5 * mtr.au_dipole_moment / (mtr.volt / mtr.meter)
    check_result_anisotropy = (
        np.sqrt(186) * mtr.au_dipole_moment / (mtr.volt / mtr.meter)
    )
    check_result_eigenvalues = (
        (16.116843969807043, -1.1168439698070416, -9.759184829871139e-16)
        * mtr.au_dipole_moment
        / (mtr.volt / mtr.meter)
    )

    assert np.allclose(p.isotropic.value, check_result_isotropic.value)
    assert p.isotropic.unit == check_result_isotropic.unit
    assert np.allclose(p.anisotropy.value, check_result_anisotropy.value)
    assert p.anisotropy.unit == check_result_anisotropy.unit
    assert np.allclose(p.eigenvalues.value, check_result_eigenvalues.value)
    assert p.eigenvalues.unit == check_result_eigenvalues.unit
