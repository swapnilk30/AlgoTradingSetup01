## Angel Broking Smart API Setup Guide with Full Python API Source

1. Open Angel One Account
2. Register For Angel One SmartAPI
```
https://smartapi.angelbroking.com/signup
```
3. Enable TOTP from the top menu and copy 
4. Create An app to get API from smartapi in angel broking.
```
Go to My profile > My API > Create an app
```
```
Now here you need to fill in information Like

Select: Trading
App name: anything you want
URL : https://smartapi.angelbroking.com/
POST URL: https://smartapi.angelbroking.com/
Angel Client ID : Optional
```

5. Download your Favorite python code editor or use VS Code 

6. Now Open VS Code terminal in your directory and run these Python commands.
```
pip install smartapi-python
pip install websocket-client
```