import zipfile
import os


def create_zip(dir_to_zip, zip_path=None, ignore_folder_root=True):
    ignored = ['.zip', '.pyc', '.tar', '.gz']

    # process zip path
    if not zip_path:
        zip_path = str('source.zip')

    if not zip_path.endswith('.zip'):
        zip_path = zip_path + '.zip'
    if not os.path.isabs(zip_path):
        zip_path = os.path.abspath(zip_path)
    print(f"Zip Path: {zip_path}")
    z = zipfile.ZipFile(zip_path, "w")

    path = os.path.abspath('.')
    path = os.path.join(path, zip_path)
    print(f"Creating Zip: {zip_path} of {dir_to_zip}")

    if dir_to_zip.startswith('~'):
        # raise RuntimeError('Tilde not suported')
        dir_to_zip = os.path.expanduser(dir_to_zip)
        print(dir_to_zip)
    if dir_to_zip.startswith('/'):
        print('got absolute path')

    original_dir = os.path.abspath(os.path.curdir)
    if ignore_folder_root:
        # default behavior, do not include prefix in the zip

        os.chdir(dir_to_zip)
        dir_to_zip = '.'
    # print(f"Current Directory: {os.path.abspath(os.curdir)}")
    for root, dirs, files in os.walk(dir_to_zip):

        # avoid infinite zip recursion
        for file in files:
            if file.endswith(tuple(ignored)): continue
            if file == zip_path: continue
            # print(os.path.join(root, file))
            z.write(os.path.join(root, file))
    z.close()
    # switch back to original working directory
    os.chdir(original_dir)
    return zip_path


create_zip(dir_to_zip='~/pworkspace/examples', zip_path='examples.zip',
           ignore_folder_root=True)
create_zip(dir_to_zip='.', zip_path='test.zip',
           ignore_folder_root=True)


