"""
Run this from the org master account, assuming that it is the default profile, will loop through the org and make a credentials file for the entire org with the account numbers as the profile name using a built in assume role
"""
import configparser
import os
from pathlib import Path

import boto3


def main():
    session = boto3.session.Session()
    org_client = session.client('organizations')
    sts = session.client('sts')
    org_master_account_id = sts.get_caller_identity()['Account']
    response = org_client.list_accounts()
    org_accounts = [a['Id'] for a in response['Accounts']]
    org_accounts.remove(org_master_account_id)
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
    print("vim ~/.aws/credentials1")
    return


if __name__ == '__main__':
    main()
