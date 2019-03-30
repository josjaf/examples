import boto3


def get_org_accounts(session):
    """
    return a list of all accounts in the organization, removes the org master since it does not have an org master role by default
    :param session:
    :return:
    """
    org_master_account_id = session.client('sts').get_caller_identity()['Account']
    org_client = session.client('organizations')
    account_ids = []
    response = org_client.list_accounts()
    for account in response['Accounts']:
        account_ids.append(account['Id'])
    while 'NextToken' in response:
        response = org_client.list_accounts(NextToken=response['NextToken'])
        for account in response['Accounts']:
            account_ids.append(account['Id'])
    account_ids.remove(org_master_account_id)
    return account_ids


session = boto3.session.Session()
account_ids = get_org_accounts(session)
print(account_ids)