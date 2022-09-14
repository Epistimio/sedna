sedna
=====

|pypi| |py_versions| |codecov| |docs| |tests| |style|

.. |pypi| image:: https://img.shields.io/pypi/v/sedna.svg
    :target: https://pypi.python.org/pypi/sedna
    :alt: Current PyPi Version

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/sedna.svg
    :target: https://pypi.python.org/pypi/sedna
    :alt: Supported Python Versions

.. |codecov| image:: https://codecov.io/gh/Epistimio/sedna/branch/master/graph/badge.svg?token=40Cr8V87HI
   :target: https://codecov.io/gh/Epistimio/sedna

.. |docs| image:: https://readthedocs.org/projects/sedna/badge/?version=latest
   :target:  https://sedna.readthedocs.io/en/latest/?badge=latest

.. |tests| image:: https://github.com/Epistimio/sedna/actions/workflows/test.yml/badge.svg?branch=master
   :target: https://github.com/Epistimio/sedna/actions/workflows/test.yml

.. |style| image:: https://github.com/Epistimio/sedna/actions/workflows/style.yml/badge.svg?branch=master
   :target: https://github.com/Epistimio/sedna/actions/workflows/style.yml



.. code-block:: bash

   pip install sedna


Simple interface to Orion hyperparameter search, no storage, no setup required,
sedna gives you back the full control over the optimization process.


Leverage Orion optimizers
-------------------------

* Random Search
* Grid Search
* Hyperband
* ASHA
* BOHB
* DEHB
* Population Based Training (PBT)
* Population Based Bandits (PB2)
* TPE
* Ax
* Evolution-ES
* MOFA
* Nevergrad
* HEBO


Simplified space definition
---------------------------

As decorated function
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @hyperparameter(a=uniform(0, 1), b=uniform(1, 2))
   def objective(a, b):
       return a + b


As annotated function
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def objective(a: uniform(0, 1), b: uniform(1, 2)) -> float:
       return a + b


As dataclass
^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class MySpace:
       a: uniform(0, 1) = 0
       b: uniform(1, 2) = 1



Gives you back the power over the optimization process
------------------------------------------------------

Setup your own workflow
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sedna.core.space import fidelity, get_space, hyperparameter, uniform
   from sedna.core.hunt import Optimize


   @hyperparameter(epoch=fidelity(2, 10, base=2), a=uniform(0, 1), b=uniform(1, 2))
   def fun(epoch, a, b):
      return (a + b) / epoch


   def main():
      space = get_space(fun)

      opt = Optimize("hyperband", space, max_trials=10)

      while not opt.is_done():
         samples = opt.suggest(2)

         for sample in samples:
            result = fun(**sample.params)

            opt.observe(sample, result)


Integrate it with your current workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sedna.core.space import fidelity, get_space, hyperparameter, uniform
   from sedna.core.hunt import Optimize


   @hyperparameter(epoch=fidelity(2, 10, base=2), a=uniform(0, 1), b=uniform(1, 2))
   def fun(epoch, a, b):
      return (a + b) / epoch


   def main(njob):

      import submitit

      executor = submitit.AutoExecutor(folder="log_test")
      executor.update_parameters(timeout_min=1, slurm_partition="dev")

      opt = Optimize("hyperband", space, max_trials=10)

      while not opt.is_done():
         samples = opt.suggest(njob)
         futures = []

         for sample in samples:
            job = executor.submit(fun, **sample.params)
            futures.append((sample, job)

         for sample, future in futures:
            result = job.result()
            opt.observe(sample, result)
