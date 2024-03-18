"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()

## Downloading financial data configurations
# possible frequencies: 1m, 2m, 5m, 15m, 30m, 60m, 1d, 5d, 1wk, 1mo, 3mo
FREQUENCIES = ["60m", "1d", "1wk"]
# date format is YYYY-MM-DD
START_DATE = "2018-01-01"
END_DATE = "2024-03-01"
# Symbols that include '.' or '_' are not suitable!
ASSETS = ["DB", "KO", "^GSPC", "EURUSD=X", "CL=F"]

## Simulating depot configurations
# possible signaling strategies: "_random_gen", "_crossover_gen", "_RSI_gen", "_BB_gen", "_MACD_gen"
STRATEGIES = ["_random_gen", "_crossover_gen", "_RSI_gen", "_BB_gen", "_MACD_gen"]
# possible unit trading strategies: "fixed_trade_units", "percentage_to_value_trades", "volatility_unit_trades"
UNIT_STRAT = "percentage_to_value_trades"
UNIT_VAR = 0.05  # variable used in unit trade strategies (positive int / float)
INITIAL_DEPOT_CASH = (
    10_000  # determines initial total depot value (positive int / float)
)
START_STOCK_PRCT = 0.25  # determines how much of the initial cash will be invested in assets (positive int / float)
TAC = 0.0005  # transactionscosts per transaction (= trade_units * tac) (positive int / float)


_ID = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]


__all__ = [
    "BLD",
    "SRC",
    "TEST_DIR",
    "ASSETS",
    "START_DATE",
    "END_DATE",
    "FREQUENCIES",
    "_ID",
    "STRATEGIES",
    "INITIAL_DEPOT_CASH",
    "START_STOCK_PRCT",
    "UNIT_STRAT",
    "UNIT_VAR",
    "TAC",
]
