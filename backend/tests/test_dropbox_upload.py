from database.sync.dropbox.file_handler import upload_file

def main():
    local_file = "test_upload.txt"
    dropbox_path = "/clientes/test_user/test_upload.txt"

    # Crear archivo local simple
    with open(local_file, "w") as f:
        f.write("Archivo de prueba para Dropbox\n")

    # Subir archivo a Dropbox
    result = upload_file(local_file, dropbox_path)
    print(result)

if __name__ == "__main__":
    main()
