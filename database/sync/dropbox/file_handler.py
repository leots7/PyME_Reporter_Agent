"""Módulo para operaciones con archivos en Dropbox."""
import dropbox.files  # ✅ Agregado para usar WriteMode correctamente
from database.sync.dropbox.dropbox_client import get_dropbox_client

def list_files(path=""):
    """
    Lista los archivos y carpetas en la ruta especificada en Dropbox.
    """
    dbx = get_dropbox_client(auto_connect=True).dbx
    try:
        result = dbx.files_list_folder(path)
        return [entry.name for entry in result.entries]
    except Exception as e:
        print(f"❌ Error al listar archivos en '{path}': {e}")
        return []

def upload_file(local_path, dropbox_path):
    """
    Sube un archivo desde local a Dropbox.
    """
    dbx = get_dropbox_client(auto_connect=True).dbx
    try:
        with open(local_path, "rb") as f:
            dbx.files_upload(
                f.read(),
                dropbox_path,
                mode=dropbox.files.WriteMode.overwrite  # ✅ Corrección aquí
            )
        print(f"✅ Archivo '{local_path}' subido a Dropbox en '{dropbox_path}'")
    except FileNotFoundError:
        print(f"❌ El archivo local '{local_path}' no existe.")
    except Exception as e:
        print(f"❌ Error subiendo archivo: {e}")

def download_file(dropbox_path, local_path):
    """
    Descarga un archivo de Dropbox a la ruta local.
    """
    dbx = get_dropbox_client(auto_connect=True).dbx
    try:
        metadata, res = dbx.files_download(dropbox_path)
        with open(local_path, "wb") as f:
            f.write(res.content)
        print(f"✅ Archivo '{dropbox_path}' descargado a '{local_path}'")
    except Exception as e:
        print(f"❌ Error descargando archivo: {e}")

if __name__ == "__main__":
    print("📂 Archivos en la raíz de Dropbox:")
    for nombre in list_files(""):
        print(" -", nombre)
