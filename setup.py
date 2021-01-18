#!/usr/bin/env python

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "terra_sdk", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = list()
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author=about["__author__"],
    author_email=about["__author_email__"],
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=about["__description__"],
    install_requires=requirements,
    license=about["__license__"],
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="jigu terra terra_sdk sdk blockchain defi finance",
    name=about["__title__"],
    packages=find_packages(include=["terra_sdk", "terra_sdk.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url=about["__url__"],
    version=about["__version__"],
    zip_safe=False,
)
