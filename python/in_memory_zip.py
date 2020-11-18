import io
from io import BytesIO
from zipfile import ZipFile
import json
import boto3
import zipfile
def main():
    session = boto3.session.Session()
    data = dict(Region='us-east-1', Namespace='sn-prod')
    data = json.dumps(data)

    s3 = session.client('s3')

    response = s3.put_object(Bucket='josjaf', Key='prod_data.json',  Body=data)
    print(response)
    in_memory = BytesIO()
    zf = ZipFile(in_memory, mode="w")
    zf.writestr("prod_data.json", data)
    zf.close()
    in_memory.seek(0)
    data = in_memory.read()
    response = s3.put_object(Bucket='josjaf', Key='prod_data.zip',  Body=data)


    return

if __name__ == '__main__':
    main()