# test_scripts/upload_test_file.py

import os
import sys

# Asegurar que la raíz del proyecto esté en sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # test_scripts/
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))       # PyME_Reporter_Agent/
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.sync.dropbox.file_handler import upload_file

# Ruta del archivo local a subir
local_path = os.path.join("test_scripts", "files", "Luke Skywalker.txt")

# Ruta destino en Dropbox
dropbox_path = "/PyME_Manager/Luke Skywalker.txt"

# Subida del archivo
upload_file(local_path, dropbox_path)
