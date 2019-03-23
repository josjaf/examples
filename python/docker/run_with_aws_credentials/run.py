import docker
import boto3


def get_credentials():
    credentials = {}
    available_profiles = boto3.session.Session().available_profiles

    if 'example' in available_profiles:
        print("using example profile")
        session = boto3.session.Session(profile='example')
    else:
        session = boto3.session.Session()

    credentials['AWS_ACCESS_KEY_ID'] = session.get_credentials().access_key
    credentials['AWS_SECRET_ACCESS_KEY'] = session.get_credentials().secret_key
    credentials['AWS_SESSION_TOKEN'] = session.get_credentials().token
    credentials['AWS_DEFAULT_REGION'] = session.region_name
    return credentials


def run_docker(docker_client, env, credentials):
    
    try:
        container = docker_client.containers.get(container_id='example')
        container.remove()
    except docker.errors.NotFound:
        pass
    except Exception as e:
        print(e)
        raise e


    container_name = f"example"
    print(f"Creating Docker Container {container_name}")
    #mounts = {os.getcwd(): {'bind': '/trident', 'mode': 'rw'}}

    environment_variables = {**env, **credentials}
    print(f"env: {environment_variables}")
    docker_client.containers.run("example", detach=True,
                          environment=environment_variables,
                          name=container_name,
                          log_config={"type": "json-file",
                                      "config": {"max-size": "1m"}}

                          )
    print(f"docker logs -f {container_name}")

    return


docker_client = docker.from_env()
credentials = get_credentials()
env = {'repo': 'examples'}
response = run_docker(docker_client, env, credentials)
