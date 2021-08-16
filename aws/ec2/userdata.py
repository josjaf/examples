import io
import pathlib
import subprocess
import time
import zipfile

import boto3
import requests


def aws_tags_to_dict(resource, dict_key_key="Key", dict_key_value="Value"):
    """
    convert a list of dicts to a flattened dict
    :param resource:
    :param dict_key_key:
    :param dict_key_value:
    :return:
    """
    return dict((tag[dict_key_key], tag[dict_key_value]) for tag in resource)


def main():
    token = requests.put("http://169.254.169.254/latest/api/token",
                         headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}).text
    headers = {"X-aws-ec2-metadata-token": token}
    instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id', headers=headers).text
    instance_region = \
        requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', headers=headers).json()[
            'region']

    region = instance_region
    session = boto3.session.Session(region_name=region)
    ec2 = session.client('ec2')
    tag_response = ec2.describe_tags(

        Filters=[
            {
                'Name': 'resource-id',
                'Values': [
                    instance_id,
                ]
            },
        ],

    )
    namespace = [i for i in tag_response['Tags'] if i['Key'] == 'namespace'][0]['Value']
    asg_group_name = [i for i in tag_response['Tags'] if i['Key'] == 'aws:autoscaling:groupName'][0]['Value']
    InitialLifeCycleHook = [i for i in tag_response['Tags'] if i['Key'] == 'InitialLifeCycleHook'][0]['Value']
    return


if __name__ == '__main__':
    main()

