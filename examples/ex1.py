import argparse
import materia as mtr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--packmol", metavar="packmol", type=str, default="packmol")
    args = parser.parse_args()

    packmol = mtr.Packmol(args.packmol)

    pack = mtr.PackmolSolvate(
        shells=3,
        tolerance=2.0,
        engine=packmol,
        io=mtr.IO("pack.in", "pack.out", temp=True),
        mass_density=789 * mtr.kg / mtr.m ** 3,
    )
    solute = mtr.Structure.generate(
        smiles="CCN1C(=CC=CC2=[N+](C3=CC=CC=C3C=C2)CC)C=CC4=CC=CC=C41.[I-]"
    )
    solvent = mtr.Structure.retrieve(name="ethanol")

    pack.requires(solute=solute, solvent=solvent)

    results = mtr.Workflow(pack).run(available_cores=1)
    print(results)
