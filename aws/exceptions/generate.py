import boto3
exceptions = (dir(boto3.client('s3').exceptions))

for e in exceptions:
	if not e.startswith('_'):
		print(e)