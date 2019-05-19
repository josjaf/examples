import boto3
import jmespath
ec2 = boto3.client('ec2')
response = ec2.describe_network_interfaces()

attached_enis = [eni for eni in response['NetworkInterfaces'] if eni['Status'] == 'in-use']

for eni in attached_enis:
    if not eni['TagSet']:
        print(f"ENI:{eni['NetworkInterfaceId']} has no Tags")
        continue

    name_tag = [tag for tag in eni['TagSet'] if tag['Key'] == 'Name']
    if not name_tag:
        print(f"ENI:{eni['NetworkInterfaceId']} has no Name Tag, but has other tags")

# list of dicts with the eni id, tagset list and the value of the name tag
enis = jmespath.search("NetworkInterfaces[].{NetworkInterfaceId: NetworkInterfaceId, Tags: TagSet,  Name: TagSet[?Key=='Name'].Value | [0]}", response)

# list of dicts with the value of the name tag
enis = jmespath.search("NetworkInterfaces[].{Name: TagSet[?Key=='Name'].Value | [0]}", response)

# list of the different tag Key values
enis = jmespath.search("NetworkInterfaces[].TagSet[].Key", response)

#  list of list of dicts where the key is Name
enis = jmespath.search("NetworkInterfaces[].TagSet[?Key=='Name']", response)

# 0 slice of list of list of dicts where the key is Name
enis = jmespath.search("NetworkInterfaces[].TagSet[?Key=='Name'] | [0]", response)

# list of values for the Name key

enis = jmespath.search("NetworkInterfaces[].TagSet[?Key=='Name'].Value | [0]", response)

print(enis)