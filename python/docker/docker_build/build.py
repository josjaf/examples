import datetime

import docker
import git


def main():
    docker_client = docker.from_env()

    t = datetime.datetime.now()
    print("Rebuilding the Container")
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    # TODO add exception processing for requests.exceptions.ConnectionError when docker dameon is not running
    #buildtime = t.strftime("%m-%d-%Y %H:%M:%S")
    # commenting out the docker_build time, because it will always generate a new image, but not take up more disks apce
    labels = {'Maintainer': 'josjaf'}
    response = docker_client.images.build(path='.', tag='example:latest', labels=labels, dockerfile='Dockerfile')
    container_build_time = datetime.datetime.now() - t
    print(f"Rebuilding the container took: {container_build_time}")
    print("$ docker run example")
    return


if __name__ == '__main__':
    main()
