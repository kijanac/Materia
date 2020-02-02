import materia


def test_nwchem_full():
    top_params = {
        "title": "anthracene",
        "echo": True,
        "scratch_dir": "./scratch",
        "permanent_dir": "./results",
        "memory_params": {"total_mem": 1000, "total_units": "mb"},
        "start": True,
    }
    geometry_params = {"title": "system", "xyz_filepath": "geom.xyz", "autosym": False}
    set_geometry_params = {
        "set_params": {"variable_name": "geometry", "variable_value": '"system"'}
    }
    basis_params = {"atom_strings": ("*",), "library_strings": ("6-311G**",)}
    dft_params = {"direct": True, "xc_params": {"xc_functional_strings": ("b3lyp",)}}
    property_params = {"response_order": 1, "response_frequency": 0}
    dft_task_params = {"task_params": {"theory_level": "dft", "operation": "property"}}

    inp = materia.NWChemInput()
    inp.add_block(top=top_params)
    inp.add_block(geometry=geometry_params)
    inp.add_block(top=set_geometry_params)
    inp.add_block(basis=basis_params)
    inp.add_block(dft=dft_params)
    inp.add_block(property=property_params)
    inp.add_block(top=dft_task_params)

    check_result = 'title "anthracene"\n'
    check_result += "echo\n"
    check_result += "scratch_dir ./scratch\n"
    check_result += "permanent_dir ./results\n"
    check_result += "memory total 1000 mb\n"
    check_result += 'start "anthracene"\n'
    check_result += "\n"
    check_result += 'geometry "system" units angstroms center noautosym autoz\n'
    check_result += '  LOAD "geom.xyz"\n'
    check_result += "end\n"
    check_result += "\n"
    check_result += 'set geometry "system"\n'
    check_result += "\n"
    check_result += "basis cartesian segment print\n"
    check_result += "  * library 6-311G**\n"
    check_result += "end\n"
    check_result += "\n"
    check_result += "dft\n"
    check_result += "  direct\n"
    check_result += "  xc b3lyp\n"
    check_result += "end\n"
    check_result += "\n"
    check_result += "property\n"
    check_result += "  response 1 0\n"
    check_result += "end\n"
    check_result += "\n"
    check_result += "task dft property"

    assert str(inp) == check_result


def test_nwchem_input_empty():
    inp = materia.NWChemInput()

    assert str(inp) == ""


def test_nwchem_input_cosmo():
    cosmo_params = {
        "dielec": 2.0,
        "parameters_file": "water.par",
        "radii": (1, 2, 3),
        "iscren": 1,
        "minbem": 3,
        "ificos": 1,
        "lineq": 1,
        "zeta": 1.0,
        "gamma_s": 0.0,
        "sw_tol": 1e-05,
        "do_gasphase": False,
        "do_cosmo_ks": True,
        "do_cosmo_yk": False,
    }

    inp = materia.NWChemInput()
    inp.add_block(cosmo=cosmo_params)

    check_result = "cosmo\n"
    check_result += "  dielec 2.0\n"
    check_result += "  parameters water.par\n"
    check_result += "  radius 1\n"
    check_result += "         2\n"
    check_result += "         3\n"
    check_result += "  iscren 1\n"
    check_result += "  minbem 3\n"
    check_result += "  ificos 1\n"
    check_result += "  lineq 1\n"
    check_result += "  zeta 1.0\n"
    check_result += "  gamma_s 0.0\n"
    check_result += "  sw_tol 1e-05\n"
    check_result += "  do_gasphase False\n"
    check_result += "  do_cosmo_ks True\n"
    check_result += "  do_cosmo_yk False\n"
    check_result += "end"

    assert str(inp) == check_result


