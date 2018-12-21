tags_from_api = [{'Key': 'Application',
                  'Value': 'examples'},
                 {'Key': 'Name', 'Value': 'example.com'},
                 {'Key': 'Type', 'Value': 'DevOps'}]


def dict_to_tags(tags_dict):
    tags = [{"Key": k, "Value": v} for k, v in tags_dict.items()]
    return tags


def aws_tags_to_dict(resource):
    return dict((tag["Key"], tag["Value"]) for tag in resource)



flat = aws_tags_to_dict(tags_from_api)
print(f"Flat: {flat}")
expanded = dict_to_tags(flat)
print(f"Expanded: {expanded}")