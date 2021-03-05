import argparse
import materia as mtr
import dask.distributed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qcenv", type=str)
    parser.add_argument("--scratch", type=str)
    parser.add_argument("--dask_scratch", type=str)
    parser.add_argument("--num_evals", type=int)
    args = parser.parse_args()

    m = mtr.Molecule("benzene")

    qchem = mtr.QChem(qcenv=args.qcenv, scratch_dir=args.scratch)

    io = mtr.IO("gs.in", "gs.out", "minimize_koopman_error")

    min_ke = qchem.minimize_koopman_error(io, name="min_ke")
    min_ke.requires(molecule=m, num_evals=args.num_evals)

    wf = mtr.Workflow(min_ke)

    cluster = dask.distributed.LocalCluster()
    with dask.config.set(temporary_directory=args.dask_scratch):
        with dask.distributed.Client(cluster) as client:
            print(wf.compute()["min_ke"])
