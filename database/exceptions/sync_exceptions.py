"""
Excepciones personalizadas para operaciones de sincronización.
"""

class SyncError(Exception):
    """Excepción base para errores de sincronización."""
    pass

class SheetNotFoundError(SyncError):
    """Se lanza cuando no se encuentra una hoja de cálculo."""
    pass

class DataFormatError(SyncError):
    """Se lanza cuando hay un error en el formato de los datos."""
    pass

class FileNotFoundError(SyncError):
    """Se lanza cuando no se encuentra un archivo."""
    pass

class DownloadError(SyncError):
    """Se lanza cuando hay un error al descargar un archivo."""
    pass

class UploadError(SyncError):
    """Se lanza cuando hay un error al subir un archivo."""
    pass

class ConnectionError(SyncError):
    """Se lanza cuando hay un error de conexión con los servicios de Google."""
    pass

class AuthenticationError(SyncError):
    """Se lanza cuando hay un error de autenticación."""
    pass

class DatabaseError(SyncError):
    """Se lanza cuando hay un error relacionado con la base de datos."""
    pass
