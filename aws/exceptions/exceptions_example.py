import boto3
from botocore.exceptions import ClientError


def main():
    s3 = boto3.client('s3')
    bucket = f"test"
    try:
        response = s3.create_bucket(
            Bucket=bucket
        )
    except ClientError as e:
        # error code example
        if e.response['Error']['Code'] == 'BucketAlreadyExists':
            print("Exception: FAIL - Bucket already Exists")
            raise e
        # error message example
        if 'The requested bucket name is not available.' in e.response['Error']['Message']:
            print("Exception: Requested Bucket Name is not available")
            raise e
    except Exception as e:
        print(e)
        raise e
    return


if __name__ == '__main__':
    main()
