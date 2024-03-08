"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

## Downloading financial data configurations
FREQUENCIES = ["5m", "60m", "1d"]
ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F"]
# date format is YYYY-MM-DD
START_DATE = "2014-01-01"
END_DATE = "2024-03-01"

## Simulating depot configurations
# possible signaling strategies: "_random_gen", "_crossover_gen", "_RSI_gen", "_BB_gen", "_MACD_gen"
STRATEGIES = ["_random_gen", "_crossover_gen", "_RSI_gen", "_BB_gen", "_MACD_gen"]
INITIAL_DEPOT_CASH = 10000  # determines initial total depot value
START_STOCK_PRCT = (
    0.25  # determines how much of the initial cash will be invested in assets
)
UNIT_VAR = 0.05  # variable used in unit trade strategies
TAC = 0.001  # transactionscosts per transaction (= trade_units * tac)
# possible unit trading strategies: "fixed_trade_units", "percentage_to_value_trades", "volatility_unit_trades"
UNIT_STRAT = "percentage_to_value_trades"


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
