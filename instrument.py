
#Get Master List
import pandas as pd
import requests
url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'] , format = "mixed").apply(lambda x: x.date())
token_df = token_df.astype({'strike': float})
#print(token_df)


token_df[  (token_df.instrumenttype == 'AMXIDX')].head(50)
#token_df = token_df[(token_df.name == 'BANKNIFTY') & ((token_df.instrumenttype == 'AMXIDX'))]
#token_df[(token_df.name == 'SENSEX') & ((token_df.instrumenttype == 'AMXIDX'))]
#token_df[(token_df.name == 'MIDCPNIFTY') & ((token_df.instrumenttype == 'AMXIDX'))]
#token_df[(token_df.name == 'BANKEX') & ((token_df.instrumenttype == 'AMXIDX'))]

token_df = token_df[(token_df.name == 'NIFTY') & ((token_df.instrumenttype == 'AMXIDX'))]

print(token_df)