import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CONNECTION = os.getenv("CONNECTION")

def create_connection():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CONNECTION, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    return creds

def get_data(creds, sheet_id, sheet_name):
    try:
        service = build("sheets", "v4", credentials=creds)
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

def append_data(creds, sheet_id, table_range, *args):
    try:
        service = build("sheets", "v4", credentials=creds)
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

def update_data(creds, sheet_id, consignment_id, sheet_name, col_ind, col_val):
    try:
        table_data = get_data(creds, sheet_id, sheet_name)
        for i, table_row in enumerate(table_data):
            if table_row[0] == consignment_id:
                row = 3+i
                break
        
        service = build("sheets", "v4", credentials=creds)
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