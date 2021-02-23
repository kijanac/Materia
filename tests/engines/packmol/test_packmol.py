import inspect
import materia

# import unittest.mock as mock


def test_packmol_input_one_structure_no_instructions():
    packmol_input = materia.PackmolInput(
        tolerance=1.0,
        filetype="xyz",
        output_name="packed",
    )
    packmol_input.add_structure(structure_filepath="/path/to/structure.xyz", number=300)

    assert (
        str(packmol_input)
        == inspect.cleandoc(
            """tolerance 1.0
                               output packed.xyz
                               filetype xyz\n\n
                               structure /path/to/structure.xyz
                                 number 300
                               end structure"""
        )
        + "\n"
    )
