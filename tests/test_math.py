import materia as mtr
import numpy as np


def test_divisors_1():
    assert mtr.divisors(1) == [1]


def test_divisors_primes():
    assert mtr.divisors(3) == [1, 3]
    assert mtr.divisors(17) == [1, 17]
    assert mtr.divisors(2099) == [1, 2099]


def test_divisors_composites():
    assert mtr.divisors(4) == [1, 2, 4]
    assert mtr.divisors(60) == [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
    assert mtr.divisors(2000) == [
        1,
        2,
        4,
        5,
        8,
        10,
        16,
        20,
        25,
        40,
        50,
        80,
        100,
        125,
        200,
        250,
        400,
        500,
        1000,
        2000,
    ]


def test_lcm():
    assert mtr.lcm([1, 3]) == 3
    assert mtr.lcm([1, 3, 5]) == 15
    assert mtr.lcm([4, 9, 2, 6, 15]) == 180
    assert mtr.lcm([4, 9, 2, 9, 3, 15]) == 180


def test_nearest_points():
    points = np.array([[1, 0, 0], [0, 0, 1], [0, 0, 2], [0.5, 0.5, 0.5], [10, 3, 4]]).T

    target = np.array([[1, 0, 0], [0.5, 0.5, 0.5]]).tolist()
    result = mtr.nearest_points(points, 2).T.tolist()

    for v in target:
        assert v in result

    target = np.array([[1, 0, 0], [0.5, 0.5, 0.5], [0, 0, 1]]).tolist()
    result = mtr.nearest_points(points, 3).T.tolist()

    for v in target:
        assert v in result

    target = np.array([[1, 0, 0], [0.5, 0.5, 0.5], [0, 0, 1], [0, 0, 2]]).tolist()
    result = mtr.nearest_points(points, 4).T.tolist()

    for v in target:
        assert v in result

    target = points.T.tolist()
    result = mtr.nearest_points(points, 5).T.tolist()

    for v in target:
        assert v in result

    points = np.array(
        [[0.5, 0, 0], [-0.5, 0, 0], [0, 0, 0], [0, 0, 2], [1, 0, 2], [10, 3, 4]]
    ).T

    target = np.array([[0.5, 0, 0], [0, 0, 0]]).tolist()
    result = mtr.nearest_points(points, 2).T.tolist()

    for v in target:
        assert v in result

    target = np.array([[0.5, 0, 0], [0, 0, 0], [-0.5, 0, 0]]).tolist()
    result = mtr.nearest_points(points, 3).T.tolist()

    for v in target:
        assert v in result

    target = np.array([[0.5, 0, 0], [0, 0, 0], [-0.5, 0, 0], [0, 0, 2]]).tolist()
    result = mtr.nearest_points(points, 4).T.tolist()

    for v in target:
        assert v in result

    target = np.array(
        [[0.5, 0, 0], [0, 0, 0], [-0.5, 0, 0], [0, 0, 2], [1, 0, 2]]
    ).tolist()
    result = mtr.nearest_points(points, 5).T.tolist()

    for v in target:
        assert v in result

    target = points.T.tolist()
    result = mtr.nearest_points(points, 6).T.tolist()

    for v in target:
        assert v in result


def test_normalize():
    a = np.array([1, 0, 0])
    assert np.allclose(mtr.normalize(a), a)

    a = np.array([0, 1, 0])
    assert np.allclose(mtr.normalize(a), a)

    a = np.array([0, 0, 1])
    assert np.allclose(mtr.normalize(a), a)

    a = np.array([1, 1, 1])
    b = a / np.sqrt(3)
    assert np.allclose(mtr.normalize(a), b)

    a = np.array([1, 2, -1])
    b = a / np.sqrt(6)
    assert np.allclose(mtr.normalize(a), b)

    a = np.array([0, 0, 0])
    assert np.allclose(mtr.normalize(a), a)


def test_reflection_matrix():
    a = np.array([1, 0, 0]).reshape((3, 1))
    R = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert np.allclose(mtr.reflection_matrix(a), R)

    a = np.array([0, 1, 0]).reshape((3, 1))
    R = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    assert np.allclose(mtr.reflection_matrix(a), R)

    a = np.array([0, 0, 1]).reshape((3, 1))
    R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    assert np.allclose(mtr.reflection_matrix(a), R)

    a = np.array([1, 1, 1]).reshape((3, 1))
    R = np.array([[1, -2, -2], [-2, 1, -2], [-2, -2, 1]]) / 3
    assert np.allclose(mtr.reflection_matrix(a), R)

    a = np.array([1, 2, -1]).reshape((3, 1))
    R = np.array([[2, -2, 1], [-2, -1, 2], [1, 2, 2]]) / 3
    assert np.allclose(mtr.reflection_matrix(a), R)
