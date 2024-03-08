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

    if generator == "_random_gen":
        signal = _random_signal_gen(data)

    if generator == "_crossover_gen":
        signal = _crossover_signal_gen(data)

    if generator == "_RSI_gen":
        signal = _rsi_signal_gen(data)

    if generator == "_BB_gen":
        signal = _bollinger_bands_signal_gen(data)

    if generator == "_MACD_gen":
        signal = _macd_signal_gen(data)

    return signal


# Signal generator functions
def _random_signal_gen(data, prob_zero=0.7, prob_one=0.15, prob_two=0.15):
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

    signal = []

    for _i in range(len(data)):
        rng = np.random.default_rng()
        signal.append(rng.choice([0, 1, 2], p=[prob_zero, prob_one, prob_two]))

    return signal


def _crossover_signal_gen(data):
    """Generates signals based on simple crossover patterns in the provided financial
    data.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().

    Returns:
    - int: An integer representing the signal generated:
           - 1 for a bearish pattern, i.e. sell
           - 2 for a bullish pattern, i.e. buy
           - 0 for no clear pattern, i.e. do nothing

    """
    signals = [0]  # Initialize with no clear pattern for the first data point

    for i in range(1, len(data)):
        current_bar = data.iloc[i]
        previous_bar = data.iloc[i - 1]

        open_price = current_bar["Open"]
        close_price = current_bar["Close"]
        previous_open = previous_bar["Open"]
        previous_close = previous_bar["Close"]

        # Bearish Pattern
        if (
            open_price > close_price
            and previous_open < previous_close
            and close_price < previous_open
            and open_price >= previous_close
        ):
            signals.append(1)  # Sell signal

        # Bullish Pattern
        elif (
            open_price < close_price
            and previous_open > previous_close
            and close_price > previous_open
            and open_price <= previous_close
        ):
            signals.append(2)  # Buy signal

        # No clear pattern
        else:
            signals.append(0)  # No signal

    return signals


def _rsi_signal_gen(data, rsi_threshold_low=30, rsi_threshold_high=70, period=14):
    """Generate RSI (Relative Strength Index) signals based on given thresholds.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().
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


def _bollinger_bands_signal_gen(data, window=20, num_std_dev=1.5):
    """Generate Bollinger Bands signals based on given parameters.

    Parameters:
    - data (pandas.DataFrame): DataFrame containing 'Close' prices.
    - window (int, optional): The window size for computing moving averages and standard deviations. Default is 20.
    - num_std_dev (int, optional): The number of standard deviations to use for the Bollinger Bands. Default is 2.

    Returns:
    - signal (list): A list of signals corresponding to Bollinger Bands conditions.
      - 0: No signal (price between lower and upper bands).
      - 1: Buy signal (price below lower band).
      - 2: Sell signal (price above upper band).

    """
    rolling_mean = data.Close.rolling(window=window).mean()
    upper_band = rolling_mean + (data.Close.rolling(window=window).std() * num_std_dev)
    lower_band = rolling_mean - (data.Close.rolling(window=window).std() * num_std_dev)

    signal = []

    for i in range(len(data)):
        if data.Close.iloc[i] < lower_band[i]:
            signal.append(1)  # Buy signal
        elif data.Close.iloc[i] > upper_band[i]:
            signal.append(2)  # Sell signal
        else:
            signal.append(0)  # No signal

    return signal


def _macd_signal_gen(
    data,
    fast_period=12,
    slow_period=26,
    signal_period=9,
    threshold_multiplier=0.4,
):
    """Calculate MACD (Moving Average Convergence Divergence) signals.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().
    - fast_period (int, optional): The number of periods for the fast EMA (Exponential Moving Average). Default is 12.
    - slow_period (int, optional): The number of periods for the slow EMA. Default is 26.
    - signal_period (int, optional): The number of periods for the signal line. Default is 9.
    - threshold_multiplier (float, optional): A multiplier to adjust the threshold for buy and sell signals.

    Returns:
    - signal (list): A list of signals corresponding to MACD conditions.
      - 0: No signal (MACD between signal line plus/minus threshold).
      - 1: Buy signal (MACD above signal line plus threshold).
      - 2: Sell signal (MACD below signal line minus threshold).

    """
    close_prices = data.Close
    ema_fast = close_prices.ewm(span=fast_period, min_periods=fast_period).mean()
    ema_slow = close_prices.ewm(span=slow_period, min_periods=slow_period).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, min_periods=signal_period).mean()

    macd_signal = []
    macd_std = macd_line.std()

    for macd, signal in zip(macd_line, signal_line):
        # Calculate the threshold based on the standard deviation of the MACD line
        threshold = threshold_multiplier * macd_std

        if macd > signal + threshold:
            macd_signal.append(1)  # Buy signal
        elif macd < signal - threshold:
            macd_signal.append(2)  # Sell signal
        else:
            macd_signal.append(0)  # No signal

    return macd_signal


def _handle_errors_signal_list(data, generator):
    """Handle type and value errors for signal_list.

    Raises:
    - ValueError: If data has wrong columns or is empty. If generator is not defined.
    - TypeError: If generator is not a string.

    """
    if not isinstance(data, pd.core.frame.DataFrame):
        msg = f"Wrong input type for 'data' ({type(data)}). Data has to be of type 'pd.DataFrame'."
        raise TypeError(msg)

    if data.empty is True:
        msg = f"Input data ({data}) is empty. Please use data_download() with valid inputs as input data."
        raise ValueError(msg)

    columns = ["Open", "High", "Low", "Close"]
    for cols in columns:
        if not any(data.columns == cols):
            msg = f"Input data has columns {data.columns}. It is missing column {cols}. Please use data_download() with valid inputs as input data."
            raise ValueError(msg)

    if not isinstance(generator, str):
        msg = f"Wrong input generator ({type(generator)}). 'generator' has to be type string."
        raise TypeError(msg)

    og_strategies = [
        "_random_gen",
        "_crossover_gen",
        "_RSI_gen",
        "_BB_gen",
        "_MACD_gen",
    ]
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
