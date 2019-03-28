"""
Run this from the org master account, assuming that it is the default profile, will loop through the org and make a credentials file for the entire org with the account numbers as the profile name using a built in assume role
"""
import os
import configparser
import boto3
from pathlib import Path
from helpers import helpers






def main():
    Helpers = helpers.Helpers()
    session = boto3.session.Session()
    org_accounts = Helpers.get_org_accounts(session)
    profiles = []
    config = configparser.ConfigParser()
    for account in org_accounts:
        config[account] = {}
        profile_config = config[account]
        print(account)
        profile_config['role_arn'] = f"arn:aws:iam::{account}:role/OrganizationAccountAccessRole"
        profile_config['region'] = session.region_name
        profile_config['source_profile'] = 'default'

    home = (Path.home())
    try:
        access_rights = 0o755
        os.mkdir(home.joinpath('.aws'), access_rights)
    except FileExistsError as e:
        pass
    except Exception as e:
        print(e)
        raise e
    full_path = home.joinpath('.aws/credentials1')
    with open(full_path, 'w') as configfile:
        config.write(configfile)
    return


if __name__ == '__main__':
    main()
