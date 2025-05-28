from database.sync.dropbox.file_handler import download_file
import os

def test_download():
    dropbox_path = "/clientes/test_user/test_upload.txt"
    local_path = "test_download.txt"
    
    resultado = download_file(dropbox_path, local_path)
    print(resultado)
    
    # Validar que el archivo se descargó correctamente
    assert resultado["status"] == "success"
    assert os.path.exists(local_path)
    
    # Limpiar archivo de prueba
    if os.path.exists(local_path):
        os.remove(local_path)

if __name__ == "__main__":
    test_download()
