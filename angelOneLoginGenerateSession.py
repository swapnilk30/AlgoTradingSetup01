from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import os
import json
import sys
import yaml
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


def getLogin():
        
    # Initialize SmartAPI
    smartApi = SmartConnect(api_key)
    
    try:
        # Generate TOTP (Time-based OTP)
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    # Generate session
    try:
        data = smartApi.generateSession(username, pwd, totp)

        if not data.get('status', True):
            logger.error(f"Login failed: {data.get('message', 'Unknown error')}")
            return

        # Extract and save tokens
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        f.save_refresh_token(refreshToken)
        logger.info("Authentication successful.")

        # Fetch profile
        res = smartApi.getProfile(refreshToken)
        print("Profile Data:", res)

        #Generate Session
        cred = {'access_token':smartApi.access_token,'refresh_token':smartApi.refresh_token,'feed_token':smartApi.feed_token,'userId':username,'api_key':api_key}
        with open("data.json","w") as jsonFile:
            json.dump(cred,jsonFile)

    except Exception as e:
        logger.exception(f"Authentication failed: {e}")
        return


getLogin()