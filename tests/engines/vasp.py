import numpy as np
import materia as mtr


def test_vasp_input():
    s = mtr.Settings()
    s["incar", "PREC"] = "Normal"
    s["incar", "ENCUT"] = 550
    s["incar", "IBRION"] = -1
    s["incar", "NSW"] = 0
    s["incar", "ISIF"] = 2
    s["incar", "NELMIN"] = 2
    s["incar", "EDIFF"] = 1.0e-5
    s["incar", "EDIFFG"] = -0.02
    s["incar", "VOSKOWN"] = 1
    s["incar", "NBLOCK"] = 1
    s["incar", "NWRITE"] = 1
    s["incar", "NELM"] = 60
    s["incar", "LUSE_VDW"] = True
    s["incar", "LASPH"] = True
    s["incar", "AGGAC"] = 0.0000
    s["incar", "GGA"] = "MK"
    s["incar", "PARAM1"] = 0.1234
    s["incar", "PARAM2"] = 1.0000
    s["incar", "ALGO"] = "Normal (blocked Davidson)"
    s["incar", "ISPIN"] = 2
    s["incar", "INIWAV"] = 1
    s["incar", "ISTART"] = 0
    s["incar", "ICHARG"] = 2
    s["incar", "LWAVE"] = False
    s["incar", "LCHARG"] = False
    s["incar", "ADDGRID"] = False
    s["incar", "ISMEAR"] = 1
    s["incar", "SIGMA"] = 0.2
    s["incar", "LREAL"] = False
    s["incar", "RWIGS"] = (1.17, 0.73)
    s["incar", "LDAU"] = True
    s["incar", "LDAUTYPE"] = 2
    s["incar", "LDAUL"] = (2, -1)
    s["incar", "LDAUU"] = (8.00, 0.00)
    s["incar", "LDAUJ"] = (4.00, 0.00)
    s["incar", "LDAUPRINT"] = 2
    s[
        "poscar", "comment"
    ] = "(Fe2 O3)24  (P1) ~ (COD #9015065)_1_2x2x1_1 0 0 1\
      surface_1 (#1)_2x2x1_1 (MD #5) (VASP)"
    s["poscar", "scaling"] = 1.0
    s["poscar", "bravais_matrix"] = np.hstack(
        [[10.0498, 0, 0], [0, 8.7034, 0], [0, 0, 28.7163]]
    )
    s["poscar", "Direct"] = True
    s["poscar", "num_atoms"] = (48, 72)
    s["kpoints", "comment"] = "Automatic grid"
    s["kpoints", "mesh_type"] = "Gamma"
    s["kpoints", "grid"] = (4, 4, 1)
    s["kpoints", "shift"] = (0.0, 0.0, 0.0)

    vasp_str = """PREC = Normal
ENCUT = 550
IBRION = -1
NSW = 0
ISIF = 2
NELMIN = 2
EDIFF = 1e-05
EDIFFG = -0.02
VOSKOWN = 1
NBLOCK = 1
NWRITE = 1
NELM = 60
LUSE_VDW = .TRUE.
LASPH = .TRUE.
AGGAC = 0.0
GGA = MK
PARAM1 = 0.1234
PARAM2 = 1.0
ALGO = Normal (blocked Davidson)
ISPIN = 2
INIWAV = 1
ISTART = 0
ICHARG = 2
LWAVE = .FALSE.
LCHARG = .FALSE.
ADDGRID = .FALSE.
ISMEAR = 1
SIGMA = 0.2
LREAL = .FALSE.
RWIGS = 1.17 0.73
LDAU = .TRUE.
LDAUTYPE = 2
LDAUL = 2 -1
LDAUU = 8.0 0.0
LDAUJ = 4.0 0.0
LDAUPRINT = 2
(Fe2 O3)24  (P1) ~ (COD #9015065)_1_2x2x1_1 0 0 1  surface_1 (#1)_2x2x1_1 (MD #5) (VASP)
1.0
10.0498  0.0  0.0
0.0  8.7034  0.0
0.0  0.0  28.7163
48 72

Automatic grid
Gamma
4  4  1
0.0  0.0  0.0


"""

    assert str(mtr.VASPInput(s) == vasp_str)
