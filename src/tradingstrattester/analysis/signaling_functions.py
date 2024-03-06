"""Functions for indicating when to buy, sell or do nothing."""
import numpy as np
import pandas as pd


def signal_list(data, generator):
    """Generates a signal list based on the asset data from data_download() using a
    specified signal generator.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().
    - generator (str): The name of the signal generator function to use.

    Returns:
    - list: A list of signals generated (either 0,1, or 2) based on the specified signal generator.

    """
    _handle_errors_signal_list(data, generator)
    signal = []
    signal.append(0)

    if generator == "_random_signal_gen":
        for i in range(1, len(data)):
            signal.append(_random_signal_gen())

    if generator == "_simple_signal_gen":
        for i in range(1, len(data)):
            df = data[i - 1 : i + 1]
            signal.append(_simple_signal_generator(df))

    if generator == "_rsi_signal_gen":
        signal = _rsi_signal_gen(data)

    return signal


# Signal generator functions
def _random_signal_gen(prob_zero=0.7, prob_one=0.15, prob_two=0.15):
    """Generates a random signal with specified probabilities using a random number
    generator.

    Parameters:
    - prob_zero (float): Probability of generating 0.
    - prob_one (float): Probability of generating 1.
    - prob_two (float): Probability of generating 2.

    Returns:
    - int: An integer representing the randomly generated signal:
           - 1 for a bearish pattern, i.e. sell
           - 2 for a bullish pattern, i.e. buy
           - 0 for no clear pattern, i.e. do nothing

    """
    _handle_errors_random_signal_gen(prob_zero, prob_one, prob_two)
    rng = np.random.default_rng()
    return rng.choice([0, 1, 2], p=[prob_zero, prob_one, prob_two])


def _simple_signal_generator(data):
    """Generates a signal based on the provided data using a simple signal generation
    algorithm.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().

    Returns:
    - int: An integer representing the signal generated:
           - 1 for a bearish pattern, i.e. sell
           - 2 for a bullish pattern, i.e. buy
           - 0 for no clear pattern, i.e. do nothing

    """
    open = data.Open.iloc[-1]
    close = data.Close.iloc[-1]
    previous_open = data.Open.iloc[-2]
    previous_close = data.Close.iloc[-2]

    # Bearish Pattern
    if (
        open > close
        and previous_open < previous_close
        and close < previous_open
        and open >= previous_close
    ):
        return 1

    # Bullish Pattern
    elif (
        open < close
        and previous_open > previous_close
        and close > previous_open
        and open <= previous_close
    ):
        return 2

    # No clear pattern
    else:
        return 0


def _rsi_signal_gen(data, rsi_threshold_low=30, rsi_threshold_high=70, period=14):
    """Generate RSI (Relative Strength Index) signals based on given thresholds.

    Parameters:
    - data (pandas.DataFrame): DataFrame containing 'Close' prices.
    - rsi_threshold_low (int, optional): The lower threshold for RSI indicating a buy signal. Default is 30.
    - rsi_threshold_high (int, optional): The higher threshold for RSI indicating a sell signal. Default is 70.
    - period (int, optional): The period used for calculating RSI. Default is 14.

    Returns:
    - signal (list): A list of signals corresponding to RSI conditions.
      - 0: No signal (RSI between rsi_threshold_low and rsi_threshold_high).
      - 1: Sell signal (RSI above rsi_threshold_high).
      - 2: Buy signal (RSI below rsi_threshold_low).

    """
    close_prices = data.Close
    deltas = close_prices.diff()

    gain = deltas.where(deltas > 0, 0)
    loss = -deltas.where(deltas < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    signal = []

    for val in rsi:
        if val < rsi_threshold_low:
            signal.append(2)  # Buy signal
        elif val > rsi_threshold_high:
            signal.append(1)  # Sell signal
        else:
            signal.append(0)  # No signal

    return signal


def _handle_errors_signal_list(data, generator):
    """Handle type and value errors for signal_list.

    Raises:
    - ValueError: If data has wrong columns or is empty. If generator is not defined.
    - TypeError: If generator is not a string.

    """
    if data.empty is True:
        msg = f"Input data ({data}) is empty. Please use data_download() with valid inputs as input data."
        raise ValueError(msg)

    if not isinstance(data, pd.core.frame.DataFrame):
        msg = f"Wrong input type for 'data' ({type(data)}). Data has to be of type 'pd.DataFrame'."
        raise TypeError(msg)

    columns = ["Open", "High", "Low", "Close"]
    for cols in columns:
        if not any(data.columns == cols):
            msg = f"Input data has columns {data.columns}. It is missing column {cols}. Please use data_download() with valid inputs as input data."
            raise ValueError(msg)

    if not isinstance(generator, str):
        msg = f"Wrong input generator ({type(generator)}). 'generator' has to be type string."
        raise TypeError(msg)

    og_strategies = ["_random_signal_gen", "_simple_signal_gen", "_rsi_signal_gen"]
    if generator not in og_strategies:
        msg = f"Selected trading strategy ({generator}) is not available. Please choose at least one from ({og_strategies})."
        raise ValueError(msg)


def _handle_errors_random_signal_gen(prob_zero, prob_one, prob_two):
    """Handle type and value errors for _random_signal_gen.

    Raises:
    - ValueError: If input probabilities are each not between 0 and 1 or together are greater than 1.

    """
    probabilities = [prob_zero, prob_one, prob_two]
    for probs in probabilities:
        if probs > 1 or probs < 0:
            msg = f"Input probability ({probs}) is not between 0 and 1. Please choose a probability which is between 0 and 1."
            raise ValueError(msg)

    total_prob = sum(probabilities)
    if total_prob != 1:
        msg = f"Sum of all given probabilities is not equal to 1 ({probabilities}). Sum has to be equal to 1."
        raise ValueError(msg)
