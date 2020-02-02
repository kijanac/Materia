import numpy as np

from materia import Atom, Molecule, Structure
import materia.symmetry

from materia.units import angstrom, Qty

yz_swap = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
xy_plane_reflection = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])


def test_validate_axes():
    identity = np.eye(3)
    scaled_identity = 2 * np.eye(3)
    nullity_one = np.array([[1, 0, 0], [1, 0, 0], [0, 0, 1]])
    nullity_two = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    nullity_three = np.zeros((3, 3))

    assert materia.symmetry.symmetric_axes_generator._validate_axes(axes=identity)
    assert materia.symmetry.symmetric_axes_generator._validate_axes(axes=scaled_identity)
    assert not materia.symmetry.symmetric_axes_generator._validate_axes(axes=nullity_one)
    assert not materia.symmetry.symmetric_axes_generator._validate_axes(axes=nullity_two)
    assert not materia.symmetry.symmetric_axes_generator._validate_axes(
        axes=nullity_three
    )


# def test_excluded_circles():
#     excluded_circles = materia.symmetry.symmetric_axes_generator._excluded_circles(A=yz_swap,B=xy_plane_reflection)
#
#     assert (excluded_circles == np.array([[0,0,1,],[0.7071067811865476,-1,0],[0.7071067811865475,0,0]])).all()

# def test_generate_axes_one_symmetry():
#     axgen = SymmetricAxesGenerator(seed=123986)
#
#     axes,A,B = axgen.generate_axes_one_symmetry(R=yz_swap)
#     assert (axes == np.array([[0.5505806938191355,0.5505806938191355,0.6984553103946161],[0.8316914778140536,-0.07176479168167849,-0.5060435650127173],[-0.07176479168167849,0.8316914778140536,-0.5060435650127173]])).all()
#     assert A is not None
#     assert B is None


def test_generate_axes_C1():
    Br = Atom(
        element="Br", position=Qty(value=(-1.66620, -0.55610, 0.10630), unit=angstrom),
    )
    Cl = Atom(
        element="Cl", position=Qty(value=(1.34390, -0.95560, 0.11960), unit=angstrom),
    )
    F = Atom(
        element="F", position=Qty(value=(0.25470, 1.36560, 0.16920), unit=angstrom),
    )
    C = Atom(
        element="C", position=Qty(value=(0.06750, 0.14600, -0.39500), unit=angstrom),
    )
    H = Atom(
        element="H", position=Qty(value=(0.08600, 0.25060, -1.48270), unit=angstrom),
    )
    structure = Structure(atoms=(Br, Cl, F, C, H))

    check_axes = np.eye(3)
    check_A = None
    check_B = None

    test_axes, test_A, test_B = materia.symmetry.generate_axes(
        structure=structure, seed=984164598
    )

    assert (check_axes == test_axes).all()
    assert check_A == test_A
    assert check_B == test_B


def test_generate_axes_Ci():
    Cl1 = Atom(
        element="Cl", position=Qty(value=(-2.11390, 0.46300, -0.36270), unit=angstrom),
    )
    Cl2 = Atom(
        element="Cl", position=Qty(value=(2.11380, -0.46300, -0.36270), unit=angstrom),
    )
    F1 = Atom(
        element="F", position=Qty(value=(-0.56080, -1.24900, 0.73640), unit=angstrom),
    )
    F2 = Atom(
        element="F", position=Qty(value=(0.56070, 1.24890, 0.73640), unit=angstrom),
    )
    C1 = Atom(
        element="C", position=Qty(value=(-0.59860, -0.46500, -0.37370), unit=angstrom),
    )
    C2 = Atom(
        element="C", position=Qty(value=(0.59860, 0.46500, -0.37370), unit=angstrom),
    )
    H1 = Atom(
        element="H", position=Qty(value=(-0.60740, -1.11770, -1.25170), unit=angstrom),
    )
    H2 = Atom(
        element="H", position=Qty(value=(0.60740, 1.11770, -1.25160), unit=angstrom),
    )
    structure = Structure(atoms=(Cl1, Cl2, F1, F2, C1, C2, H1, H2))

    check_axes = np.eye(3)
    check_A = None
    check_B = None

    test_axes, test_A, test_B = materia.symmetry.generate_axes(
        structure=structure, seed=984164598
    )

    assert (check_axes == test_axes).all()
    assert check_A == test_A
    assert check_B == test_B


# def test_generate_axes_C2():
#     check_axes = np.array([[0.6086169959917437,0.6086169959917437,0.0],[0.500064123546683,-0.500064123546683,0.7764092961632936],[0.616052939714984,-0.616052939714984,-0.6302290098299339]])
#     check_A = np.array([[1,0,0],[0,-1,0],[0,0,-1]]).T
#     check_B = None
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B

