from sedna.core.space import fidelity, get_space, hyperparameter, uniform
from sedna.core.hunt import Optimize


@hyperparameter(a=uniform(0, 1), b=uniform(1, 2))
def fun(a, b):
    return a + b


def test_random_hunt():

    space = get_space(fun)

    hunter = Optimize("random", space, max_trials=10)

    while not hunter.is_done():
        samples = hunter.suggest(2)

        for sample in samples:
            result = fun(**sample.params)

            hunter.observe(sample, result)


@hyperparameter(epoch=fidelity(2, 10, base=2), a=uniform(0, 1), b=uniform(1, 2))
def fun(epoch, a, b):
    return (a + b) / epoch


def test_hyperband_hunt():

    space = get_space(fun)

    hunter = Optimize("hyperband", space, max_trials=10)

    while not hunter.is_done():
        samples = hunter.suggest(2)

        for sample in samples:
            result = fun(**sample.params)

            hunter.observe(sample, result)
