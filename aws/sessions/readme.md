This is includes code to create AWS Boto3 Python Sessions. Once the Session object is created, the Client can be created from the Session. This uses a custom Session

```
import boto3
AWS_PROFILE = 'default'
AWS_REGION = 'us-east-1'
session = boto3.Session(region_name=AWS_REGION, profile_name=AWS_PROFILE)
iam = session.client('iam')
sts = session.client('sts')
```
This method uses the default session, every client that is not created by the custom session will inherit these properties
```
import boto3
AWS_PROFILE='default'
AWS_REGION='us-east-1'
boto3.setup_default_session(profile_name=AWS_PROFILE,region_name=AWS_REGION)
```