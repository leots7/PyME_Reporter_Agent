from google.oauth2.service_account import Credentials
import gspread

# Ruta al archivo JSON de credenciales
SERVICE_ACCOUNT_FILE = "database/sync/google/service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/spreadsheets"]

def authenticate_google_client():
    """
    Autentica y devuelve el cliente de Google Sheets.
    """
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    return client