# def test_generate_axes_Cs():
#     F1 = Atom(element='F',position=Qty(value=(-1.12800,0.26120,0.00000),unit=angstrom))
#     F2 = Atom(element='F',position=Qty(value=(1.12800,0.26120,0.00000),unit=angstrom))
#     N = Atom(element='N',position=Qty(value=(0.00000,-0.52250,0.00000),unit=angstrom))
#     H = Atom(element='H',position=Qty(value=(0.00000,-1.14490,0.80680),unit=angstrom))
#     structure = Structure(atoms=(F2,F2,N,H))
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5850320462111454,-0.5850320462111454,-2.3085970485894903e-16],[0.8110101755872119,0.8110101755872119,1.6653345369377348e-16],[0.0,-2.701206510426641e-16,1.0]])
#     check_A = np.array([[-1.0,1.387778780781446e-17,6.162975822039156e-33],[1.387778780781446e-17,1.0,4.440892098500626e-16],[0.0,-3.3306690738754696e-16,1.0]])
#     check_B = None
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B

# def test_generate_axes_C2h():
#     check_axes = np.array([[0.6086169959917437,0.6086169959917437,0.0],[0.500064123546683,-0.500064123546683,0.7764092961632936],[0.616052939714984,-0.616052939714984,-0.6302290098299339]])
#     check_A = np.array([[1,0,0],[0,-1,0],[0,0,-1]]).T
#     check_B = None
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B

