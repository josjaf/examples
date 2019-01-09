import boto3
import jmespath

session = boto3.session.Session()
ec2 = session.client('ec2')

response = ec2.describe_instances()
instanceIds = jmespath.search("Reservations[].Instances[].InstanceId", response)
print(instanceIds)


