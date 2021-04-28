![logo](./docs/img/logo.png)

You can find the documentation [here](https://terra-project.github.io/terra-sdk-python/).

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [For Maintainers](#for-maintainers)
  - [Testing](#testing)
  - [Code Quality](#code-quality)
  - [Releasing a new version](#releasing-a-new-version)
- [License](#license)

## Installation

Terra SDK requires **Python v3.7+**.

```sh
$ pip install -U terra-sdk
```

## For Maintainers

**NOTE:** This section is for developers and maintainers of the Terra SDK for Python.

Terra SDK uses [Poetry](https://python-poetry.org/) to manage dependencies. To get set up with all the

```sh
$ pip install poetry
$ poetry install
```

### Testing

Terra SDK provides tests for data classes and functions. To run them:

```
$ make test
```

### Code Quality

Terra SDK uses Black, isort, and mypy for checking code quality and maintaining style:

```
$ make qa && make format
```

### Releasing a new version

**NOTE**: This section only concerns approved publishers on PyPI. An automated release
process will be run upon merging into the `master` branch.

To publish a new version on PyPI, bump the version on `pyproject.toml` and run:

```
$ make release
```

## License

Terra SDK is licensed under the MIT License. More details are available [here](./LICENSE).
