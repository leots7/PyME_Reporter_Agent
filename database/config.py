"""
Configuración para la conexión con servicios externos y base de datos.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de base de datos
DATABASE_CONFIG = {
    "url": os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/pyme_reporter"),
    "echo": os.getenv("DB_ECHO", "True").lower() in ("true", "1", "t"),
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
}

# Configuración de Google API
GOOGLE_API_CONFIG = {
    # Ruta al archivo de credenciales de cuenta de servicio
    "service_account_file": os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE", 
        "database/sync/google/service_account.json"
    ),
    # Ámbitos (scopes) requeridos para las APIs
    "scopes": [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly"
    ],
    # ID de la hoja de cálculo principal (opcional)
    "default_spreadsheet_id": os.getenv("GOOGLE_DEFAULT_SPREADSHEET_ID", ""),
}

# Configuración de Dropbox
DROPBOX_CONFIG = {
    "app_key": os.getenv("DROPBOX_APP_KEY", ""),
    "app_secret": os.getenv("DROPBOX_APP_SECRET", ""),
    "refresh_token": os.getenv("DROPBOX_REFRESH_TOKEN", ""),
    "access_token": os.getenv("DROPBOX_ACCESS_TOKEN", ""),
}

# Directorios para archivos sincronizados
SYNC_DIRECTORIES = {
    "downloads": os.getenv("SYNC_DOWNLOADS_DIR", "downloads"),
    "uploads": os.getenv("SYNC_UPLOADS_DIR", "uploads"),
    "temp": os.getenv("SYNC_TEMP_DIR", "temp"),
}

# Asegurar que los directorios existan
for dir_path in SYNC_DIRECTORIES.values():
    os.makedirs(dir_path, exist_ok=True)

def get_service_account_path() -> str:
    """
    Obtiene la ruta completa al archivo de cuenta de servicio.
    
    Returns:
        Ruta absoluta al archivo de credenciales
    """
    path = GOOGLE_API_CONFIG["service_account_file"]
    
    # Si la ruta es relativa, convertirla a absoluta
    if not os.path.isabs(path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, path)
    
    return path

def validate_config() -> Dict[str, bool]:
    """
    Valida que la configuración necesaria esté presente.
    
    Returns:
        Diccionario con el estado de validación de cada servicio
    """
    validation = {
        "database": bool(DATABASE_CONFIG["url"]),
        "google_api": os.path.exists(get_service_account_path()),
        "dropbox": bool(DROPBOX_CONFIG["app_key"] and DROPBOX_CONFIG["app_secret"]),
    }
    
    return validation

