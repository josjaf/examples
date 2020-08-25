import boto3
import argparse
import sys
import jmespath
import argparse
import botocore


def delete_repo(session, repo_name, by_force):
    ecr = session.client('ecr')
    try:
        delete_response = ecr.delete_repository(repositoryName=repo_name, force=by_force)
    except Exception:
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=str, help="Repository to be deleted")
    parser.add_argument("-f", "--force", action="store_true", help="Delete repository by force")
    parser.add_argument("-p", "--profile", type=str, help="AWS profile used to execute command")
    args = parser.parse_args()
    session = boto3.session.Session()
    by_force = False
    repository = args.repository
    if args.profile:
        session = boto3.session.Session(profile_name=args.profile)
    if args.force:
        by_force = True
    by_force = True # always doing by force
    try:
        delete_repo(session, args.repository, by_force)
        print("Deleting Repository: {}...".format(repository))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'RepositoryNotFoundException':
            print("Repository: {} does not exist in your account".format(repository))
        else:
            print(e)
            raise e


if __name__ == '__main__':
    main()
