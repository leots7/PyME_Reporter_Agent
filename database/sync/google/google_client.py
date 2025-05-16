"""
Cliente para interactuar con las APIs de Google (Sheets y Drive).
"""
import os
from typing import Optional, List
from google.oauth2.service_account import Credentials
import gspread
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ...config import GOOGLE_API_CONFIG, get_service_account_path
from ...exceptions.sync_exceptions import AuthenticationError, ConnectionError

class GoogleClient:
    """
    Cliente unificado para interactuar con las APIs de Google.
    """
    _instance = None
    
    def __new__(cls):
        """Implementa patrón Singleton para reutilizar el cliente."""
        if cls._instance is None:
            cls._instance = super(GoogleClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el cliente solo una vez."""
        if self._initialized:
            return
            
        try:
            # Obtener ruta al archivo de credenciales
            service_account_file = get_service_account_path()
            
            # Verificar que el archivo existe
            if not os.path.exists(service_account_file):
                raise AuthenticationError(
                    f"Archivo de credenciales no encontrado: {service_account_file}"
                )
            
            # Obtener ámbitos de la configuración
            scopes = GOOGLE_API_CONFIG["scopes"]
            
            # Inicializar credenciales
            self.credentials = Credentials.from_service_account_file(
                service_account_file, 
                scopes=scopes
            )
            
            # Inicializar clientes
            self.sheets_client = gspread.authorize(self.credentials)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            
            self._initialized = True
            
        except AuthenticationError:
            # Re-lanzar excepciones de autenticación
            raise
        except Exception as e:
            raise ConnectionError(f"Error al inicializar el cliente de Google: {str(e)}")
    
    def get_sheets_client(self) -> gspread.Client:
        """Devuelve el cliente de Google Sheets."""
        return self.sheets_client
    
    def get_drive_service(self):
        """Devuelve el servicio de Google Drive."""
        return self.drive_service
    
    def test_connection(self) -> dict:
        """Prueba la conexión a las APIs de Google."""
        try:
            # Probar Sheets
            spreadsheets = self.sheets_client.openall()
            sheet_count = len(spreadsheets)
            
            # Probar Drive
            results = self.drive_service.files().list(
                pageSize=1, 
                fields="nextPageToken, files(id, name)"
            ).execute()
            
            return {
                "status": "success",
                "message": "Conexión exitosa a las APIs de Google",
                "sheets_available": sheet_count,
                "drive_connected": True
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al conectar con las APIs de Google: {str(e)}"
            }

# Función de conveniencia para obtener el cliente
def get_google_client() -> GoogleClient:
    """
    Devuelve una instancia del cliente de Google.
    """
    return GoogleClient()
