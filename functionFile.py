import json
from logzero import logger


# Function to save the refresh token to a file
def save_refresh_token(token, filename="refresh_token.json"):
    try:
        with open(filename, 'w') as file:
            json.dump({"refreshToken": token}, file)
        print(f"Refresh token saved to {filename}")
    except Exception as e:
        logger.exception(f"Failed to save refresh token: {e}")


# Function to read the refresh token from a file
def read_refresh_token(filename="refresh_token.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get("refreshToken", None)
    except FileNotFoundError:
        logger.error(f"{filename} not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {filename}.")
        return None
    except Exception as e:
        logger.exception(f"Failed to read refresh token: {e}")
        return None
    
import requests

def SendMessageToTelegram(Message,TelegramBotCredential,ReceiverTelegramID):
    try:
        Url = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendMessage?chat_id=" + str(ReceiverTelegramID)
        
        textdata ={ "text":Message}
        response = requests.request("POST",Url,params=textdata)
    except Exception as e:
        Message = str(e) + ": Exception occur in SendMessageToTelegram"
        print(Message)  

        
def SendTelegramFile(FileName,TelegramBotCredential,ReceiverTelegramID):
    Documentfile={'document':open(FileName,'rb')}
    
    Fileurl = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendDocument?chat_id=" + str(ReceiverTelegramID)
      
    response = requests.request("POST",Fileurl,files=Documentfile)

    print("Status Code : ",response.status_code)