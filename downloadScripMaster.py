



import warnings
warnings.filterwarnings('ignore')
from datetime import datetime,date,timedelta,time
import math
import requests
import pandas as pd

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

#d = requests.get(url).json()
#token_df = pd.DataFrame.from_dict(d)
#token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
#token_df = token_df.astype({'strike': float})
#print(token_df)

response = requests.get(url)

if response.status_code == 200:
    file_path = "ScripMaster.json"
    
    with open(file_path,"wb") as file:
        file.write(response.content)
        print("JSON data downloaded successfully to : ",file_path)

else:
    print("Failed to fetch data from the url : ",url)


# with open(file_path,"r") as file:
#     json_data = pd.DataFrame(json.load(file))

# df = json_data

# token_to_symbol = dict(zip(df['token'],df['symbol']))