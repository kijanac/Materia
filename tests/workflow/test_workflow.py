import materia as mtr
import numpy as np
import time

# TEST TASKS


@mtr.task
def f1(x):
    return -(5 + np.exp(-x))


@mtr.task
def f2(x):
    return x ** 4 * np.exp(-x)


class Append(mtr.Task):
    def __init__(self, append_str, name):
        super().__init__(name=name)
        self.append_str = append_str

    def compute(self, s):
        return s + self.append_str


class Combine(mtr.Task):
    def compute(self, s1, s2):
        return s1 + s2


class FirstHalf(mtr.Task):
    def compute(self, s):
        return s[: len(s) // 2]


class Reverse(mtr.Task):
    def compute(self, s):
        return s[::-1]


class Mul(mtr.Task):
    def compute(self, **kwargs):
        return {"product": np.random.randint(10) * np.random.randint(10)}


class Add(mtr.Task):
    def compute(self, a, b):
        x, a = a
        x, b = b
        return x, a + b


class MatMul(mtr.Task):
    def compute(self, a, b):
        return a @ b


class SlowMatMul(mtr.Task):
    def compute(self, a, b):
        time.sleep(0.5)
        return a @ b


class Signal(mtr.Task):
    def compute(self):
        return "Signal triggered successfully."


class SlowSignal(mtr.Task):
    def compute(self):
        time.sleep(0.5)
        return "Signal triggered successfully."


class AddOn(mtr.Task):
    def compute(self):
        return "AddOn triggered successfully."


class PreMulA(mtr.Task):
    def compute(self, a):
        return np.array([[-1, 0], [0, 1]]) @ a


# TESTS


def test_workflow_signal():
    t0, t1, t2, t3, t4, t5, t6 = (
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
    )

    t1.requires(t0)
    t2.requires(t1)
    t4.requires(t3)
    t5.requires(t4)
    t6.requires(t2, t5)

    out = mtr.Workflow(t0, t1, t2, t3, t4, t5, t6).compute()

    assert out == {
        0: "Signal triggered successfully.",
        3: "Signal triggered successfully.",
        7: "AddOn triggered successfully.",
        8: "AddOn triggered successfully.",
        1: "Signal triggered successfully.",
        4: "Signal triggered successfully.",
        9: "AddOn triggered successfully.",
        10: "AddOn triggered successfully.",
        2: "Signal triggered successfully.",
        5: "Signal triggered successfully.",
        11: "AddOn triggered successfully.",
        12: "AddOn triggered successfully.",
        6: "Signal triggered successfully.",
        13: "AddOn triggered successfully.",
    }


def test_workflow_multiply_linear():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))
    mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp1, b=inp0)
    mm2.requires(a=mm0, b=mm1)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
    assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


def test_workflow_multiply_complicated():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))
    mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp1, b=inp0)
    mm2.requires(a=mm0, b=mm1)
    mm3.requires(a=mm1, b=mm2)
    mm4.requires(a=mm3, b=mm0)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
    assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
    assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
    assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


def test_workflow_multiply_topheavy_complicated():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))

    mm0, mm1, mm2, mm3, mm4, mm5 = (
        MatMul(),
        MatMul(),
        MatMul(),
        MatMul(),
        MatMul(),
        MatMul(),
    )
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp0, b=mm0)
    mm2.requires(a=inp0, b=inp1)
    mm3.requires(a=inp0, b=inp1)
    mm4.requires(a=inp0, b=inp1)
    mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
    assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
    assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


def test_workflow_signal_complicated():
    t0, t1, t2, t3, t4, t5, t6 = (
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
        Signal(),
    )

    t1.requires(t0)
    t2.requires(t1)
    t4.requires(t3)
    t5.requires(t4)
    t6.requires(t2, t5)

    out = mtr.Workflow(t0, t1, t2, t3, t4, t5, t6).compute()

    assert out == {
        0: "Signal triggered successfully.",
        3: "Signal triggered successfully.",
        7: "AddOn triggered successfully.",
        8: "AddOn triggered successfully.",
        1: "Signal triggered successfully.",
        4: "Signal triggered successfully.",
        9: "AddOn triggered successfully.",
        10: "AddOn triggered successfully.",
        2: "Signal triggered successfully.",
        5: "Signal triggered successfully.",
        11: "AddOn triggered successfully.",
        12: "AddOn triggered successfully.",
        6: "Signal triggered successfully.",
        13: "AddOn triggered successfully.",
    }


def test_workflow_slow_signal_complicated():
    t0, t1, t2, t3, t4, t5, t6 = (
        SlowSignal(),
        SlowSignal(),
        SlowSignal(),
        SlowSignal(),
        SlowSignal(),
        SlowSignal(),
        SlowSignal(),
    )

    t1.requires(t0)
    t2.requires(t1)
    t4.requires(t3)
    t5.requires(t4)
    t6.requires(t2, t5)

    out = mtr.Workflow(t0, t1, t2, t3, t4, t5, t6).compute()

    assert out == {
        0: "Signal triggered successfully.",
        3: "Signal triggered successfully.",
        7: "AddOn triggered successfully.",
        8: "AddOn triggered successfully.",
        1: "Signal triggered successfully.",
        4: "Signal triggered successfully.",
        9: "AddOn triggered successfully.",
        10: "AddOn triggered successfully.",
        2: "Signal triggered successfully.",
        5: "Signal triggered successfully.",
        11: "AddOn triggered successfully.",
        12: "AddOn triggered successfully.",
        6: "Signal triggered successfully.",
        13: "AddOn triggered successfully.",
    }


def test_workflow_slow_matmul_linear():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))
    mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp1, b=inp0)
    mm2.requires(a=mm0, b=mm1)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
    assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


def test_workflow_slow_multiply_complicated():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))
    mm0, mm1, mm2, mm3, mm4 = (
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
    )
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp1, b=inp0)
    mm2.requires(a=mm0, b=mm1)
    mm3.requires(a=mm1, b=mm2)
    mm4.requires(a=mm3, b=mm0)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
    assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
    assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
    assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


def test_workflow_slow_multiply_topheavy_complicated():
    inp0 = mtr.InputTask(a=np.array([[1, 2], [2, 1]]))
    inp1 = mtr.InputTask(a=np.array([[-3, 1], [-3, 0.5]]))

    mm0, mm1, mm2, mm3, mm4, mm5 = (
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
        SlowMatMul(),
    )
    mm0.requires(a=inp0, b=inp1)
    mm1.requires(a=inp0, b=mm0)
    mm2.requires(a=inp0, b=inp1)
    mm3.requires(a=inp0, b=inp1)
    mm4.requires(a=inp0, b=inp1)
    mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
    out = mtr.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).compute()

    assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
    assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
    assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
    assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
    assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
    assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


def test_workflow_slow_multiply_linear():
    np.random.seed(10198735)

    tasks = (Mul(), Mul(), Mul())
    links = {0: [1], 1: [2], 2: []}
    wf = mtr.Workflow(tasks=tasks, links=links)

    assert wf.compute(numors=2) == {
        0: {"product": 18},
        1: {"product": 16},
        2: {"product": 0},
    }
