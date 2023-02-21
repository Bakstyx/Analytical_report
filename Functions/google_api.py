#Libraries
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
from datetime import date


#Functions
# === Google API - Spreadsheets ===
#Execute one time. To generate the token
#Requiere a google account, and go to google cluod platform. 
#Create and Download the OAUTH json and rename as 'Credentials.json'
#Credentials MUST BE in the same directory than this file.

#Generate credential and tokens
def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './Credentials/Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

#Check API credntials
""" Intermediary function to check the credentials. 
Avoiding break if credentials are no ok"""

def credentials_check(SCOPES):
    try:
        #SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = gsheet_api_check(SCOPES)
        print("Credentials check successful.")
        return creds
    except:
        print('Credentials check unsuccessful. Chech credential or folder')

#extract spreadsheet id from url
def extract_id_from_url(url):
    components = str(url).split('/')
    id=components[-2]
    return id


#Pull the spreadsheets.
def pull_sheet_data(Spreadsheet_url,data_to_pull):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = credentials_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = extract_id_from_url(Spreadsheet_url)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=data_to_pull).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=data_to_pull).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data