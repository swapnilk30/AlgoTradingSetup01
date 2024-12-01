import sys
import os
#print(os.getcwd())
import json
import requests
from datetime import datetime as dt
from datetime import time,timedelta as td
from pytz import timezone
from time import sleep

import pandas_ta as ta

try:
    import yaml
except ImportError:
    os.system('python3 -m pip install --user pyyaml')
    import yaml  # Retry importing after installation



# Specify the path to the file
config_path = '/Users/swapnilk/Desktop/GITHUB/Config.yaml'

# Read the YAML file
try:
    with open(config_path, 'r') as file:

        config_data = yaml.safe_load(file)
        print("Config file loaded successfully.")

        userid = config_data.get('userid', None)
        password = config_data['Credential']['password']

    # Print the contents
    #print(config_data)

except FileNotFoundError:
    print(f"File not found: {config_path}")
except yaml.YAMLError as e:
    print(f"Error reading YAML file: {e}")

