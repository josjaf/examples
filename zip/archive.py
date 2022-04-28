import os
from io import BytesIO
from zipfile import ZipFile, ZipInfo

from pathlib import Path

def in_memory_zip(directory: Path, working_directory='../'):
    os.chdir(working_directory)
    archive = BytesIO()
    with ZipFile(archive, 'w') as zip_archive:
        # Create three files on zip archive
        for file_path in directory.rglob("**/*"):

            if file_path.suffix in ['.zip', '*.pyc']: continue
            if any(item in ['.git', '.eggs', '.idea', '__pycache__', ] for item in file_path.parts): continue
            if file_path.is_dir(): continue
            print(file_path)
            file1 = ZipInfo(str(file_path.relative_to(Path.cwd())))
            zip_archive.writestr(file1, file_path.read_bytes())
    return archive
if __name__ == '__main__':
    directory = Path.cwd()
    archive = in_memory_zip(directory, '../')
    with open('config1.zip', 'wb') as f:
        f.write(archive.getbuffer())