import ase
import ase.spacegroup
import ase.visualize
import materia as mtr

amm = mtr.Structure.read("~/ammonia.xyz")
basis = ase.Atoms(amm.atomic_symbols, amm.atomic_positions.T)

ase_crystal = ase.spacegroup.crystal(
    basis=basis,
    spacegroup=198,
    cellpar=[4.9621636999999996, 4.9621636999999996, 4.9621636999999996, 90, 90, 90],
    size=(3, 3, 3),
)
ase.io.write("~/ammonia_crystal.xyz", ase_crystal)

crystal = mtr.Structure.read("~/ammonia_crystal.xyz")

atoms = tuple(
    crystal.atoms[k]
    for k, v in crystal.perceive_bonds().items()
    if (crystal.atoms[k].Z == 7 and len(v) == 3)
    or (crystal.atoms[k].Z == 1 and len(v) == 1)
)
bonds = crystal.perceive_bonds()
while len(bonds) > len(atoms):
    bonds = crystal.perceive_bonds()
    atoms = tuple(
        crystal.atoms[k]
        for k, v in crystal.perceive_bonds().items()
        if (crystal.atoms[k].Z == 7 and len(v) == 3)
        or (crystal.atoms[k].Z == 1 and len(v) == 1)
    )
    crystal = mtr.Structure(atoms)

crystal.write("~/good_ammonia_crystal.xyz", overwrite=True)
