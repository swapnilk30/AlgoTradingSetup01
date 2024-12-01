from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import os
import json


with open('data.json','r') as jsonFile:
    cred = json.load(jsonFile)

obj = SmartConnect(api_key=cred['api_key'],access_token=cred['access_token'],refresh_token=cred['refresh_token'],feed_token=cred['feed_token'],userId=cred['userId'])


#print(obj.getProfile(cred['refresh_token']))


ltp = obj.ltpData(exchange='NSE',tradingsymbol='NIFTY',symboltoken='26000')['data']

print(ltp)