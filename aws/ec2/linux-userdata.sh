#!/bin/bash
yum install -y jq curl
export instance_id=$(curl http://169.254.169.254/latest/meta-data/instance-id)
export region=$(curl --silent http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region)
export AWS_DEFAULT_REGION=$region
response=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$instance_id")
export instance_name=$(echo $response | jq -r '.Tags[] | select(.Key=="Name") | .Value')

export asg_name=$(echo $response | jq -r '.Tags[] | select(.Key=="aws:autoscaling:groupName") | .Value')
export namespace=$(echo $response | jq -r '.Tags[] | select(.Key=="namespace") | .Value')
