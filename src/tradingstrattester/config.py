"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

FREQUENCIES = ["2m", "60m", "1d"]
ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F", "^TNX"]
_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]

# Simulating depot configurations
STRATEGIES = ["_simple_signal_gen", "_random_signal_gen"]
initial_depot_cash = 10000
start_stock_prct = 0.25


__all__ = [
    "BLD",
    "SRC",
    "TEST_DIR",
    "ASSETS",
    "FREQUENCIES",
    "initial_depot_cash",
    "_id",
    "start_stock_prct",
]
