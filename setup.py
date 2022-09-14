#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import setup

with open("sedna/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

assert (
    os.path.exists(os.path.join("sedna", "__init__.py")) is False
), "sedna is a namespace not a module"

extra_requires = {"plugins": ["importlib_resources"]}
extra_requires["all"] = sorted(set(sum(extra_requires.values(), [])))

if __name__ == "__main__":
    setup(
        name="sedna",
        version=version,
        extras_require=extra_requires,
        description="Simple interface to Orion algorithm",
        long_description=(Path(__file__).parent / "README.rst").read_text(),
        author="Pierre Delaunay",
        author_email="pierre.delaunay@mila.quebec",
        license="BSD 3-Clause License",
        url="https://sedna.readthedocs.io",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
        ],
        packages=[
            "sedna.core",
            "sedna.plugins.example",
        ],
        setup_requires=["setuptools"],
        install_requires=["importlib_resources", "orion", "typing_extensions"],
        namespace_packages=[
            "sedna",
            "sedna.plugins",
        ],
        package_data={
            "sedna.data": [
                "sedna/data",
            ],
        },
    )
