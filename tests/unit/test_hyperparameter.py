from dataclasses import dataclass

import pytest

from sedna.core.space import (
    choices,
    get_space_configuration,
    hyperparameter,
    loguniform,
    normal,
    uniform,
)


@hyperparameter(a=uniform(0, 1), b=uniform(1, 2))
def my_decorated_function(a, b):
    return a + b


def my_annotated_function(a: uniform(0, 1), b: uniform(1, 2)):
    return a + b


class ObjectWithSpaceMethod:
    def get_space(self):
        return dict(
            a=uniform(0, 1),
            b=uniform(1, 2),
        )


@dataclass
class DataClassWithSpace:
    a: uniform(0, 1) = 0
    b: loguniform(1, 2) = 1
    c: normal(1, 2) = 1
    d: choices([1, 2, 3]) = 1


def test_decorated_function():
    assert get_space_configuration(my_decorated_function) == {
        "a": "uniform(0, 1)",
        "b": "uniform(1, 2)",
    }


def test_annotated_function():
    assert get_space_configuration(my_annotated_function) == {
        "a": "uniform(0, 1)",
        "b": "uniform(1, 2)",
    }


def test_object_with_space_method():
    obj = ObjectWithSpaceMethod()
    assert get_space_configuration(obj) == {"a": "uniform(0, 1)", "b": "uniform(1, 2)"}


def test_dataclass_types():
    obj = DataClassWithSpace()
    assert get_space_configuration(obj) == {
        "a": "uniform(0, 1)",
        "b": "loguniform(1, 2)",
        "c": "normal(1, 2)",
        "d": "choices([1, 2, 3])",
    }


def test_wrong_obj():
    obj = True

    with pytest.raises(TypeError):
        get_space_configuration(obj)
