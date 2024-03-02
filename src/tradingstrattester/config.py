"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

FREQUENCIES = ["5m", "60m", "1d"]
ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F"]
_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]

## Simulating depot configurations
STRATEGIES = ["_simple_signal_gen", "_random_signal_gen"]
initial_depot_cash = 10000
start_stock_prct = 0.25
unit_strat = "percentage_to_value_trades"
unit_var = 0.075


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
