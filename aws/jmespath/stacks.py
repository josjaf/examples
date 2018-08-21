import boto3
import jmespath

session = boto3.Session()
cloudformation = session.client('cloudformation')

response = cloudformation.list_stacks()
ids = jmespath.search("StackSummaries[].StackId", response)
stacks = jmespath.search("StackSummaries[].StackName", response)

for stack in stacks:
    print(stack)


stacks = jmespath.search("StackSummaries[*].{ID: StackId, StackName: StackName}", response)

for stack in stacks:
    print(stack)