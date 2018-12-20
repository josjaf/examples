import boto3
import jmespath

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
instanceIds = jmespath.search("Reservations[].Instances[].{InstanceId: InstanceId, Name: Tags[?Key=='Name'].Value | [0]}", response)
for instance in instanceIds:
    print(instance)
