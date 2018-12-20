import boto3
import jmespath


ec2 = boto3.client('ec2')
response = ec2.describe_instances()

# instead of nested looping
instances = jmespath.search("Reservations[].Instances[]", response)

for instance in instances:
    # List Comprehension
    blank_tags = [tag for tag in instance['Tags'] if tag['Value'] == '']
    if blank_tags:
        print(f"Instance {instance['InstanceId']} has a Blank Tag Value: {blank_tags}")



    # JMESPath
    blank_tags = jmespath.search("Tags[?Value==''].{Key: Key, Value: Value}", instance)
    if blank_tags:
        print(f"Instance {instance['InstanceId']} has a Blank Tag Value: {blank_tags}")