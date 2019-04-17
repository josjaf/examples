import zipfile
import os

def create_zip(dir, ignore_folder_root=True):


    ignored = ['.zip', '.pyc', '.tar', '.gz']
    zipname = str('source.zip')
    z = zipfile.ZipFile(zipname, "w")
    path = os.path.abspath('.')
    path = os.path.join(path, zipname)
    print(f"Creating Zip: {path} of {dir}")
    if dir.startswith('~'):
        #raise RuntimeError('Tilde not suported')
        dir = os.path.expanduser(dir)
        print(dir)
    if dir.startswith('/'):
        print('got absolute path')

    if ignore_folder_root:
        # default behavior, do not include prefix in the zip
        os.chdir(dir)
        dir = '.'
    for root, dirs, files in os.walk(dir):

        # avoid infinite zip recursion
        for file in files:
            if file.endswith(tuple(ignored)): continue
            if file == zipname: continue
            #print(os.path.join(root, file))
            z.write(os.path.join(root, file))
    z.close()
    return zipname

create_zip('~/workspace/newport_automated_security')
# create_zip('.')

