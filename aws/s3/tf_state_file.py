import random
import string

import boto3
import botocore
from botocore.exceptions import ClientError
import sys

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    session = boto3.session.Session()
    s3 = session.client('s3')
    bucket = sys.argv[1]
    print(f"Processing Bucket:w {bucket}")
    create_bucket_kwargs = dict(Bucket=bucket)
    if session.region_name != 'us-east-1':
        print("Adding Location Constraint to Payload")
        create_bucket_kwargs['CreateBucketConfiguration'] = {'LocationConstraint': session.region_name}
    try:
        response = s3.create_bucket(**create_bucket_kwargs)
        print(f'Creating Bucket: {create_bucket_kwargs}')
    except ClientError as e:
        # logger.info(e)
        if e.response['Error']['Code'] == 'OperationAborted':
            raise e
    except:
        pass
    print("Adding Bucket Versions")
    response = s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={
            'Status': 'Enabled'
        },
    )
    print(response)
    print("Adding S3 Public Access Block")
    response = s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
    )
    print(response)

    # buckets = []
    # response = s3.list_buckets()
    # for bucket in response['Buckets']:
    #     buckets.append(bucket['Name'])
    # while 'NextToken' in response:
    #     response = s3.list_buckets(NextToken=response['NextToken'])
    #     for bucket in response['Buckets']:
    #         buckets.append(bucket['Name'])



    tags_dict = {'Type': 'terraform-state'}

    tags = [{"Key": k, "Value": v} for k, v in tags_dict.items()]


    print("Adding Bucket Tags")

    response = s3.put_bucket_tagging(
        Bucket=bucket,
        Tagging={
            'TagSet': tags
        },
    )
    print(response)
    sts = session.client('sts')
    account_id = sts.get_caller_identity()['Account']
    default_key = f"arn:aws:kms:{session.region_name}:{account_id}:alias/aws/s3"
    print("Adding Default Encryption to Bucket")
    response = s3.put_bucket_encryption(
        Bucket=bucket,
        # ContentMD5='string',
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256',
                        # 'KMSMasterKeyID': default_key
                    },
                    'BucketKeyEnabled': True
                },
            ]
        },
        # ExpectedBucketOwner='string'
    )
    print(response)
    return


if __name__ == '__main__':
    main()

