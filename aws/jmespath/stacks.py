import boto3
import jmespath
from helpers import text

text_helpers = text.helpers()

session = boto3.Session()
cloudformation = session.client('cloudformation')

response = cloudformation.list_stacks()
ids = jmespath.search("StackSummaries[].StackId", response)
stacks = jmespath.search("StackSummaries[].StackName", response)


text_helpers.print_separator("String Example")
for stack in stacks:
    print(stack)


text_helpers.print_separator("Dictionary Example")

stacks = jmespath.search("StackSummaries[*].{ID: StackId, StackName: StackName}", response)

for stack in stacks:
    print(stack)