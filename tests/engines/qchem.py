# def test_structure_he():
#     he = StructureTestClass(
#         mtr.Atom(element="He", position=(0.000, 0.000, 0.000) * mtr.angstrom,)
#     )

#     check_result_center_of_mass = np.array([[0.0, 0.0, 0.0]]).T * mtr.angstrom

#     check_result_inertia_tensor = (
#         np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
#         * mtr.amu
#         * mtr.angstrom ** 2
#     )

#     assert he.center_of_mass == check_result_center_of_mass
#     assert np.allclose(he.inertia_tensor.value, check_result_inertia_tensor.value)