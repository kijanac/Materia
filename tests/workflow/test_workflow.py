import materia as mtr
import numpy as np

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
    def compute(self, a, b):
        return a * b


class Add(mtr.Task):
    def compute(self, a, b):
        x, a = a
        x, b = b
        return x, a + b


class MatMul(mtr.Task):
    def compute(self, a, b):
        return a @ b


# TESTS


def test_workflow_matmul_linear():
    A = np.array([[1, 2], [2, 1]])
    B = np.array([[-3, 1], [-3, 0.5]])

    mm1 = MatMul(name="mm1")
    mm2 = MatMul(name="mm2")
    mm3 = MatMul(name="mm3")

    mm1.requires(a=A, b=B)
    mm2.requires(a=B, b=A)
    mm3.requires(a=mm1, b=mm2)

    results = mtr.Workflow(mm1, mm2, mm3).compute().results

    assert np.allclose(results["mm1"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm2"], np.array([[-1, -5], [-2, -5.5]]))
    assert np.allclose(results["mm3"], np.array([[5, 34], [4, 31.25]]))


def test_workflow_matmul_complicated():
    A = np.array([[1, 2], [2, 1]])
    B = np.array([[-3, 1], [-3, 0.5]])

    mm1 = MatMul(name="mm1")
    mm2 = MatMul(name="mm2")
    mm3 = MatMul(name="mm3")
    mm4 = MatMul(name="mm4")
    mm5 = MatMul(name="mm5")

    mm1.requires(a=A, b=B)
    mm2.requires(a=A, b=B)
    mm3.requires(a=mm1, b=mm2)
    mm4.requires(a=mm2, b=mm3)
    mm5.requires(a=mm4, b=mm1)

    results = mtr.Workflow(mm1, mm2, mm3, mm4, mm5).compute().results

    assert np.allclose(results["mm1"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm2"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm3"], np.array([[63, -13], [58.5, -11.75]]))
    assert np.allclose(results["mm4"], np.array([[-450, 93.5], [-420.75, 87.625]]))
    assert np.allclose(
        results["mm5"], np.array([[3208.5, -666.25], [2998.125, -622.4375]])
    )


def test_workflow_matmul_topheavy_complicated():
    A = np.array([[1, 2], [2, 1]])
    B = np.array([[-3, 1], [-3, 0.5]])

    mm1 = MatMul(name="mm1")
    mm2 = MatMul(name="mm2")
    mm3 = MatMul(name="mm3")
    mm4 = MatMul(name="mm4")
    mm5 = MatMul(name="mm5")
    mm6 = MatMul(name="mm6")

    mm1.requires(a=A, b=B)
    mm2.requires(a=A, b=mm1)
    mm3.requires(a=A, b=B)
    mm4.requires(a=A, b=B)
    mm5.requires(a=A, b=B)
    mm6.requires(a=mm4, b=mm5)

    results = mtr.Workflow(mm1, mm2, mm3, mm4, mm5, mm6).compute().results

    assert np.allclose(results["mm1"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm2"], np.array([[-27, 7], [-27, 6.5]]))
    assert np.allclose(results["mm3"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm4"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm5"], np.array([[-9, 2], [-9, 2.5]]))
    assert np.allclose(results["mm6"], np.array([[63, -13], [58.5, -11.75]]))


def test_workflow_multiply_linear():
    mul1 = Mul(name="mul1")
    mul1.requires(a=2, b=3)

    mul2 = Mul(name="mul2")
    mul2.requires(a=mul1, b=-1)

    mul3 = Mul(name="mul3")
    mul3.requires(a=10, b=mul2)

    wf = mtr.Workflow(mul1, mul2, mul3)
    results = wf.compute().results
    assert results["mul1"] == 6
    assert results["mul2"] == -6
    assert results["mul3"] == -60
