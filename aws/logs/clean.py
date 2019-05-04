import boto3


def main():
    client = boto3.client('logs')
    paginator = client.get_paginator('describe_log_groups')
    response_iterator = paginator.paginate(
        #logGroupNamePrefix='/aws/lambda',
    )
    response = {}
    response['logGroups'] = []
    for r in response_iterator:
        #for l in response['logGroups']:
        for log_group in r['logGroups']:
            response['logGroups'].append(log_group)

    for log_group in response['logGroups']:
        if log_group['logGroupName'].startswith('/home'):
            response = client.put_retention_policy(
                logGroupName=log_group['logGroupName'],
                retentionInDays=731
            )
            continue
        if log_group['logGroupName'].startswith(''):
            print(f"Deleting Log Group: {log_group['logGroupName']}")
            # response = client.delete_log_group(
            #     logGroupName=log_group['logGroupName']
            # )
            response = client.put_retention_policy(
                logGroupName=log_group['logGroupName'],
                retentionInDays=14
            )
            print(response)
    return

if __name__ == '__main__':
    main()