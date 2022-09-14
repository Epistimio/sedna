from dataclasses import dataclass

from sedna.core.space import get_space_configuration, hyperparameter, uniform


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
    b: uniform(1, 2) = 1


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
    assert get_space_configuration(obj) == {"a": "uniform(0, 1)", "b": "uniform(1, 2)"}
