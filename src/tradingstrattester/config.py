"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

ASSETS = ["MSFT", "DB", "EURUSD=X", "GC=F", "^TNX"]
FREQUENCIES = ["1m", "5m", "15m", "60m", "90m", "1d"]
MAX_DAYS = [7, 59, 59, 729, 59, 10_000]

__all__ = ["BLD", "SRC", "TEST_DIR", "ASSETS", "FREQUENCIES", "MAX_DAYS"]
