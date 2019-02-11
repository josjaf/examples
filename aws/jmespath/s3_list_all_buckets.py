import boto3
import jmespath
session = boto3.Session()
s3 = session.client('s3')
response = s3.list_buckets()
buckets = jmespath.search("Buckets[].Name", response)
for bucket in buckets:
    print(bucket)


