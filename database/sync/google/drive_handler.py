"""
Módulo para interactuar con archivos en Google Drive.
"""
import os
import io
from typing import List, Dict, Any, Optional, Union, BinaryIO
from googleapiclient.http import MediaIoBaseDownload
from .google_client import get_google_client
from ...exceptions.sync_exceptions import FileNotFoundError, DownloadError

class DriveHandler:
    """
    Clase para manejar operaciones con Google Drive.
    """
    
    def __init__(self):
        """Inicializa el manejador con el servicio de Google Drive."""
        self.service = get_google_client().get_drive_service()
    
    def list_files(self, query: str = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Lista archivos en Google Drive, opcionalmente filtrados por una consulta.
        
        Args:
            query: Consulta para filtrar archivos (sintaxis de Google Drive)
            max_results: Número máximo de resultados a devolver
            
        Returns:
            Lista de diccionarios con información de los archivos
            
        Ejemplo de query:
            "mimeType='application/vnd.google-apps.spreadsheet'"  # Solo hojas de cálculo
            "name contains 'finanzas'"  # Archivos con 'finanzas' en el nombre
        """
        try:
            results = self.service.files().list(
                q=query,
                pageSize=max_results,
                fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Error al listar archivos: {str(e)}")
            return []
    
    def get_file_by_id(self, file_id: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un archivo por su ID.
        
        Args:
            file_id: ID único del archivo en Google Drive
            
        Returns:
            Diccionario con información del archivo
            
        Raises:
            FileNotFoundError: Si no se encuentra el archivo
        """
        try:
            return self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, createdTime, modifiedTime, size, webViewLink"
            ).execute()
        except Exception as e:
            raise FileNotFoundError(f"No se pudo encontrar el archivo: {str(e)}")
    
    def download_file(self, file_id: str, output_path: Optional[str] = None) -> Union[str, bytes]:
        """
        Descarga un archivo de Google Drive.
        
        Args:
            file_id: ID único del archivo en Google Drive
            output_path: Ruta donde guardar el archivo (opcional)
            
        Returns:
            Ruta al archivo descargado o contenido del archivo si no se especifica ruta
            
        Raises:
            DownloadError: Si hay un error al descargar el archivo
        """
        try:
            # Obtener información del archivo
            file_metadata = self.get_file_by_id(file_id)
            file_name = file_metadata.get('name', 'downloaded_file')
            
            # Preparar la solicitud de descarga
            request = self.service.files().get_media(fileId=file_id)
            
            # Si no se especifica ruta, usar una temporal basada en el nombre del archivo
            if not output_path:
                # Asegurar que existe el directorio de descargas
                os.makedirs('downloads', exist_ok=True)
                output_path = os.path.join('downloads', file_name)
            
            # Descargar el archivo
            with io.BytesIO() as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Descarga {int(status.progress() * 100)}%.")
                
                # Si se especificó una ruta, guardar el archivo
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(fh.getvalue())
                    return output_path
                else:
                    # Si no, devolver el contenido
                    return fh.getvalue()
                    
        except Exception as e:
            raise DownloadError(f"Error al descargar el archivo: {str(e)}")
    
    def search_files_by_name(self, name: str, exact_match: bool = False) -> List[Dict[str, Any]]:
        """
        Busca archivos por nombre.
        
        Args:
            name: Nombre o parte del nombre a buscar
            exact_match: Si es True, busca coincidencia exacta
            
        Returns:
            Lista de archivos que coinciden con la búsqueda
        """
        query = f"name = '{name}'" if exact_match else f"name contains '{name}'"
        return self.list_files(query=query)
    
    def search_files_by_type(self, mime_type: str) -> List[Dict[str, Any]]:
        """
        Busca archivos por tipo MIME.
        
        Args:
            mime_type: Tipo MIME a buscar
            
        Returns:
            Lista de archivos del tipo especificado
            
        Ejemplos de mime_type:
            'application/vnd.google-apps.spreadsheet' - Hojas de cálculo
            'application/vnd.google-apps.document' - Documentos
            'application/pdf' - PDFs
        """
        query = f"mimeType = '{mime_type}'"
        return self.list_files(query=query)
    
    def get_spreadsheets(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las hojas de cálculo disponibles.
        
        Returns:
            Lista de hojas de cálculo
        """
        return self.search_files_by_type('application/vnd.google-apps.spreadsheet')
    
    def get_recent_files(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene los archivos modificados más recientemente.
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de archivos recientes
        """
        try:
            results = self.service.files().list(
                pageSize=max_results,
                orderBy="modifiedTime desc",
                fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Error al obtener archivos recientes: {str(e)}")
            return []

# Instancia para uso directo
drive_handler = DriveHandler()
