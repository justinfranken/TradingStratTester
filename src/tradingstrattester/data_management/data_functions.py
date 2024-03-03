"""Functions for downloading financial data."""

import warnings
from datetime import date, datetime, timedelta

import yfinance as yf
from tradingstrattester.config import FREQUENCIES


def data_download(symbol, frequency, start_date=None, end_date=None):
    """Download financial data for a given stock symbol within a specified time range
    and frequency.

    Args:
    - symbol (str): The stock symbol for which data is being downloaded.
    - frequency (str, optional): The frequency of the data, e.g. "5m", "60m", "1d".
    - start_date (str, optional): The start date in the format "YYYY-MM-DD". If None, start_date will be set to the maximum possible time difference.
    - end_date (str, optional): The end date in the format "YYYY-MM-DD". If None, end_date will be set to today's date.

    Returns:
    pandas.DataFrame: A DataFrame containing the financial data.

    """
    _handle_errors_data_download(start_date, end_date, frequency)
    dates = _define_dates(frequency=frequency, start_date=start_date, end_date=end_date)

    temp = yf.download(symbol, start=dates[0], end=dates[1], interval=frequency)

    if temp.empty:
        msg = f"Input symbol ('{symbol}') is invalid. Please choose a valid input ticker-symbol from Yahoo Finance."
        raise TypeError(msg)

    else:
        out = temp

    return out


def _define_dates(frequency, start_date=None, end_date=None):
    """Define start and end dates based on the specified frequency.

    Args:
    - frequency (str): The frequency for which dates are being calculated.
    - start_date (str, optional): The start date in the format "YYYY-MM-DD". If None, start_date will be set to None or the maximum possible time difference.
    - end_date (str, optional): The end date in the format "YYYY-MM-DD". If None, end_date will be set to today's date.

    Returns:
    Tuple[Optional[str], str]: A tuple containing the formatted start and end dates in the format "YYYY-MM-DD".

    """
    MAX_DAYS = __get_max_days(FREQUENCIES)
    max_days_for_frequency = dict(zip(FREQUENCIES, MAX_DAYS))

    max_possible_start = date.today() - timedelta(
        days=max_days_for_frequency[frequency],
    )

    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        start_date_result = start_date

        if start_date < max_possible_start:
            start_date_result = max_possible_start
            warnings.warn(
                f"start_date ({start_date}) is larger than allowed. Automatically switching to the max allowed date ({max_days_for_frequency[frequency]}).",
            )

    if start_date is None:
        start_date_result = max_possible_start

    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        end_date = date.today()

    # Ensure the start date is after the end date. For high-frequency data, retrieve the maximum possible data length. For mid to long frequencies, include an extra day for end_date.
    if start_date_result >= end_date:
        if any(frequency == freq for freq in ["60m", "1d", "5d", "1wk", "1mo", "3mo"]):
            end_date = start_date_result + timedelta(days=1)
        if any(frequency == freq for freq in ["1m", "2m", "5m", "15m", "30m"]):
            end_date = date.today()

    return start_date_result.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def __get_max_days(FREQUENCIES):
    """Get the maximum days corresponding to the given frequencies.

    Args:
        FREQUENCIES (list of str): A list of frequency strings for which maximum days are to be retrieved.

    Returns:
        list of int: A list containing the maximum days corresponding to the given frequencies.

    """
    out = []
    frequencies_all = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]
    max_days_all = [
        7,
        59,
        59,
        59,
        59,
        729,
        100000,
        100000,
        100000,
        100000,
        100000,
    ]
    for freq in FREQUENCIES:
        index = frequencies_all.index(freq)
        out.append(max_days_all[index])
    return out


def _handle_errors_data_download(start_date, end_date, frequency):
    """Handle type and value errors for data_download.

    Raises:
    - TypeError: If start_date or end_date is not a string nor a type(None). If frequency is not a string.
    - ValueError: If start_date or end_date have not the correct 'YYYY-MM-DD' format or end_date <= start_date. If selected frequency is not available.

    """
    # Check if frequency has correct type and format
    if not isinstance(frequency, str):
        msg = f"{frequency} is {type(frequency)} but must be a string."
        raise TypeError(
            msg,
        )

    og_frequencies = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]

    if frequency not in og_frequencies:
        msg = f"Invalid frequency: {frequency}. Supported frequencies are {og_frequencies}"
        raise ValueError(
            msg,
        )

    # Check if start_date and end_date are in the correct format
    for input_string in [start_date, end_date]:
        if not isinstance(input_string, type(None) | str):
            msg = f"{input_string} is {type(input_string)} but must be a string or a type(None)."
            raise TypeError(msg)
        elif isinstance(input_string, str):
            try:
                datetime.strptime(input_string, "%Y-%m-%d")
            except ValueError:
                msg = f"Invalid date format: {input_string}. It should be in the format 'YYYY-MM-DD'."
                raise ValueError(msg)

    # Check if end_date is greater than or equal to start_date
    if end_date is not None and start_date is not None and end_date <= start_date:
        msg = f"end_date ({end_date}) must be greater than start_date({start_date})."
        raise ValueError(
            msg,
        )
