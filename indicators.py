# indicators.py
import pandas_ta as ta

def calculate_ema(df, length):
    """
    Calculate Exponential Moving Average (EMA) for the given DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    length (int): The period length for the EMA.

    Returns:
    pandas.Series: The calculated EMA.
    """
    return ta.ema(df['Close'], length=length)


def calculate_rsi(df, length):
    """
    Calculate Relative Strength Index (RSI) for the given DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    length (int): The period length for the RSI.

    Returns:
    pandas.Series: The calculated RSI.
    """
    return ta.rsi(df['Close'], length=length)



def calculate_supertrend(df, period, multiplier):
    """
    Calculate Supertrend for the given DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    period (int): The lookback period for the Supertrend.
    multiplier (float): The multiplier for the ATR in the Supertrend calculation.

    Returns:
    pandas.DataFrame: The DataFrame with Supertrend columns.
    """
    supertrend = ta.supertrend(high=df['High'], low=df['Low'], close=df['Close'], length=period, multiplier=multiplier)
    
    # Supertrend columns include Supertrend line and direction
    df['Supertrend'] = supertrend['SUPERT_{}'.format(period)]
    df['Supertrend_Direction'] = supertrend['SUPERTd_{}'.format(period)]
    
    return df

# Add more indicators as needed
