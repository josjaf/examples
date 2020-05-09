import boto3
import sys
iam = boto3.client('iam')

response = iam.list_roles()

roleNames = sys.argv[1].split(",")

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
        response = iam.detach_role_policy(
            RoleName=role,
            PolicyArn=policy['PolicyArn']
        )
        print(response)
for role in roleNames:
    print(f"Deleting Role: {role}")
    response = iam.delete_role(RoleName=role)
    print(response)
    #print("Role: {} Policies: {}".format(role,response['AttachedPolicies']))
