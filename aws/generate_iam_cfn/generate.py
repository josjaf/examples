import boto3
import re

ec2 = boto3.client('ec2')
api_calls = dir(ec2)

def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

for line in api_calls:
    if line.startswith("_"): continue
    if line.startswith("waiter"): continue
    formatted_api_call = snake_to_camel(line)
    final = "- ec2:{}".format(formatted_api_call)     
    print(final)
