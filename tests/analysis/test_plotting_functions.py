""""Test for the plotting functions."""
import pandas as pd
import pytest
from tradingstrattester.analysis.plotting_functions import (
    _generate_intervals,
    _handle_errors_in_plot_functions,
    plot_asset_strategy,
    plot_indicators,
    plot_units_and_cash,
)
from tradingstrattester.config import _ID, BLD, STRATEGIES
from tradingstrattester.data_management.data_functions import data_download

# Correct input variables
data = data_download("DB", "60m")
id = "60m_DB.pkl"
initial_depot_cash = 100
_dependencies = []
for strategy in STRATEGIES:
    _dependencies.append(BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl")


## Testing error_handling
# error lists
value_error_data = [
    pd.DataFrame(),
    pd.DataFrame(1, index=range(10), columns=["Open", "High", "Missing_low", "Close"]),
    pd.DataFrame(1, index=range(10), columns=["High", "Low", "Close"]),
]
type_error_data = [range(10), "string", ["list", "of", "strings"]]
value_error_id = ["3m_DB.pkl", "1d_DB", "DB_1d.pkl"]
type_error_id = [100, ["60m_DB.pkl"], {"60m_DB.pkl"}]
value_error_idc = ["3m_DB.pkl", "1d_DB", "DB_1d.pkl"]
type_error_idc = [100, ["60m_DB.pkl"], {"60m_DB.pkl"}]
type_error_depends_on = [
    range(10),
    [range(10)],
    ["string1", "string2", "string3"],
]


@pytest.mark.parametrize(
    (
        "value_inputs_data",
        "type_inputs_data",
        "value_inputs_id",
        "type_inputs_id",
        "value_inputs_idc",
        "type_inputs_idc",
        "type_inputs_depends_on",
    ),
    zip(
        value_error_data,
        type_error_data,
        value_error_id,
        type_error_id,
        value_error_idc,
        type_error_idc,
        type_error_depends_on,
    ),
)
def test_value_error_data_error_handling(
    value_inputs_data,
    type_inputs_data,
    value_inputs_id,
    type_inputs_id,
    value_inputs_idc,
    type_inputs_idc,
    type_inputs_depends_on,
):
    """Tests for error_handling for the plotting helper function."""
    with pytest.raises(ValueError):
        _handle_errors_in_plot_functions(data=value_inputs_data)
        _handle_errors_in_plot_functions(data=data, id=value_inputs_id)
        _handle_errors_in_plot_functions(
            data=data,
            id=id,
            initial_depot_cash=value_inputs_idc,
        )
    with pytest.raises(TypeError):
        _handle_errors_in_plot_functions(data=type_inputs_data)
        _handle_errors_in_plot_functions(data=data, id=type_inputs_id)
        _handle_errors_in_plot_functions(
            data=data,
            id=id,
            initial_depot_cash=type_inputs_idc,
        )
        _handle_errors_in_plot_functions(
            data=data,
            id=id,
            initial_depot_cash=initial_depot_cash,
            depends_on=type_inputs_depends_on,
        )


## Testing expected outcomes
# plotting functions
@pytest.mark.parametrize("id_str", _ID)
def test_outcome_of_plot_functions(id_str):
    fig_asset_strat = plot_asset_strategy(
        data,
        id_str,
        initial_depot_cash,
        _dependencies,
    )
    """Test expected plot function outcomes."""
    fig_indicators = plot_indicators(data, id_str, initial_depot_cash, _dependencies)
    fig_units_cash = plot_units_and_cash(data, id_str, _dependencies)
    id_str = id_str.split(".")[0]
    for i in [fig_asset_strat, fig_indicators, fig_units_cash]:
        assert (
            i.layout["title"]["text"][
                i.layout["title"]["text"]
                .find(id_str) : i.layout["title"]["text"]
                .find(id_str)
                + len(id_str)
            ]
        ) == id_str


# generate_intervals
input_nums = [
    1,
    2,
]
expected_output_intervals = [
    [[0, 1]],
    [[0, 0.455], [0.545, 1.0]],
]


@pytest.mark.parametrize(
    ("input", "output"),
    zip(input_nums, expected_output_intervals),
)
def test_generate_intervals(input, output):
    """Test expected _generate_intervals outcomes."""
    assert _generate_intervals(input) == output
