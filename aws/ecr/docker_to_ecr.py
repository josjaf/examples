import boto3
import docker
from base64 import b64decode
import os

PROJECT = ""

def main():
    session = boto3.session.Session()
    region = session.region_name
    identity = session.client("sts").get_caller_identity()
    account_id = identity["Account"]
    registry = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{PROJECT}"

    # tag image
    docker_client = docker.from_env()
    image = docker_client.images.get(f'{PROJECT}:latest')
    image.tag(registry, 'latest')


    # login
    ecr = session.client('ecr', region_name=session.region_name)
    login_response = ecr.get_authorization_token()
    token = b64decode(login_response['authorizationData'][0]['authorizationToken']).decode()
    username, password = token.split(':', 1)
    print(username, password)
    print(f"UserName: {username}")
    print(f"Password: {password}")
    response = docker_client.login(username=username, password=password, registry=registry, reauth=True, email=None)
    print(response)
    response = docker_client.images.push(registry, tag="latest", auth_config=dict(username=username, password=password))
    print(response)
    return
if __name__ == '__main__':
    main()
