"""Functions for indicating when to buy or sell."""


def signal_list(data, generator):
    """Generates a signal list based on the input data using a specified signal
    generator.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().
    - generator (str): The name of the signal generator function to use.

    Returns:
    - list: A list of signals generated based on the specified signal generator.

    """
    signal = []
    signal.append(0)

    if generator == "_simple_signal_generator":
        for i in range(1, len(data)):
            df = data[i - 1 : i + 1]
            signal.append(_simple_signal_generator(df))

    return signal


# Signal generator functions
def _simple_signal_generator(data):
    """Generates a signal based on the provided data using a simple signal generation
    algorithm.

    Parameters:
    - data (pandas.DataFrame): A DataFrame containing the financial data from data_download().

    Returns:
    - int: An integer representing the signal generated:
           - 1 for a bearish pattern
           - 2 for a bullish pattern
           - 0 for no clear pattern

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
