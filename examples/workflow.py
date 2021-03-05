import argparse
import materia as mtr
import dask.distributed
import time


def f(x, y, z):
    time.sleep(10)
    return x * (y - z)


def g(a, b):
    return a + 2 * b


def h(a, b):
    return a + 2 * b


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dask_scratch", type=str)
    args = parser.parse_args()

    t1 = mtr.FunctionTask(f)
    t1.requires(x=13, y=7, z=3)

    t2 = mtr.FunctionTask(g)
    t2.requires(a=t1, b=2)

    t3 = mtr.FunctionTask(h)
    t3.requires(a=11, b=t1)

    w = mtr.Workflow(t2, t3)

    cluster = dask.distributed.LocalCluster()

    with dask.config.set(temporary_directory=args.dask_scratch):
        with dask.distributed.Client(cluster) as client:
            results = w.compute()

            restarted_results = w.compute(restart=results)

    print(results)
    print(restarted_results)
