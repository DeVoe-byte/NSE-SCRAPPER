import requests
import json
import pandas as pd
import xlwings as xw
from df2gspread import df2gspread as d2g

import gspread 
from oauth2client.service_account import  ServiceAccountCredentials

pd.set_option('display.width', 1500)
pd.set_option('display.max_columns', 75)
pd.set_option('display.max_row', 2500)

url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
found = False
while not found:
    try:
        data = requests.get(url, headers=urlheader).content
        data2 = data.decode('utf-8')
        df = json.loads(data2)
        expiry_dt = df['records']['expiryDates'][0]

        found = True
    except:
        pass

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
"accept-language": "en-US,en;q=0.9,hi;q=0.8","accept-encoding": "gzip, deflate, br"}

    cookie_dict = {'bm_sv' : 'AA02590AB18B4FC4A036CC62F5230694~8py6nqGfKvu3P4aKZoNpf4HZOUYQJ4i6JMyPMX14ksLZYE+0HlglIA3S2AAa9JGJPvXrBHcJ7uS2ZMcMq3f+FZ/ttHuqFzuAmMf1ZnI9hFgpqB7USISOoa3NfzMufwVAd0U7MgeSxF7+GjuyOuApyOQcoHmyr53hB4JLSqd0U1s'}
    
    session = requests.session()
    
    for cookie in cookie_dict:
        session.cookies.set(cookie,cookie_dict[cookie])


expiry = '16-Jul-2020'


def fetch_oi():
   
   r = session.get(url, headers=headers).json()
   #print(r)      PRINT 1 - THIS PRINT IS WORKING 

   if expiry:
      ce_values = [data['CE'] for data in r ['records']['data'] if "CE" in data and str(data['expiryDate'].lower() == str(expiry).lower())]
      pe_values = [data['PE'] for data in r ['records']['data'] if "PE" in data and str(data['expiryDate'].lower() == str(expiry).lower())]
   else:
     ce_values = [data['CE'] for data in r ['filtered']['data'] if "CE" in data]
     pe_values = [data['PE'] for data in r ['filtered']['data'] if "PE" in data]
     print(ce_values) # PRINT 2 NO OUTPUT NO ERROR
     
     ce_data = pd.DataFrame(ce_values)
     pe_data = pd.DataFrame(pe_values)
     ce_data = ce_data.sort_values(['strikePrice'])
     pe_data = pe_data.sort_values(['strikePrice'])
     print(ce_values)      # PRINT 3 NO OUTPUT NO ERROR    
    

def main():
    fetch_oi()

if __name__ == '__main__':
    main()
