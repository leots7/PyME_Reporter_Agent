"""
Cliente para interactuar con la API de Dropbox.
"""
import os
from typing import Dict, Any, List
import dropbox
from dropbox.exceptions import AuthError

from ...config import DROPBOX_CONFIG
from ...exceptions.sync_exceptions import AuthenticationError, ConnectionError

class DropboxClient:
    """
    Cliente para interactuar con la API de Dropbox.
    """
    _instance = None
    
    def __new__(cls):
        """Implementa patrón Singleton para reutilizar el cliente."""
        if cls._instance is None:
            cls._instance = super(DropboxClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el cliente solo una vez."""
        if self._initialized:
            return
            
        try:
            # Verificar si tenemos un token de acceso
            access_token = DROPBOX_CONFIG.get("access_token")
            
            if not access_token:
                raise AuthenticationError(
                    "Se requiere un token de acceso para Dropbox"
                )
            
            # Inicializar cliente con token de acceso
            self.dbx = dropbox.Dropbox(access_token)
            
            # Verificar que el cliente está autenticado
            self.dbx.users_get_current_account()
            
            self._initialized = True
            
        except AuthError as e:
            raise AuthenticationError(f"Error de autenticación con Dropbox: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Error al inicializar el cliente de Dropbox: {str(e)}")
    
    def get_client(self) -> dropbox.Dropbox:
        """Devuelve el cliente de Dropbox."""
        return self.dbx
    
    def test_connection(self) -> Dict[str, Any]:
        """Prueba la conexión a la API de Dropbox."""
        try:
            account = self.dbx.users_get_current_account()
            return {
                "status": "success",
                "message": "Conexión exitosa a Dropbox",
                "account_id": account.account_id,
                "email": account.email,
                "name": f"{account.name.given_name} {account.name.surname}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al conectar con Dropbox: {str(e)}"
            }
    
    def list_files(self, path: str = "") -> List[Dict[str, Any]]:
        """
        Lista archivos y carpetas en una ruta de Dropbox.
        
        Args:
            path: Ruta en Dropbox (vacía para la raíz)
            
        Returns:
            Lista de archivos y carpetas
        """
        try:
            result = self.dbx.files_list_folder(path)
            files = []
            
            for entry in result.entries:
                file_info = {
                    "name": entry.name,
                    "path": entry.path_display,
                    "id": entry.id
                }
                
                # Añadir información específica según el tipo
                if isinstance(entry, dropbox.files.FileMetadata):
                    file_info["type"] = "file"
                    file_info["size"] = entry.size
                    file_info["modified"] = entry.server_modified.isoformat()
                elif isinstance(entry, dropbox.files.FolderMetadata):
                    file_info["type"] = "folder"
                
                files.append(file_info)
                
            return files
            
        except Exception as e:
            raise ConnectionError(f"Error al listar archivos en Dropbox: {str(e)}")
    
    def download_file(self, dropbox_path: str, local_path: str) -> Dict[str, Any]:
        """
        Descarga un archivo de Dropbox a una ubicación local.
        
        Args:
            dropbox_path: Ruta del archivo en Dropbox
            local_path: Ruta local donde guardar el archivo
            
        Returns:
            Información del archivo descargado
        """
        try:
            # Asegurar que el directorio local existe
            os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
            
            # Descargar el archivo
            metadata, response = self.dbx.files_download(dropbox_path)
            
            # Guardar el archivo localmente
            with open(local_path, "wb") as f:
                f.write(response.content)
            
            return {
                "status": "success",
                "message": f"Archivo descargado exitosamente",
                "name": metadata.name,
                "path": dropbox_path,
                "local_path": local_path,
                "size": metadata.size,
                "modified": metadata.server_modified.isoformat()
            }
            
        except Exception as e:
            raise ConnectionError(f"Error al descargar archivo de Dropbox: {str(e)}")
    
    def upload_file(self, local_path: str, dropbox_path: str, overwrite: bool = False) -> Dict[str, Any]:
        """
        Sube un archivo local a Dropbox.
        
        Args:
            local_path: Ruta local del archivo
            dropbox_path: Ruta de destino en Dropbox
            overwrite: Si es True, sobrescribe archivos existentes
            
        Returns:
            Información del archivo subido
        """
        try:
            # Verificar que el archivo local existe
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"Archivo local no encontrado: {local_path}")
            
            # Leer el archivo
            with open(local_path, "rb") as f:
                file_data = f.read()
            
            # Configurar modo de escritura
            mode = dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
            
            # Subir el archivo
            response = self.dbx.files_upload(
                file_data,
                dropbox_path,
                mode=mode
            )
            
            return {
                "status": "success",
                "message": f"Archivo subido exitosamente",
                "name": response.name,
                "path": response.path_display,
                "id": response.id,
                "size": response.size,
                "modified": response.server_modified.isoformat()
            }
            
        except Exception as e:
            raise ConnectionError(f"Error al subir archivo a Dropbox: {str(e)}")

# Instancia global para uso directo
dropbox_client = DropboxClient()

# Función de conveniencia para obtener el cliente
def get_dropbox_client() -> DropboxClient:
    """
    Devuelve una instancia del cliente de Dropbox.
    """
    return dropbox_client


