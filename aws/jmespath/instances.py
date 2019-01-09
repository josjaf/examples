import boto3
import jmespath

session = boto3.session.Session()
ec2 = session.client('ec2')

response = ec2.describe_instances()
instanceIds = jmespath.search("Reservations[].Instances[].InstanceId", response)
print(instanceIds)


# running instance ids
running_instance_ids = jmespath.search("Reservations[].Instances[?State.Name=='running'].InstanceId | []", response)

#
running_instances = jmespath.search("Reservations[].Instances[?State.Name=='running'].InstanceId | []", response)