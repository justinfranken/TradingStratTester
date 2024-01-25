# TradingStratTester

[![image](https://img.shields.io/github/actions/workflow/status/justinfranken/tradingstrattester/main.yml?branch=main)](https://github.com/justinfranken/tradingstrattester/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/justinfranken/tradingstrattester/branch/main/graph/badge.svg)](https://codecov.io/gh/justinfranken/tradingstrattester)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/justinfranken/tradingstrattester/main.svg)](https://results.pre-commit.ci/latest/github/justinfranken/tradingstrattester/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

In this project we are trying out several different trading strategies on a simulated
depot using different asset classes. The general goal is then to see, which strategy
works best on which asset class. We will also use a random strategie on all asset
classes to see if our results differ a lot from randomness.

## Trading strategies:

Our trading strategies are the following:

1. ...
1. ...
1. ...
1. ...
1. Random: In this strategy we will generate random buy or sell decisions.

## Asset classes:

In this project we have the following asset data prepared:

1. Foreign exchange courses (EUR/USD) from ... to ...
1. Stock data (Microsoft (MSFT), Tesla (TSLA), ...) from ... to ...
1. Bond data from ... to ...

You are free to add new data to test the outcome of our trading strategies. In order to
try out new data you need to:

```python
def somefunction(test):
    var = something
    return var
```

## Pictures ?!

Maybe some pictures later on ...

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate ass5
```

In order to create the full reproducible project type the following into your console,
while being in the project directory:

```console
$ pytask
```

## Project template

The project which will then be generated is structured as follows:

- **bld**: The build directory contains our analysis results. Including our plots and
  tables.
- **paper**: The paper directory contains our TEX-files which generate the PDF results.
- **src**: The source directory contains all of our python files for our analysis.
- **test**: The test directory contains all of our python files to test the functions
  used for our analysis.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
