#!/bin/bash
yum install -y jq curl
export instance_id=$(curl http://169.254.169.254/latest/meta-data/instance-id)
export region=$(curl --silent http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region)
export AWS_DEFAULT_REGION=$region
response=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$instance_id")
export instance_name=$(echo $response | jq -r '.Tags[] | select(.Key=="Name") | .Value')

export asg_name=$(echo $response | jq -r '.Tags[] | select(.Key=="aws:autoscaling:groupName") | .Value')

# namespace with jq
export namespace=$(echo $response | jq -r '.Tags[] | select(.Key=="namespace") | .Value')

# namespace without jq
export namespace=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$instance_id" "Name=key,Values=namespace" --query 'Tags[0].Value' --output text)

### install cloudwatch agent
wget https://s3.${region}.amazonaws.com/amazoncloudwatch-agent-${region}/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm
rm -rf amazon-cloudwatch-agent.rpm