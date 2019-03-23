import csv
import os
import threading
import uuid

import boto3
import botocore


def get_child_session(account_id, role_name, session=None):
    """
    get session, with error handling, allows for passing in an sts client. This allows Account A > B > C where A cannot assume a role directly to C
    :param account_id:
    :param role_name:
    :param session=None:
    :return:
    """
    # “/“ + name if not name.startswith(“/“) else name
    try:
        # allow for a to b to c if given sts client.
        if session == None:
            session = boto3.session.Session()

        client = session.client('sts')

        response = client.get_caller_identity()
        # remove the first slash
        role_name = role_name[1:] if role_name.startswith("/") else role_name
        # never have a slash in front of the role name
        role_arn = 'arn:aws:iam::' + account_id + ':role/' + role_name
        print("Creating new session with role: {} from {}".format(role_arn, response['Arn']))

        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=str(uuid.uuid1())
        )
        credentials = response['Credentials']
        session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return session
    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == 'AccessDenied':
            print(e)
            # raise Exception(e)

        elif 'Not authorized to perform sts:AssumeRole' in str(e):
            print(e)
            # raise Exception(f"ERROR:Not authorized to perform sts:AssumeRole on {role_arn}")
        else:
            print(e)
            # raise Exception(e)

    finally:
        pass


def get_org_accounts(session):
    """
    return a list of all accounts in the organization
    :param session:
    :return:
    """
    org_client = session.client('organizations')
    account_ids = []
    response = org_client.list_accounts()
    for account in response['Accounts']:
        account_ids.append(account['Id'])
    while 'NextToken' in response:
        response = org_client.list_accounts(NextToken=response['NextToken'])
        for account in response['Accounts']:
            account_ids.append(account['Id'])
    return account_ids


def worker(account, session):
    """
    function to run inside threads, new session required for each thread. caught errors when only using 1 argument
    :param account:
    :param session:
    :return:
    """
    vpc = None
    session = boto3.session.Session()
    try:
        print(f"Processing Account: {account}")

        role_name = os.environ.get('RoleName', 'OrganizationAccountAccessRole')
        child_session = get_child_session(account_id=account, role_name=role_name, session=session)
        ec2 = child_session.client('ec2')
        region_list = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

        for region in region_list:
            ec2 = child_session.client('ec2', region_name=region)
            vpcs = []
            response = ec2.describe_vpcs()
            for vpc in response['Vpcs']:
                vpcs.append(vpc)
            while 'NextToken' in response:
                response = ec2.describe_vpcs(NextToken=response['NextToken'])
                for vpc in response['Vpcs']:
                    vpcs.append(vpc)
            for vpc in vpcs:

                if vpc['IsDefault'] == True: continue

                # if vpc['OwnerId'] != account: continue
                vpc_dict = {'AccountId': account, 'VpcId': vpc['VpcId'], 'CIDR': vpc['CidrBlock'], 'Region': region}
                print(vpc_dict)
                final_result.append(vpc_dict)
    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == 'OptInRequired':
            print(e)
            pass
    except Exception as e:
        raise e


def get_headers(results):
    """
    getting keys from downstream result so that custom logic added after won't required updating in multiple places
    :param results:
    :return:
    """

    headers = []
    for d in results:
        for key in d.keys():
            headers.append(key)
    headers = list(set(headers))
    return headers


def write_csv(results):
    """
    write to csv
    :param results:
    :return:
    """
    headers = get_headers(results)
    output_ec2 = 'output.csv'
    with open(output_ec2, 'w') as csvfile:
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')

        writer.writeheader()
        for result in results:
            row = result
            writer.writerow(row)


def main():
    global final_result
    threads = []
    final_result = []
    session = boto3.session.Session()
    org_accounts = get_org_accounts(session)
    for account in org_accounts:
        t = threading.Thread(target=worker, args=(account, None))
        threads.append(t)
        t.start()
    # wait for threads to finish
    for thread in threads:
        thread.join()

    print(len(final_result))
    write_csv(final_result)
    return


if __name__ == '__main__':
    main()
