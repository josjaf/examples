import boto3

session = boto3.session.Session()
iam = session.client('iam')

response = iam.list_roles()
role_names = [r['RoleName'] for r in response['Roles']]
role_arns = [r['Arn'] for r in response['Roles']]
role_ids = [r['RoleId'] for r in response['Roles']]
admin_role_dict = [r for r in response['Roles'] if r['RoleName'] == 'Administrator']