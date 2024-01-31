"""Functions for downloading financial data."""

from datetime import date, datetime, timedelta

import yfinance as yf
from tradingstrattester.config import FREQUENCIES, MAX_DAYS


def data_download(symbol, frequency="60m", start_date=None, end_date=None):
    """Download financial data for a given stock symbol within a specified time range
    and frequency.

    Args:
    - symbol (str): The stock symbol for which data is being downloaded.
    - frequency (str, optional): The frequency of the data, e.g., "1m", "5m", "15m", "60m", "90m", "1d".
    - start_date (str, optional): The start date in the format "YYYY-MM-DD". If None, start_date will be set to the maximum possible time difference.
    - end_date (str, optional): The end date in the format "YYYY-MM-DD". If None, end_date will be set to today's date.

    Returns:
    pandas.DataFrame: A DataFrame containing the financial data.

    """
    dates = _define_dates(frequency=frequency, start_date=start_date, end_date=end_date)
    return yf.download(symbol, start=dates[0], end=dates[1], interval=frequency)


def _define_dates(frequency, start_date=None, end_date=None):
    """Define start and end dates based on the specified frequency.

    Args:
    - frequency (str): The frequency for which dates are being calculated.
    - start_date (str, optional): The start date in the format "YYYY-MM-DD". If None, start_date will be set to the maximum possible time difference.
    - end_date (str, optional): The end date in the format "YYYY-MM-DD". If None, end_date will be set to today's date.

    Returns:
    Tuple[str, str]: A tuple containing the formatted start and end dates in the format "YYYY-MM-DD".

    """
    _handle_errors_in_define_dates(start_date, end_date, frequency)

    # Define correct start_date and end_date strings
    max_days_for_frequency = dict(zip(FREQUENCIES, MAX_DAYS))

    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start_date = date.today() - timedelta(days=max_days_for_frequency[frequency])

    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        end_date = date.today()

    # Check if the difference between start_date and end_date after creation does not exceed max_days and start_date < end_date
    max_allowed_days = max_days_for_frequency.get(frequency, None)
    if max_allowed_days is not None and (end_date - start_date).days > max_allowed_days:
        msg = f"The difference between end_date and start_date exceeds the maximum allowed days ({max_allowed_days}) for the selected frequency."
        raise ValueError(
            msg,
        )
    if start_date >= end_date:
        msg = f"end_date ({end_date}) must be greater than start_date({start_date})."
        raise ValueError(
            msg,
        )

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def _handle_errors_in_define_dates(start_date, end_date, frequency):
    """Handle type and value errors for _define_dates.

    Raises:
    - TypeError: If start_date or end_date is not a string nor a type(None).
    - ValueError: If start_date or end_date have not the correct 'YYYY-MM-DD' format or end_date <= start_date and if selected frequency is not available.

    """
    if frequency not in FREQUENCIES:
        msg = f"Invalid frequency: {frequency}. Supported frequencies are {FREQUENCIES}"
        raise ValueError(
            msg,
        )

    # Check if start_date and end_date are in the correct format
    for input_string in [start_date, end_date]:
        if isinstance(input_string, str):
            try:
                datetime.strptime(input_string, "%Y-%m-%d")
            except ValueError:
                msg = f"Invalid date format: {input_string}. It should be in the format 'YYYY-MM-DD'."
                raise ValueError(
                    msg,
                )
        elif not isinstance(input_string, type(None) | str):
            msg = f"{input_string} is {type(input_string)} but must be a string or a type(None)."
            raise TypeError(
                msg,
            )

    # Check if end_date is greater than or equal to start_date
    if end_date is not None and start_date is not None and end_date <= start_date:
        msg = f"end_date ({end_date}) must be greater than start_date({start_date})."
        raise ValueError(
            msg,
        )
