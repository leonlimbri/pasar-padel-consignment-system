import os, json

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_CONNECTION = json.loads(os.getenv("SERVICE_ACCOUNT"))
USER_DETAILS = json.loads(os.getenv("USERNAME_PAIRS"))
USERNAME_PAIRS = {user: userdat["password"] for user, userdat in USER_DETAILS.items()}

def create_service():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_info(SERVICE_CONNECTION, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_data(sheet_id, sheet_name):
    try:
        service = create_service()
        response = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"{sheet_name}!D1"
        ).execute()
        table_range = response.get("values", [[]])[0][0]
        
        response = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"{sheet_name}!{table_range}"
        ).execute()
        
        table_data = response.get("values", [[]])
        table_header = table_data[0]
        table_rows = table_data[1:]
        return table_header, table_rows
    
    except HttpError as err:
        print(err)

def append_data(sheet_id, table_range, *args):
    try:
        service = create_service()
        response = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=table_range,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": args}
        ).execute()
        print(f"Append successful: {response}")

    except HttpError as err:
        print(err)

def update_data(sheet_id, consignment_id, sheet_name, col_ind, col_val):
    try:
        service = create_service()
        table_data = get_data(sheet_id, sheet_name)
        for i, table_row in enumerate(table_data):
            if table_row[0] == consignment_id:
                row = 3+i
                break
        
        service = create_service()
        col = chr(ord("A") + (col_ind))
        body = {"values": [[col_val]]}
        response = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, 
            range=f"{sheet_name}!{col}{row}",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"Update successful: {response}")

    except HttpError as err:
        print(err)