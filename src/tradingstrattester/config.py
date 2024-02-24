"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

FREQUENCIES = ["2m", "60m", "1d"]
MAX_DAYS = [59, 729, 10**1000]
ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F", "^TNX"]
STRATEGIES = ["_simple_signal_gen"]

__all__ = ["BLD", "SRC", "TEST_DIR", "ASSETS", "FREQUENCIES", "MAX_DAYS"]
