import boto3


def main():
    session = boto3.session.Session()
    s3 = session.client('s3')
    bucket = 'josjaf-test'
    create_bucket_kwargs = dict(Bucket=bucket)
    if session.region_name != 'us-east-1':
        print("Adding Location Constraint to Payload")
        create_bucket_kwargs['CreateBucketConfiguration'] = {'LocationConstraint': session.region_name}
    try:
        response = s3.create_bucket(**create_bucket_kwargs)
    except: pass
    response = s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={
            'Status': 'Enabled'
        },
    )
    print(response)
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
    return


if __name__ == '__main__':
    main()