# def test_generate_axes_C2v():
#     Cl1 = Atom(element='Cl',position=Qty(value=(2.00300,1.61820,-0.00090),unit=angstrom))
#     Cl2 = Atom(element='Cl',position=Qty(value=(2.00390,-1.61750,0.00170),unit=angstrom))
#     C1 = Atom(element='C',position=Qty(value=(0.54000,0.69760,-0.00010),unit=angstrom))
#     C2 = Atom(element='C',position=Qty(value=(0.54040,-0.69720,-0.00100),unit=angstrom))
#     C3 = Atom(element='C',position=Qty(value=(-0.66820,1.39470,0.00080),unit=angstrom))
#     C4 = Atom(element='C',position=Qty(value=(-0.66740,-1.39500,-0.00120),unit=angstrom))
#     C5 = Atom(element='C',position=Qty(value=(-1.87600,0.69700,0.00090),unit=angstrom))
#     C6 = Atom(element='C',position=Qty(value=(-1.87560,-0.69780,-0.00020),unit=angstrom))
#     H1 = Atom(element='H',position=Qty(value=(-0.68710,2.48170,0.00150),unit=angstrom))
#     H2 = Atom(element='H',position=Qty(value=(-0.68590,-2.48200,-0.00150),unit=angstrom))
#     H3 = Atom(element='H',position=Qty(value=(-2.81690,1.23960,0.00160),unit=angstrom))
#     H4 = Atom(element='H',position=Qty(value=(-2.81610,-1.24090,-0.00010),unit=angstrom))
#     structure = Structure(atoms=(Cl1,Cl2,C1,C2,C3,C4,C5,C6,H1,H2,H3,H4))
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,symprec=3,seed=984164598)
#
#     check_axes = np.array([[-0.656322233553044,-0.6559871605837445,-0.6561395568491857],[0.4834714375085587,-0.57487559516455,-0.5796797051326116],[0.579220592570181,0.48907964099263146,-0.4831690401868923]])
#     check_A = np.array([[0.9999998920609756,0.00038958457004489486,0.0002531835302271367],[0.00024955953557012064,0.009274302055615705,-0.9999569615945574],[-0.0003919159034810487,0.9999569168445429,0.009274203830012288]])
#     check_B = np.array([[0.9999999704547695,0.00017194882991273044,0.00017182566705576597],[0.00017194882991407044,-0.0007165179647635957,-0.9999997285177661],[0.00017182566705442509,-0.9999997285177661,0.0007165475099939928]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_C3():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.22274362590154373,0.24743899049007242,-0.9429523970516683],[-0.9429523970516683,0.22274362590154373,0.24743899049007242],[0.24743899049007242,-0.9429523970516683,0.22274362590154373]])
#     check_A = np.array([[0,0,1],[1,0,0],[0,1,0]])
#     check_B = np.array([[0,1,0],[0,0,1],[1,0,0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C3i():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.22274362590154373,0.24743899049007242,-0.9429523970516683],[-0.9429523970516683,0.22274362590154373,0.24743899049007242],[0.24743899049007242,-0.9429523970516683,0.22274362590154373]])
#     check_A = np.array([[0,0,1],[1,0,0],[0,1,0]])
#     check_B = np.array([[0,1,0],[0,0,1],[1,0,0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C3h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.6086169959917437,0.6086169959917437,-0.634837002850988],[0.500064123546683,0.500064123546683,0.7726460896239459],[0.616052939714984,-0.616052939714984,0.0]])
#     check_A = np.array([[1,0,0],[0,1,0],[0,0,-1]])
#     check_B = None
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B
#
# def test_generate_axes_C3v():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.22274362590154373,0.24743899049007242,-0.9429523970516683],[-0.9429523970516683,0.22274362590154373,0.24743899049007242],[0.24743899049007242,-0.9429523970516683,0.22274362590154373]])
#     check_A = np.array([[0,0,1],[1,0,0],[0,1,0]])
#     check_B = np.array([[0,1,0],[0,0,1],[1,0,0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C4():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C4h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C4v():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_C6():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.6086169959917437,-0.6086169959917437,0.634837002850988],[0.500064123546683,-0.500064123546683,-0.7726460896239459],[0.616052939714984,0.616052939714984,0.0]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = None
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B
#
# def test_generate_axes_C6h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.6086169959917437,-0.6086169959917437,0.634837002850988],[0.500064123546683,-0.500064123546683,-0.7726460896239459],[0.616052939714984,0.616052939714984,0.0]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = None
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert check_B == test_B
#
# def test_generate_axes_C6v():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.1851385974695784,-0.1851385974695784,0.5350701736805461],[0.5350701736805461,-0.5350701736805461,0.1851385974695784],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[0,1,0],[1,0,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D2():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D2d():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D2h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D3():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.22274362590154373,0.24743899049007242,-0.9429523970516683],[-0.9429523970516683,0.22274362590154373,0.24743899049007242],[0.24743899049007242,-0.9429523970516683,0.22274362590154373]])
#     check_A = np.array([[0,0,1],[1,0,0],[0,1,0]])
#     check_B = np.array([[0,1,0],[0,0,1],[1,0,0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D3d():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.22274362590154373,0.24743899049007242,-0.9429523970516683],[-0.9429523970516683,0.22274362590154373,0.24743899049007242],[0.24743899049007242,-0.9429523970516683,0.22274362590154373]])
#     check_A = np.array([[0,0,1],[1,0,0],[0,1,0]])
#     check_B = np.array([[0,1,0],[0,0,1],[1,0,0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D3h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.7578137995820899,-0.4078822233711221,0.7578137995820899],[-0.4078822233711221,0.7578137995820899,-0.4078822233711221],[0.5092645059502834,-0.5092645059502834,-0.5092645059502834]])
#     check_A = np.array([[0,1,0],[1,0,0],[0,0,-1]])
#     check_B = np.array([[1,0,0],[0,1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D4():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D4h():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_D6():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.9429523970516682,0.9429523970516682,0.22274362590154373],[-0.22274362590154373,0.22274362590154373,0.9429523970516682],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[0,-1,0],[-1,0,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_D6h():
#     C1 = Atom(element='C',position=Qty(value=(-0.000000,-0.000000,1.392262),unit=angstrom))
#     C2 = Atom(element='C',position=Qty(value=(-0.000000,1.205786,0.696131),unit=angstrom))
#     C3 = Atom(element='C',position=Qty(value=( 0.000000,1.205786,-0.696131),unit=angstrom))
#     C4 = Atom(element='C',position=Qty(value=( 0.000000,-0.000000,-1.392262),unit=angstrom))
#     C5 = Atom(element='C',position=Qty(value=(-0.000000,-1.205786,-0.696131),unit=angstrom))
#     C6 = Atom(element='C',position=Qty(value=(-0.000000,-1.205786,0.696131),unit=angstrom))
#     H1 = Atom(element='H',position=Qty(value=(-0.000000,-0.000000,2.478709),unit=angstrom))
#     H2 = Atom(element='H',position=Qty(value=(-0.000000,2.146614,1.239449),unit=angstrom))
#     H3 = Atom(element='H',position=Qty(value=( 0.000000,2.146614,-1.239449),unit=angstrom))
#     H4 = Atom(element='H',position=Qty(value=( 0.000000,-0.000000,-2.478709),unit=angstrom))
#     H5 = Atom(element='H',position=Qty(value=(-0.000000,-2.146614,-1.239449),unit=angstrom))
#     H6 = Atom(element='H',position=Qty(value=(-0.000000,-2.146614,1.239449),unit=angstrom))
#     structure = Structure(atoms=(C1,C2,C3,C4,C5,C6,H1,H2,H3,H4,H5,H6))
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.9429523970516682,0.9429523970516682,0.22274362590154373],[-0.22274362590154373,0.22274362590154373,0.9429523970516682],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[0,-1,0],[-1,0,0],[0,0,-1]])
#
#     print([[x for x in v] for v in test_axes])
#     print([[x for x in v] for v in test_A])
#     print([[x for x in v] for v in test_B])
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_O():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_Oh():
#     S = Atom(element='S',position=Qty(value=(0.00000,0.00000,0.00000),unit=angstrom))
#     F1 = Atom(element='F',position=Qty(value=(0.000000,0.000000,1.575382),unit=angstrom))
#     F2 = Atom(element='F',position=Qty(value=(0.000000,1.575382,0.000000),unit=angstrom))
#     F3 = Atom(element='F',position=Qty(value=(0.000000,0.000000,-1.575382),unit=angstrom))
#     F4 = Atom(element='F',position=Qty(value=(-1.575382,0.000000,0.000000),unit=angstrom))
#     F5 = Atom(element='F',position=Qty(value=(1.575382,0.000000,0.000000),unit=angstrom))
#     F6 = Atom(element='F',position=Qty(value=(0.000000,-1.575382,0.000000),unit=angstrom))
#     structure = Structure(atoms=(S,F1,F2,F3,F4,F5,F6))
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     # check_axes = np.array([[-0.24743899049007242,-0.5092645059502834,0.24743899049007242],[0.5092645059502834,-0.24743899049007242,-0.5092645059502834],[-0.8242715626324055,-0.8242715626324055,-0.8242715626324055]])
#     # check_A = np.array([[0,-1,0],[1,0,0],[0,0,1]])
#     # check_B = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_axes = np.array([[-0.2516323578563435,0.2516323578563435,-0.46944053794628043],[0.9591622969429394,0.9591622969429394,0.8502582068979709],[0.1291853110953476,0.1291853110953476,0.23808940114031585]])
#     check_A = np.array([[-1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
#     check_B = np.array([[-0.33333333333333326,-0.6666666666666671,0.6666666666666666],[-0.666666666666667,0.6666666666666663,0.3333333333333337],[0.6666666666666667,0.33333333333333337,0.6666666666666666]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_S4():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[-0.24743899049007242,0.24743899049007242,0.5092645059502834],[0.5092645059502834,-0.5092645059502834,0.24743899049007242],[-0.8242715626324055,-0.8242715626324055,0.8242715626324055]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[0,1,0],[-1,0,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
#
# def test_generate_axes_T():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_Td():
#     C = Atom(element='C',position=Qty(value=(0.00000,0.00000,0.00000),unit=angstrom))
#     H1 = Atom(element='H',position=Qty(value=(0.00000,0.00000,1.08900),unit=angstrom))
#     H2 = Atom(element='H',position=Qty(value=(1.02672,0.00000,-0.36300),unit=angstrom))
#     H3 = Atom(element='H',position=Qty(value=(-0.51336,-0.88916,-0.36300),unit=angstrom))
#     H4 = Atom(element='H',position=Qty(value=(-0.51336,0.88916,-0.36300),unit=angstrom))
#     structure = Structure(atoms=(C,H1,H2,H3,H4))
#
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     # check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     # check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     # check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#     check_axes = np.array([[-0.2742571927037992,-0.2742571927037992,0.9240147234491685],[-0.9086178346002285,0.9086178346002287,-0.2167952212400773],[0.314954953757871,0.3149549537578709,0.314954953757871]])
#     check_A = np.array([[1.0,9.58883784164973e-18,1.2398095986385965e-18],[9.588837841649727e-18,-1.0000000000000002,5.551115123125783e-17],[-1.2398095986385967e-18,1.1102230246251565e-16,1.0]])
#     check_B = np.array([[-0.49999999999255595,-0.8660254037887366,1.0218790272412069e-18],[-0.8660254037887366,0.49999999999255584,5.899821314627996e-19],[1.0218790272412069e-18,5.899821314627996e-19,1.0]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()

# def test_generate_axes_Th():
#     test_axes,test_A,test_B = materia.symmetry.generate_axes(structure=structure,seed=984164598)
#
#     check_axes = np.array([[0.5092645059502834,-0.5092645059502834,0.5092645059502834],[0.8242715626324055,-0.8242715626324055,-0.8242715626324055],[0.24743899049007242,0.24743899049007242,-0.24743899049007242]])
#     check_A = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
#     check_B = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#
#     assert (check_axes == test_axes).all()
#     assert (check_A == test_A).all()
#     assert (check_B == test_B).all()
