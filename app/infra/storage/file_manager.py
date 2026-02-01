import os
from tempfile import NamedTemporaryFile


def save_temp_file(upload_file, suffix: str) -> str:
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        upload_file.file.seek(0)
        tmp.write(upload_file.file.read())
        return tmp.name


def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
