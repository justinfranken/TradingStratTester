"""Functions for indicating when to buy, sell or do nothing."""
import numpy as np


def signal_list(data, generator):
    """Generates a signal list based on the asset data from data_download() using a
    specified signal generator.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().
    - generator (str): The name of the signal generator function to use.

    Returns:
    - list: A list of signals generated (either 0,1, or 2) based on the specified signal generator.

    """
    signal = []
    signal.append(0)

    if generator == "_random_signal_gen":
        for i in range(1, len(data)):
            signal.append(_random_signal_gen())

    if generator == "_simple_signal_gen":
        for i in range(1, len(data)):
            df = data[i - 1 : i + 1]
            signal.append(_simple_signal_generator(df))

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