def test_nwchem_input_property_cosmo():
    property_params = {
        "nbofile": True,
        "dipole": True,
        "quadrupole": True,
        "octupole": True,
        "mulliken": True,
        "esp": True,
        "efield": True,
        "efieldgrad": True,
        "efieldgradz4": True,
        "gshift": True,
        "aimfile": True,
        "moldenfile": True,
        "molden_norm": "janpa",
        "electrondensity": True,
        "vectors_filename": "h2o.movecs",
        "hyperfine_num_atoms": 3,
        "hyperfine_atoms": (1, 2, 3),
        "shielding_num_atoms": 2,
        "shielding_atoms": (1, 2),
        "spinspin_num_pairs": 3,
        "spinspin_atom_pairs": ((6, 7), (8, 9), (10, 11)),
        "response_order": 1,
        "response_frequency": 1e-3,
        "response_gauge": "velocity",
        "response_damping": 5e-4,
        "response_convergence": 1e-4,
        "response_orbeta": True,
        "response_giao": True,
        "response_bdtensor": True,
        "response_analysis": True,
        "all": True,
        "center": "arb",
        "center_coords": (0.0, 0.0, 0.0),
    }
    cosmo_params = {
        "dielec": 2.0,
        "parameters_file": "water.par",
        "radii": (1, 2, 3),
        "iscren": 1,
        "minbem": 3,
        "ificos": 1,
        "lineq": 1,
        "zeta": 1.0,
        "gamma_s": 0.0,
        "sw_tol": 1e-05,
        "do_gasphase": False,
        "do_cosmo_ks": True,
        "do_cosmo_yk": False,
    }

    inp = materia.NWChemInput()
    inp.add_block(property=property_params)
    inp.add_block(cosmo=cosmo_params)

    check_result = "property\n"
    check_result += "  nbofile\n"
    check_result += "  dipole\n"
    check_result += "  quadrupole\n"
    check_result += "  octupole\n"
    check_result += "  mulliken\n"
    check_result += "  esp\n"
    check_result += "  efield\n"
    check_result += "  efieldgrad\n"
    check_result += "  efieldgradz4\n"
    check_result += "  gshift\n"
    check_result += "  electrondensity\n"
    check_result += "  hyperfine 3 1 2 3\n"
    check_result += "  shielding 2 1 2\n"
    check_result += "  spinspin 3 6 7 8 9 10 11\n"
    check_result += "  response 1 0.001\n"
    check_result += "  velocity\n"
    check_result += "  damping 0.0005\n"
    check_result += "  convergence 0.0001\n"
    check_result += "  orbeta\n"
    check_result += "  giao\n"
    check_result += "  bdtensor\n"
    check_result += "  analysis\n"
    check_result += "  vectors h2o.movecs\n"
    check_result += "  center 0.0 0.0 0.0\n"
    check_result += "  aimfile True\n"
    check_result += "  moldenfile True\n"
    check_result += "  molden_norm janpa\n"
    check_result += "  all\n"
    check_result += "end\n"
    check_result += "\n"
    check_result += "cosmo\n"
    check_result += "  dielec 2.0\n"
    check_result += "  parameters water.par\n"
    check_result += "  radius 1\n"
    check_result += "         2\n"
    check_result += "         3\n"
    check_result += "  iscren 1\n"
    check_result += "  minbem 3\n"
    check_result += "  ificos 1\n"
    check_result += "  lineq 1\n"
    check_result += "  zeta 1.0\n"
    check_result += "  gamma_s 0.0\n"
    check_result += "  sw_tol 1e-05\n"
    check_result += "  do_gasphase False\n"
    check_result += "  do_cosmo_ks True\n"
    check_result += "  do_cosmo_yk False\n"
    check_result += "end"

    assert str(inp) == check_result


def test_nwchem_rttddft_empty():
    rttddft = materia.NWChemRTTDDFTBlock()

    check_result = "rttddft\n"
    check_result += "end\n"

    assert str(rttddft) == check_result


def test_nwchem_rttddft_field_subblock_empty():
    field = materia.NWChemRTTDDFTFieldSubblock()

    check_result = '  field "None"\n'
    check_result += "    type None\n"
    check_result += "    polarization None\n"
    check_result += "  end\n"

    assert str(field) == check_result


def test_nwchem_rttddft_field_subblock_full():
    field = materia.NWChemRTTDDFTFieldSubblock(
        field_name="kick",
        shape="delta",
        polarization="x",
        frequency=5e-2,
        center=393.3,
        width=1e-3,
        max=1e-5,
    )

    check_result = '  field "kick"\n'
    check_result += "    type delta\n"
    check_result += "    polarization x\n"
    check_result += "    frequency 0.05\n"
    check_result += "    center 393.3\n"
    check_result += "    width 0.001\n"
    check_result += "    max 1e-05\n"
    check_result += "  end\n"

    assert str(field) == check_result


def test_nwchem_rttddft_visualization_subblock_empty():
    rttddft_visualization_subblock = materia.NWChemRTTDDFTVisualizationSubblock()

    check_result = "  visualization\n"
    check_result += "  end\n"

    assert str(rttddft_visualization_subblock) == check_result


def test_nwchem_rttddft_visualization_subblock_full():
    rttddft_visualization_subblock = materia.NWChemRTTDDFTVisualizationSubblock(
        tstart=0.0, tend=100.0, treference=0.0, dplot=True
    )

    check_result = "  visualization\n"
    check_result += "    tstart 0.0\n"
    check_result += "    tend 100.0\n"
    check_result += "    treference 0.0\n"
    check_result += "    dplot\n"
    check_result += "  end\n"

    assert str(rttddft_visualization_subblock) == check_result


