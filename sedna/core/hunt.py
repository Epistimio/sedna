from dataclasses import dataclass, field
from typing import List

from orion.algo.base import algo_factory
from orion.core.worker.trial import Trial


@dataclass
class Sample:
    id: str
    hash: str
    params: dict
    result: List[float] = field(default_factory=list)


class _FakeTrial:
    def __init__(self, sample) -> None:
        self.sample = sample

    @staticmethod
    def compute_trial_hash(
        obj,
        ignore_fidelity=False,
        ignore_experiment=False,
        ignore_lie=False,
        ignore_parent=False,
    ):
        if ignore_fidelity == 0:
            return obj.sample.id

        return obj.sample.hash

    @property
    def objective(self):
        return Trial.Result(
            name="objective", type="objective", value=self.sample.result[-1]
        )

    @property
    def lie(self):
        return False

    @property
    def results(self):
        return []

    @results.setter
    def results(self, value):
        pass

    @property
    def gradient(self):
        return None


class Optimize:
    """Simplified orion interface without storage

    Parameters
    ----------

    name: str
        Name of the hyperparameter search algorithm to use

    space: Space
        Search space to use

    config: Dict
        Configuration for the hyperparameter search algorithm

    """

    def __init__(self, name, space, max_trials, **config) -> None:
        self.space = space
        self.max_trials = max_trials
        self.algo = algo_factory.create(name, self.space, **config)
        self.trials = dict()

    def suggest(self, count) -> List[Sample]:
        """Suggest samples to execute"""
        trials = []

        trials.extend(self.algo.suggest(count))

        return [self._no_trial(t) for t in trials]

    def observe(self, sample: Sample, result: float) -> None:
        """Observe the obhective for a given sample"""
        n = self.algo.n_observed

        sample.result.append(result)

        use_fake_trial = False

        if use_fake_trial:
            self.algo.observe([_FakeTrial(sample)])

        else:
            trial = self.trials[sample.id]
            results = trial.results
            results += [_FakeTrial(sample).objective]
            trial.results = results

            self.algo.observe([trial])

        assert self.algo.n_observed > n

    def is_done(self):
        """Return true if the algo finished optimizing"""
        if self.max_trials <= 0:
            return self.algo.is_done

        return self.algo.is_done or self.algo.n_observed >= self.max_trials

    def _no_trial(self, trial):
        unique_id = trial.compute_trial_hash(
            trial,
            ignore_fidelity=False,
            ignore_experiment=False,
            ignore_lie=False,
            ignore_parent=False,
        )
        param_hash = trial.compute_trial_hash(
            trial,
            ignore_fidelity=True,
            ignore_experiment=True,
            ignore_lie=True,
            ignore_parent=True,
        )
        simple = Sample(unique_id, param_hash, trial.params)
        self.trials[simple.id] = trial
        return simple

    def state_dict(self):
        return {
            "algo": self.algo.state_dict(),
        }

    def set_state(self, state):
        self.aglo.set_state(state["algo"])
