import requests
import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import time

load_dotenv()

# google sheets API setup
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('gsheet_creds.json', scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("canal_Ids.csv").sheet1
    return sheet

X_CANAL_APP_ID = os.getenv('X_CANAL_APP_ID')
X_CANAL_APP_TOKEN = os.getenv('X_CANAL_APP_TOKEN')
CANAL_BASE_URL = os.getenv('CANAL_BASE_URL')
CANAL_RESYNC_PATH='/platform/products/{product_id}/resync/'

def resync_product(product_id):
    url = f'{CANAL_BASE_URL}{CANAL_RESYNC_PATH}'.format(product_id=product_id)
    headers = {
        'X-CANAL-APP-ID': X_CANAL_APP_ID,
        'X-CANAL-APP-TOKEN': X_CANAL_APP_TOKEN
        }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            print(f'successfully resynced {product_id} \n {response.json()} \n')    
    except requests.exceptions.HTTPError as http_err:
        print(f'failed to resync {product_id} with status: {response.status_code} and error: {http_err}\n')

if __name__ == '__main__':
    sheet = setup_google_sheets()
    canal_product_ids = sheet.col_values(2)[1:]
    
    for product_id in canal_product_ids:
        resync_product(product_id)
        time.sleep(1)