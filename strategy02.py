from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import os
import json
import yaml
import sys

import pandas_ta as ta
import functionFile as f


def Config_reading():
    print("Reading Config file...\n")
    global api_key,username,pwd,token
    global TelegramBotCredential,ReceiverTelegramID

    # Specify the path to the file
    config_path = '/Users/swapnilk/Desktop/GITHUB/Config.yaml'

    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)  # Exit if the config file doesn't exist
    
    with open(config_path) as file:
        try:
            databaseConfig = yaml.safe_load(file)
            print("Config file loaded successfully.")

            # Access the nested dictionary properly
            credentials = databaseConfig.get('AngelOneCred', {})
            username = credentials.get('username')
            api_key = credentials.get('api_key')
            pwd = credentials.get('pwd')
            token = credentials.get('token')


            # TradeMode = databaseConfig['Algo_Setup']['TradeMode'].upper()
            
            TelegramBotCredential = databaseConfig['Telegram']['TelegramBotCredential']
            ReceiverTelegramID = databaseConfig['Telegram']['Chat_Id']

            if username is None:
                print("Error: 'username' not found in the config file.")
                sys.exit(1)  # Exit if 'userid' is not found
            
        except yaml.YAMLError as exc:
            print(f"Error reading the config file: {exc}")
            sys.exit(1)  # Exit on YAML parsing error

# Call the config reading function
Config_reading()


with open('data.json','r') as jsonFile:
    cred = json.load(jsonFile)

obj = SmartConnect(api_key=cred['api_key'],access_token=cred['access_token'],refresh_token=cred['refresh_token'],feed_token=cred['feed_token'],userId=cred['userId'])


#print(obj.getProfile(cred['refresh_token']))





# Send message to Telegram
message = "LTP data retrieved successfully!"
f.SendMessageToTelegram(message,TelegramBotCredential,ReceiverTelegramID)


# Angel LTP Data Fetching


def getLTP_data():
    LTP = obj.ltpData(exchange='NSE',tradingsymbol='NIFTY',symboltoken='26000')['data']
    open = LTP['open']
    high = LTP['high']
    low = LTP['low']
    close = LTP['close']
    ltp = LTP['ltp']


import util as u

# Fetch historical data
exchange = "NSE"
symboltoken = "3045"
interval = "ONE_MINUTE"
#fromdate = "2024-02-08 09:00"
#todate = "2024-02-08 11:16"


fromdate, todate  = u.get_dynamic_dates(10)
hist_data = u.fetch_historical_data(obj, exchange, symboltoken, interval, fromdate, todate)

import pandas as pd
df = pd.DataFrame(hist_data['data'])

df = df.rename(columns={0:"datetime",1:"open",2:"high",3:"low",4:"Close",5:"volume"})
df['datetime'] = pd.to_datetime(df["datetime"])
df = df.set_index('datetime')
print(df)

import pandas_ta as ta

import indicators as i

df['ema_30'] = i.calculate_ema(df,30)

print(df)

import requests

def initializeSymbolTokenMap():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    global token_df
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({{'strike':float}})




def get_order_info(order_id):
    orb = obj.orderBook()
    # https://www.youtube.com/watch?v=-U8vauvS2MQ&list=PLZ58Qp4m_MwtlvRM4Py2i_VBa0ysuXMdP

import warnings
warnings.filterwarnings('ignore')
from datetime import datetime,date
import math


url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
print(token_df)
token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
token_df = token_df.astype({'strike': float})

print(token_df)

def getTokenInfo (symbol, exch_seg ='NSE',instrumenttype='OPTIDX',strike_price = '',pe_ce = 'CE',expiry_day = None):
    df = token_df
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['expiry']==expiry_day) &  (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])


expiry_day = date(2024,12,5)
symbol = 'NIFTY' #BANKNIFTY | NIFTY
spot_token = getTokenInfo(symbol).iloc[0]['token']
ltpInfo = obj.ltpData('NSE',symbol,spot_token)

indexLtp = ltpInfo['data']['ltp']
print(indexLtp)
ATMStrike = math.ceil(indexLtp/100)*100
print(ATMStrike)

ce_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',ATMStrike,'CE',expiry_day).iloc[0]
print(ce_strike_symbol)

pe_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',ATMStrike,'PE',expiry_day).iloc[0]
print(pe_strike_symbol)



def place_order(token,symbol,qty,buy_sell,ordertype,price,variety= 'NORMAL',exch_seg='NSE',triggerprice=0):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty,
            "triggerprice":triggerprice
            }
        print(orderparams)
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))


place_order(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')
place_order(pe_strike_symbol['token'],pe_strike_symbol['symbol'],pe_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')

# response = requests.get(url)

# if response.status_code == 200:

#     file_path = "ScripMaster.json"

#     with open(file_path,"wb") as file:
#         file.write(response.content)
#         print("JSON data downloaded successfully to : ",file_path)

# else:
#     print("Failed to fetch data from the url : ",url)


# with open(file_path,"r") as file:
#     json_data = pd.DataFrame(json.load(file))

# df = json_data

# token_to_symbol = dict(zip(df['token'],df['symbol']))


