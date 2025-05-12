# database/sync/google/sync_handler.py

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime

# Define el nombre del archivo de las credenciales de Google
CREDENTIALS_FILE = "path/to/your/service-account-file.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Define el ID de la hoja de cálculo y el rango de la hoja
SPREADSHEET_ID = 'your-spreadsheet-id'
RANGE_NAME = 'Sheet1!A1:D10'

# Autenticación con la API de Google Sheets
def authenticate_google_sheets():
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    if not creds or not creds.valid:
        raise Exception("Google credentials invalid or expired.")

    return build('sheets', 'v4', credentials=creds)

# Función para obtener datos de la hoja de cálculo
def get_data_from_sheet():
    try:
        service = authenticate_google_sheets()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return None
        return values
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

# Función para insertar datos en la hoja de cálculo
def insert_data_to_sheet(data):
    try:
        service = authenticate_google_sheets()
        sheet = service.spreadsheets()
        body = {
            'values': data
        }
        result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='RAW', body=body).execute()
        print(f"Data updated: {result.get('updatedCells')} cells updated.")
    except HttpError as err:
        print(f"An error occurred: {err}")

# Función para manejar la sincronización periódica
def sync_data():
    data = get_data_from_sheet()
    if data
