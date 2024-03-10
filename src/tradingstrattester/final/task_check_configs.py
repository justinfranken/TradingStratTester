""""Task to check if config.py lists."""

import pytask
from tradingstrattester.config import ASSETS, FREQUENCIES, STRATEGIES


@pytask.mark.try_first
def task_check_config_lists():
    """Task function to check lists of config.py."""
    config_list_vars = [FREQUENCIES, ASSETS, STRATEGIES]
    config_list_names = ["FREQUENCIES", "ASSETS", "STRATEGIES"]
    for i in [0, 1, 2]:
        if not config_list_vars[i]:
            msg = f"{config_list_names[i]} is empty. Please specify at least one entry in {config_list_names[i]} in the config.py file."
            raise ValueError(msg)

    for syb in ASSETS:
        if "." in syb or "_" in syb:
            msg = f"Symbols cannot include '.' or '_' in their names. Please enter a different symbol instead of {syb}."
            raise ValueError(msg)
