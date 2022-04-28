import os
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
# go up one dir
os.chdir('../')
directory = Path.cwd()
zip_path = Path.cwd().joinpath("archive.zip")
print(f"Writing {zip_path}")
with ZipFile(f"{zip_path}", mode="w") as archive:
     for file_path in directory.rglob("**/*"):

         if file_path.suffix in ['.zip', '*.pyc']: continue
         if any(item in ['.git', '.eggs', '.idea', '__pycache__', ] for item in file_path.parts): continue
         print(f"Writing {file_path}")
         archive.write(file_path,arcname=file_path.relative_to(directory.parent))