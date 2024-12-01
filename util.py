

from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import os
import json



# Function to fetch historical data
def fetch_historical_data(smartApi, exchange, symboltoken, interval, fromdate, todate):
    """
    Fetch historical candle data using SmartAPI.

    Parameters:
        smartApi (SmartConnect): SmartAPI instance.
        exchange (str): Exchange name (e.g., NSE, BSE).
        symboltoken (str): Symbol token of the stock.
        interval (str): Time interval (e.g., ONE_MINUTE, ONE_DAY).
        fromdate (str): Start date in "YYYY-MM-DD HH:MM" format.
        todate (str): End date in "YYYY-MM-DD HH:MM" format.

    Returns:
        dict: Historical data retrieved from the API.
    """
    try:
        historicParam = {
            "exchange": exchange,
            "symboltoken": symboltoken,
            "interval": interval,
            "fromdate": fromdate,
            "todate": todate,
        }
        hist_data = smartApi.getCandleData(historicParam)
        logger.info("Historical data fetched successfully.")
        return hist_data
    except Exception as e:
        logger.exception(f"Failed to fetch historical data: {e}")
        return None






from datetime import datetime, timedelta

# Dynamic date calculation
def get_dynamic_dates(days):
    """
    Get dynamic fromdate and todate for the past `days` days.

    Parameters:
        days (int): Number of past days to fetch data for.

    Returns:
        tuple: (fromdate, todate) in "YYYY-MM-DD HH:MM" format.
    """
    todate = datetime.now()
    fromdate = todate - timedelta(days=days)
    return fromdate.strftime("%Y-%m-%d %H:%M"), todate.strftime("%Y-%m-%d %H:%M")


# Get fromdate and todate for the last 10 days
#fromdate, todate = get_dynamic_dates(10)
#print(fromdate,"   ",todate)


def place_order(obj, variety, tradingsymbol, symboltoken, transactiontype, exchange, ordertype, 
                producttype, duration, price, quantity, squareoff="0", stoploss="0"):
    """
    Places an order using the provided parameters.

    Parameters:
        obj (object): The trading API object (e.g., SmartAPI instance).
        variety (str): Order variety (e.g., NORMAL, AMO).
        tradingsymbol (str): Trading symbol of the stock.
        symboltoken (str): Symbol token of the stock.
        transactiontype (str): Transaction type (BUY or SELL).
        exchange (str): Exchange (e.g., NSE, BSE).
        ordertype (str): Order type (e.g., LIMIT, MARKET).
        producttype (str): Product type (e.g., INTRADAY, DELIVERY).
        duration (str): Order duration (e.g., DAY, IOC).
        price (str): Order price.
        quantity (str): Order quantity.
        squareoff (str, optional): Square-off value for the order. Defaults to "0".
        stoploss (str, optional): Stop-loss value for the order. Defaults to "0".

    Returns:
        str: The order ID if the order is placed successfully.
        None: If the order placement fails.
    """
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": transactiontype,
            "exchange": exchange,
            "ordertype": ordertype,
            "producttype": producttype,
            "duration": duration,
            "price": price,
            "squareoff": squareoff,
            "stoploss": stoploss,
            "quantity": quantity,
        }
        order_id = obj.placeOrder(orderparams)
        print("The order ID is: {}".format(order_id))
        return order_id
    except Exception as e:
        print("Order placement failed: {}".format(str(e)))
        return None

# Example usage:
'''
try:
    order_id = place_order(
        obj=obj,
        variety="NORMAL",
        tradingsymbol="SBIN-EQ",
        symboltoken="3045",
        transactiontype="BUY",
        exchange="NSE",
        ordertype="LIMIT",
        producttype="INTRADAY",
        duration="DAY",
        price="19500",
        quantity="1"
    )
except Exception as e:
    print("An error occurred while placing the order: {}".format(e))

'''
