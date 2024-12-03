from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import os
import json
import yaml
import sys
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
message = "Login successfully!"
f.SendMessageToTelegram(message,TelegramBotCredential,ReceiverTelegramID)


import warnings
warnings.filterwarnings('ignore')
from datetime import datetime,date
import math
import requests
import pandas as pd

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
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

#place_order(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')
#place_order(pe_strike_symbol['token'],pe_strike_symbol['symbol'],pe_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')

