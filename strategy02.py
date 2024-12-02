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


ltp = obj.ltpData(exchange='NSE',tradingsymbol='NIFTY',symboltoken='26000')['data']

print(ltp)



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

def getTokenInfo(exchange):
    strike_price = strike_price*100


def get_order_info(order_id):
    orb = obj.orderBook()
    # https://www.youtube.com/watch?v=-U8vauvS2MQ&list=PLZ58Qp4m_MwtlvRM4Py2i_VBa0ysuXMdP


url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
response = requests.get(url)

if response.status_code == 200:

    file_path = "ScripMaster.json"

    with open(file_path,"wb") as file:
        file.write(response.content)
        print("JSON data downloaded successfully to : ",file_path)

else:
    print("Failed to fetch data from the url : ",url)


with open(file_path,"r") as file:
    json_data = pd.DataFrame(json.load(file))

df = json_data

token_to_symbol = dict(zip(df['token'],df['symbol']))
