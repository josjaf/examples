import boto3
import jmespath

session = boto3.Session()
cfn = session.client('cloudformation')

response = cfn.list_stacks()
stack_status = ['CREATE_COMPLETE', 'UPDATE_COMPLETE']
stacks = [stack for stack in response['StackSummaries'] if stack['StackStatus'] in stack_status]

for stack in stacks:
    print(stack['StackName'])




paginator = cfn.get_paginator('list_stacks')
response_iterator = paginator.paginate(StackStatusFilter=[
    'CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_IN_PROGRESS', 'DELETE_FAILED',  'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE', 'REVIEW_IN_PROGRESS',
])
# removing delete complete
#'DELETE_COMPLETE',
response = {}
response['StackSummaries'] = []
for page in response_iterator:
    for s in page['StackSummaries']:
        response['StackSummaries'].append(s)

good_stack_status = ['UPDATE_COMPLETE', 'CREATE_COMPLETE']

stack_list = [stack['StackName'] for stack in response['StackSummaries'] if stack['StackStatus'] in good_stack_status]