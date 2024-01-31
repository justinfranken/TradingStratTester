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
try out new assets you need to include the trading symbol of that
asset from [Yahoo Finance](https://de.finance.yahoo.com/) in:

```
src / tradingstrattester / config.py
```

Here you can simply change the list object **ASSET**, for example:

```python
ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F", "^TNX"]
```

## Frequency:

The data we downloaded have different observed granularity. In this project we focus on
the following frequencies:

- **High frequency**: 2 minute, 5 minute
- **Reproducible frequency**: 1 day, from "2004-01-01" until "2024-01-01"

> [!NOTE]
> Since [Yahoo Finance](https://de.finance.yahoo.com/) is limmiting the maximal possible history of data to download _(e.g. only 7 days back from today for frequency 1 minute)_ we fix the observed period of daily dates from "2004-01-01" until "2024-01-01" in order to have reproducible analysis results for one frequency. High frequency data is always up-to-date.

But [yfinance](https://github.com/ranaroussi/yfinance) is providing several different possible frequencies:

|   Frequency   | Maximum possible history from today | Variable Name | Include in 'MAX_DAYS' as |
| :---:   | :---: | :---: | :---: |
| 1 Minute | 7 days | "1m" | 7 |
| 2 Minute | 60 days | "2m" | 59 |
| 5 Minute | 60 days | "5m" | 59 |
| 15 Minute | 60 days | "15m" | 59 |
| 30 Minute | 60 days | "30m" | 59 |
| 60 Minute | 730 days | "60m" | 729 |
| 90 Minute | 60 days | "90m" | 59 |
| 1 Day | Infinity | "1d" | 10 ** 1000 |
| 5 Days | Infinity | "5d" | 10 ** 1000 |
| 1 Week | Infinity | "1wk" | 10 ** 1000 |
| 1 Months | Infinity | "1mo" | 10 ** 1000 |
| 3 Months | Infinity | "3mo" | 10 ** 1000 |

You are free to add new of the above frequencies to test the outcome of our trading
strategies. In order to try out new frequencies you need to include the new frequency as you can see in above table in:

```
src / tradingstrattester / config.py
```

Here you can simply change the list object **FREQUENCIES** and **MAX_DAYS**:

```python
FREQUENCIES = ["2m", "60m", "1d"]
MAX_DAYS = [59, 729, 10**1000]
```

> [!CAUTION]
> In order to have a correctly working project you have to add the maximum possible history in the same order in **MAX_DAYS** as you have included frequencies in **FREQUENCIES** and also subtract one day from that history as you can see in the table above.

## Pictures / Analysis results ?!

Maybe some pictures or fancy analysis results later on ...

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate tst
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

We furthmore used the open-source package
[yfinance](https://github.com/ranaroussi/yfinance) to download financial data via
[Yahoo Finance](https://de.finance.yahoo.com/).
