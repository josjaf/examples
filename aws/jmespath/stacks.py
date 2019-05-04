import boto3
import jmespath
from helpers import text

text_helpers = text.helpers()

session = boto3.Session()
cloudformation = session.client('cloudformation')

response = cloudformation.list_stacks()

paginator = cloudformation.get_paginator('list_stacks')
response_iterator = paginator.paginate()
response = {}
response['StackSummaries'] = []
for page in response_iterator:
    for s in page['StackSummaries']:
        response['StackSummaries'].append(s)
#### get paginated data

ids = jmespath.search("StackSummaries[].StackId", response)
stacks = jmespath.search("StackSummaries[].StackName", response)


text_helpers.print_separator("String Example")
for stack in stacks:
    print(stack)


text_helpers.print_separator("Dictionary Example")

running_instance_ids = jmespath.search("Reservations[].Instances[?State.Name=='running'].InstanceId | []", response)

stacks = jmespath.search("StackSummaries[*].{ID: StackId, StackName: StackName}", response)
stacks = jmespath.search("StackSummaries[?StackStatus=='CREATE_COMPLETE' "
                         "|| StackStatus=='UPDATE_COMPLETE']"
                         ".{ID: StackId, StackName: StackName, StackStatus: StackStatus}", response)

for stack in stacks:
    print(stack)