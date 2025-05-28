import os
from dotenv import load_dotenv
import dropbox

load_dotenv()  # Asume que el .env está en el mismo directorio o que lo definís con ruta absoluta

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

print(f"Access Token: {DROPBOX_ACCESS_TOKEN}")
print(f"Refresh Token: {DROPBOX_REFRESH_TOKEN}")
print(f"App Key: {DROPBOX_APP_KEY}")
print(f"App Secret: {DROPBOX_APP_SECRET}")

try:
    dbx = dropbox.Dropbox(
        oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
        app_key=DROPBOX_APP_KEY,
        app_secret=DROPBOX_APP_SECRET,
    )
    print("Cliente Dropbox creado correctamente.")
except Exception as e:
    print(f"Error creando cliente Dropbox: {e}")
