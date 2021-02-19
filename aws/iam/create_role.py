import boto3
import json
import time

# This is the account id where terraform is running
ORGMASTER_ACCOUNT_ID = ""


def main():
    path = '/'
    role_name = 'OrganizationAccountAccessRole'
    description = 'Org Master Role'

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{ORGMASTER_ACCOUNT_ID}:root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    tags = [
        {
            'Key': 'Environment',
            'Value': 'Production'
        }
    ]
    iam = boto3.client('iam')
    try:
        response = iam.create_role(
            Path=path,
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=description,
            MaxSessionDuration=3600,
            Tags=tags
        )
        print(response)
        print(f"Created Role: {response['Role']['Arn']}")
    except Exception as e:
        print(e)
        pass
    try:
        ## TODO Lock this down
        time.sleep(5)
        response = iam.attach_role_policy(
            RoleName=role_name, PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")
        print("Attaching Policy")
        print(response)
    except Exception as e:
        print(e)
    return

if __name__ == '__main__':
    main()

