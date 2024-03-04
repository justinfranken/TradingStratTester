""""Test for the plotting functions."""
import pandas as pd
import pytest
from tradingstrattester.analysis.plotting_functions import (
    _handle_errors_in_plot_functions,
)
from tradingstrattester.config import BLD, STRATEGIES

_dependencies = []
for strategy in STRATEGIES:
    _dependencies.append(BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl")

## Testing error_handling

# for data
value_error_data = [
    pd.DataFrame(),
    pd.DataFrame(1, index=range(10), columns=["Open", "High", "Missing_low", "Close"]),
    pd.DataFrame(1, index=range(10), columns=["High", "Low", "Close"]),
]


@pytest.mark.parametrize("inputs", value_error_data)
def test_value_error_data_error_handling(inputs):
    with pytest.raises(ValueError):
        _handle_errors_in_plot_functions(data=inputs)
