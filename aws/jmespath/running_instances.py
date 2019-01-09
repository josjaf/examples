import boto3
import jmespath




session = boto3.session.Session()
ec2 = session.client('ec2')

response = ec2.describe_instances()


### PYTHON
# produce flat instance dict
instances = []
for r in response['Reservations']:
    for i in r['Instances']:
        instances.append(i)

running_instances = [i for i in instances if i['State']['Name'] =='running']





# running instance ids
running_instance_ids = jmespath.search("Reservations[].Instances[?State.Name=='running'].InstanceId | []", response)

# running instances dict
running_instances = jmespath.search("Reservations[].Instances[?State.Name=='running'] | []", response)