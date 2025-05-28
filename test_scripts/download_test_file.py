# test_scripts/download_test_file.py
from database.sync.dropbox.file_handler import download_file

if __name__ == "__main__":
    dropbox_path = "/PyME_Manager/Luke Skywalker.txt"
    local_path = "downloads/Luke Skywalker.txt"
    download_file(dropbox_path, local_path)
