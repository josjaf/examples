def aws_tags_to_dict(resource):
    return dict((tag["Key"], tag["Value"]) for tag in resource)


upstream_tags = [{'Key': 'Application',
                  'Value': 'examples'},
                 {'Key': 'Name', 'Value': 'example.com'},
                 {'Key': 'Type', 'Value': 'DevOps'},
                 {'Key': 'aws:', 'Value': 'stack1'}]

expanded = aws_tags_to_dict(upstream_tags)

# downstream filter
tags_from_api = {k: v for k, v in expanded.items() if not k.startswith('aws:')}

print(f"Flat: {tags_from_api}")
print(f"Expanded: {upstream_tags}")
