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
start_date = "2014-01-01"
end_date = "2024-01-01"

## Simulating depot configurations
# possible signaling strategies: "_simple_signal_gen", "_random_signal_gen"
STRATEGIES = ["_simple_signal_gen", "_random_signal_gen"]
initial_depot_cash = 10000
start_stock_prct = 0.25
unit_var = 0.075
tac = 0.005
# possible unit trading strategies: "fixed_trade_units", "percentage_to_value_trades", "volatility_unit_trades"
unit_strat = "percentage_to_value_trades"


_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]


__all__ = [
    "BLD",
    "SRC",
    "TEST_DIR",
    "ASSETS",
    "FREQUENCIES",
    "_id",
    "STRATEGIES",
    "initial_depot_cash",
    "start_stock_prct",
    "unit_strat",
    "unit_var",
]
