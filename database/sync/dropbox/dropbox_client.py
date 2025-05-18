"""Cliente para interactuar con la API de Dropbox."""
import os
from typing import Dict, Any, Optional
import dropbox
from dropbox.exceptions import AuthError
from dotenv import load_dotenv

from database.exceptions.sync_exceptions import AuthenticationError, ConnectionError

# Cargar variables desde el archivo .env
load_dotenv()

class DropboxClient:
    """Cliente para interactuar con la API de Dropbox."""
    
    def __init__(self, auto_connect=False):
        """
        Inicializa el cliente de Dropbox.
        
        Args:
            auto_connect: Si es True, intenta conectarse automáticamente
        """
        self.dbx = None
        self.config = {
            "access_token": os.getenv("DROPBOX_ACCESS_TOKEN"),
            "refresh_token": os.getenv("DROPBOX_REFRESH_TOKEN"),
            "app_key": os.getenv("DROPBOX_APP_KEY"),
            "app_secret": os.getenv("DROPBOX_APP_SECRET")
        }
        
        # Validar que las credenciales necesarias estén presentes
        if not self.config["refresh_token"] or not self.config["app_key"] or not self.config["app_secret"]:
            raise AuthenticationError("Falta el refresh token o las claves de la aplicación en la configuración")

        # Solo conectar si auto_connect es True
        if auto_connect:
            self._connect()
    
    def _connect(self):
        """Establece la conexión con Dropbox priorizando el refresh token."""
        try:
            refresh_token = self.config["refresh_token"]
            app_key = self.config["app_key"]
            app_secret = self.config["app_secret"]
            access_token = self.config["access_token"]
            
            if refresh_token:
                self.dbx = dropbox.Dropbox(
                    app_key=app_key,
                    app_secret=app_secret,
                    oauth2_refresh_token=refresh_token  # ✅ Se prioriza el refresh token
                )
            elif access_token:
                self.dbx = dropbox.Dropbox(access_token)
            else:
                raise AuthenticationError("No se encontró un método válido de autenticación con Dropbox")
                
            # Verificar que la conexión funciona correctamente
            self.dbx.users_get_current_account()
            
        except AuthError as e:
            raise AuthenticationError(f"Error de autenticación con Dropbox: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Error conectando con Dropbox: {str(e)}")
    
    def ensure_connected(self):
        """Asegura que hay una conexión activa a Dropbox."""
        if self.dbx is None:
            self._connect()
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Prueba la conexión a Dropbox.
        
        Returns:
            Dict con información sobre el resultado de la prueba
        """
        result = {
            "status": "not_tested",
            "message": ""
        }
        
        try:
            self.ensure_connected()
            account = self.dbx.users_get_current_account()
            result["status"] = "success"
            result["name"] = account.name.display_name
            result["email"] = account.email
            result["account_id"] = account.account_id
        except AuthenticationError as e:
            result["status"] = "error"
            result["message"] = str(e)
        except Exception as e:
            result["status"] = "error"
            result["message"] = f"Error inesperado: {str(e)}"
            
        return result

# Función para obtener una instancia del cliente
def get_dropbox_client(auto_connect=False) -> DropboxClient:
    """
    Obtiene una instancia del cliente de Dropbox.
    
    Args:
        auto_connect: Si es True, intenta conectarse automáticamente
        
    Returns:
        Instancia de DropboxClient
    """
    return DropboxClient(auto_connect=auto_connect)



