import materia as mtr

if __name__ == "__main__":
    f1 = mtr.FunctionTask(lambda x: x ** 2)
    f2 = mtr.FunctionTask(lambda x: x + 1)

    f1.requires(x=10)
    f2.requires(x=f1)

    wf = mtr.Workflow(f1, f2)
    print(wf.run(1))
