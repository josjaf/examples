import boto3
import re

ec2 = boto3.client('ec2')
api_calls = dir(ec2)

def snake_to_camel(word):
    import re
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

for line in api_calls:
    if line.startswith("_"):
        continue
    if line.startswith("waiter"):
        continue
    final = "- ec2:{}".format(line)     
    print(final)
