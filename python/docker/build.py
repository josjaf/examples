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
    buildtime = t.strftime("%m-%d-%Y %H:%M:%S")
    labels = {'Maintainer': 'josjaf', 'commit': sha, 'buildtime': buildtime}
    response = docker_client.images.build(path='.', tag='example:latest', labels=labels, dockerfile='Dockerfile')
    container_build_time = datetime.datetime.now() - t
    print(f"Rebuilding the container took: {container_build_time}")
    print("$ docker run example")
    return


if __name__ == '__main__':
    main()
