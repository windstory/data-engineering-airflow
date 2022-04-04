from oauth2client.service_account import ServiceAccountCredentials
from airflow.models import Variable

import gspread
import os
import pandas as pd

def write_gspread_keyfile():
    content = Variable.get('google_sheet_access_token')
    file_name = 'google_sheet_access_token.json'
    f = open(file_name, 'w')
    f.write(content)
    f.close()

    return os.getcwd() + os.sep + file_name 

def get_gspread_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    json_keyfile_path = write_gspread_keyfile()
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    return gspread.authorize(credentials)
    
def get_csv_from_google_sheet(csv_file_name, url, sheet_name=None):
    gc = get_gspread_client()
    sheet_instance = gc.open_by_url(url)
    if sheet_name:
        sheet = sheet_instance.worksheet(sheet_name)
    else:
        sheet = sheet_instance.sheet1

    header = sheet.get_all_values()[0]
    data = sheet.get_all_values()[1:]

    pd.DataFrame(data, columns=header).to_csv(
        csv_file_name,
        index=False,
        header=True,
        encoding='utf-8'
    )
