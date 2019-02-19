import boto3
org_client = boto3.client('organizations')
account_ids = []
response = org_client.list_accounts()
for account in response['Accounts']:
    account_ids.append(account['Id'])
while 'NextToken' in response:
    response = org_client.list_accounts(NextToken=response['NextToken'])
    for account in response['Accounts']:
        account_ids.append(account['Id'])
print(account_ids)