def test_nwchem_rttddft_excite_subblock_empty():
    excite = materia.NWChemRTTDDFTExciteSubblock()

    check_result = '  excite "None" with "None"\n'

    assert str(excite) == check_result


def test_nwchem_rttddft_excite_subblock_full():
    excite = materia.NWChemRTTDDFTExciteSubblock(geometry_name="geom", field_name="kick")

    check_result = '  excite "geom" with "kick"\n'

    assert str(excite) == check_result


def test_nwchem_property_empty():
    prop = materia.NWChemPropertyBlock()

    check_result = "property\n"
    check_result += "end\n"

    assert str(prop) == check_result


def test_nwchem_property_full():
    prop = materia.NWChemPropertyBlock(
        nbofile=True,
        dipole=True,
        quadrupole=True,
        octupole=True,
        mulliken=True,
        esp=True,
        efield=True,
        efieldgrad=True,
        efieldgradz4=True,
        gshift=True,
        aimfile=True,
        moldenfile=True,
        molden_norm="janpa",
        electrondensity=True,
        vectors_filename="h2o.movecs",
        hyperfine_num_atoms=3,
        hyperfine_atoms=(1, 2, 3),
        shielding_num_atoms=2,
        shielding_atoms=(1, 2),
        spinspin_num_pairs=3,
        spinspin_atom_pairs=((6, 7), (8, 9), (10, 11)),
        response_order=1,
        response_frequency=1e-3,
        response_gauge="velocity",
        response_damping=5e-4,
        response_convergence=1e-4,
        response_orbeta=True,
        response_giao=True,
        response_bdtensor=True,
        response_analysis=True,
        all=True,
        center="arb",
        center_coords=(0.0, 0.0, 0.0),
    )

    check_result = "property\n"
    check_result += "  nbofile\n"
    check_result += "  dipole\n"
    check_result += "  quadrupole\n"
    check_result += "  octupole\n"
    check_result += "  mulliken\n"
    check_result += "  esp\n"
    check_result += "  efield\n"
    check_result += "  efieldgrad\n"
    check_result += "  efieldgradz4\n"
    check_result += "  gshift\n"
    check_result += "  electrondensity\n"
    check_result += "  hyperfine 3 1 2 3\n"
    check_result += "  shielding 2 1 2\n"
    check_result += "  spinspin 3 6 7 8 9 10 11\n"
    check_result += "  response 1 0.001\n"
    check_result += "  velocity\n"
    check_result += "  damping 0.0005\n"
    check_result += "  convergence 0.0001\n"
    check_result += "  orbeta\n"
    check_result += "  giao\n"
    check_result += "  bdtensor\n"
    check_result += "  analysis\n"
    check_result += "  vectors h2o.movecs\n"
    check_result += "  center 0.0 0.0 0.0\n"
    check_result += "  aimfile True\n"
    check_result += "  moldenfile True\n"
    check_result += "  molden_norm janpa\n"
    check_result += "  all\n"
    check_result += "end\n"

    assert str(prop) == check_result


def test_nwchem_cosmo_empty():
    cosmo = materia.NWChemCosmoBlock()

    check_result = "cosmo\n"
    check_result += "end\n"

    assert str(cosmo) == check_result


def test_nwchem_cosmo_full():
    cosmo = materia.NWChemCosmoBlock(
        dielec=2.0,
        parameters_file="water.par",
        radii=(1, 2, 3),
        iscren=1,
        minbem=3,
        ificos=1,
        lineq=1,
        zeta=1.0,
        gamma_s=0.0,
        sw_tol=1e-05,
        do_gasphase=False,
        do_cosmo_ks=True,
        do_cosmo_yk=False,
    )

    check_result = "cosmo\n"
    check_result += "  dielec 2.0\n"
    check_result += "  parameters water.par\n"
    check_result += "  radius 1\n"
    check_result += "         2\n"
    check_result += "         3\n"
    check_result += "  iscren 1\n"
    check_result += "  minbem 3\n"
    check_result += "  ificos 1\n"
    check_result += "  lineq 1\n"
    check_result += "  zeta 1.0\n"
    check_result += "  gamma_s 0.0\n"
    check_result += "  sw_tol 1e-05\n"
    check_result += "  do_gasphase False\n"
    check_result += "  do_cosmo_ks True\n"
    check_result += "  do_cosmo_yk False\n"
    check_result += "end\n"

    assert str(cosmo) == check_result
