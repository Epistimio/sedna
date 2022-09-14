from typing import Any, List, Optional, Union

from orion.core.io.space_builder import DimensionBuilder, SpaceBuilder
from orion.algo.space import Space, Dimension


# pylint: disable=too-few-public-methods
class SpaceDimFunction:
    """Type to recognize orion functions parsed by the override parser"""

    def __init__(self, fun) -> None:
        self.fun = fun

    def __call__(self, name: str) -> Any:
        return self.fun(name)


def uniform(
    low: Union[int, float],
    high: Union[int, float],
    discrete: bool = False,
    precision: int = 4,
    shape: Optional[List] = None,
) -> SpaceDimFunction:
    """Builds a uniform dimension"""

    def dim(name):
        builder = DimensionBuilder()
        builder.name = name
        return builder.uniform(
            low, high, discrete=discrete, precision=precision, shape=shape
        )

    return SpaceDimFunction(dim)


def loguniform(
    low: Union[int, float],
    high: Union[int, float],
    discrete: bool = False,
    precision: int = 4,
    shape: Optional[List] = None,
) -> SpaceDimFunction:
    """Builds a uniform dimension"""

    def dim(name):
        builder = DimensionBuilder()
        builder.name = name
        return builder.loguniform(
            low, high, discrete=discrete, precision=precision, shape=shape
        )

    return SpaceDimFunction(dim)


def normal(
    loc: Union[int, float],
    scale: Union[int, float],
    discrete: bool = False,
    precision: int = 4,
    shape: Optional[List] = None,
) -> SpaceDimFunction:
    """Builds a normal dimension"""

    def dim(name):
        builder = DimensionBuilder()
        builder.name = name
        return builder.normal(
            loc, scale, discrete=discrete, precision=precision, shape=shape
        )

    return SpaceDimFunction(dim)


def fidelity(
    low: Union[int, float], high: Union[int, float], base: Union[int, float] = 2
) -> SpaceDimFunction:
    """Builds a fidelity dimension"""

    def dim(name):
        builder = DimensionBuilder()
        builder.name = name
        return builder.fidelity(low, high, base=base)

    return SpaceDimFunction(dim)


def choices(options) -> SpaceDimFunction:
    """Builds a choices dimension"""

    def tovalue(v):
        return v

    if isinstance(options, list):
        options = [tovalue(option) for option in options]

    def dim(name):
        builder = DimensionBuilder()
        builder.name = name
        return builder.choices(options)

    return SpaceDimFunction(dim)


def hyperparameter(**dims):
    """Hyper-parameter decorator
    Example
    -------
    >>> @hyperparameter(a=uniform(0, 1), b=normal(0, 1))
    ... def fun(a, b):
    ...    return a + b
    >>> get_space(fun).configuration
    {'a': 'uniform(0, 1)', 'b': 'normal(0, 1)'}
    """

    def call(fun):
        space = dict()

        for k, v in dims.items():
            if isinstance(v, SpaceDimFunction):
                space[k] = v(k)
            else:
                raise TypeError(f"{type(v)} is not a supported dimension type")

        setattr(fun, "__space__", space)
        return fun

    return call


def get_space_dimensions(obj):
    """Retrieve hyper-parameter space for a given function or object"""
    space = None

    # Extract space dimensions from object

    # Decorated function
    if hasattr(obj, "__space__"):
        space = obj.__space__

    # get space override
    elif hasattr(obj, "get_space"):
        space = obj.get_space()

    # Read the space from the annotations
    elif hasattr(obj, "__annotations__"):
        dims = obj.__annotations__

        if dims:
            space = dict()

            for k, v in dims.items():
                space[k] = v

    if space is None:
        raise TypeError(f"No space information held inside {type(obj)}, {obj}")

    # --------------------
    # Build the dimensions
    dims = dict()
    for k, v in space.items():
        if isinstance(v, SpaceDimFunction):
            dims[k] = v(k)

        if isinstance(v, Dimension):
            dims[k] = v

    return dims


def get_space_configuration(obj) -> Space:
    """Build orion space configuration fron an object"""
    dimensions = get_space_dimensions(obj)

    config = dict()
    for k, dim in dimensions.items():
        config[k] = dim.get_prior_string()

    return config


def get_space(obj) -> Space:
    """Build orion space from an object"""
    config = get_space_configuration(obj)

    return SpaceBuilder().build(config)
