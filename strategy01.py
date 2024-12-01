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


ltp = obj.ltpData(exchange='NSE',tradingsymbol='NIFTY',symboltoken='26000')['data']

print(ltp)



# Send message to Telegram
message = "LTP data retrieved successfully!"
f.SendMessageToTelegram(message,TelegramBotCredential,ReceiverTelegramID)

