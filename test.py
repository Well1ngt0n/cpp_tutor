import pytest
from yandex_testing_lesson import Rectangle


def test_empty():
    with pytest.raises(TypeError):
        Rectangle()


def test_empty_2():
    with pytest.raises(TypeError):
        Rectangle(1)


def test_incorrect_type_1():
    with pytest.raises(TypeError):
        Rectangle(None, 100)


def test_incorrect_type_1_2():
    with pytest.raises(TypeError):
        Rectangle([1], 100)


def test_incorrect_type_1_3():
    with pytest.raises(TypeError):
        Rectangle({1}, 100)


def test_incorrect_type_2():
    with pytest.raises(TypeError):
        Rectangle(100, None)


def test_incorrect_type_2_2():
    with pytest.raises(TypeError):
        Rectangle(100, [1])


def test_incorrect_type_2_3():
    with pytest.raises(TypeError):
        Rectangle(1, {1})


def test_incorrect_num_1():
    with pytest.raises(ValueError):
        Rectangle(100, -100)


def test_incorrect_num_2():
    with pytest.raises(ValueError):
        Rectangle(-100, 100)


def test_area():
    assert Rectangle(20, 3).get_area() == 60


def test_perimeter():
    assert Rectangle(7, 4).get_perimeter() == 22
