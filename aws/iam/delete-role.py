import boto3
iam = boto3.client('iam')

response = iam.list_roles()

roleNames = ['SJ-Test2']

for role in roleNames:
    response = iam.list_role_policies(
        RoleName=role
    )
    print("Role: {} Policies: {}".format(role,response['PolicyNames']))
    for policy in response['PolicyNames']:
        response = iam.delete_role_policy(
            RoleName=role,
            PolicyName=policy
        )


for role in roleNames:
    response = iam.list_attached_role_policies(
        RoleName=role
    )

    for policy in response['AttachedPolicies']:
        if policy['PolicyName'] == 'RoleQuarantinePolicy':
            response = iam.detach_role_policy(
                RoleName=role,
                PolicyArn=policy['PolicyArn']
            )
            print(response)
for role in roleNames:
    response = iam.delete_role(RoleName=role)
    print(response)
    #print("Role: {} Policies: {}".format(role,response['AttachedPolicies']))
