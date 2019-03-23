import os
def wildcard_delete(extension, directory='.'):
    assert extension, f"Got Blank Extension"
    for subdir, dirs, files in os.walk(directory):
        for file in files:

            full_path = (os.path.abspath(os.path.join(subdir, file)))
            if full_path.endswith(extension):
                print(f"Removing {full_path}")
                #os.remove(full_path)
    return
wildcard_delete(extension='.zip', directory='.')