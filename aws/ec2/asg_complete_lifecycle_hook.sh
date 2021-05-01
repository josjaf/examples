#!/bin/bash
set -e -x
yum update -y
amazon-linux-extras install nginx1 -y
service nginx start
rm -f /usr/share/nginx/html/index.html
curl 169.254.169.254/latest/meta-data/local-ipv4 > /usr/share/nginx/html/index.html
echo >> /usr/share/nginx/html/index.html
curl 169.254.169.254/latest/meta-data/instance-id >> /usr/share/nginx/html/index.html
echo >> /usr/share/nginx/html/index.html
curl 169.254.169.254/latest/meta-data/ami-id >> /usr/share/nginx/html/index.html
echo thisisgreen >> /usr/share/nginx/html/index.html
echo userdata completed >> /home/ec2-user/userdatacomplete.txt


sudo yum install -y jq
INSTANCE_ID=$(curl -s 'http://169.254.169.254/latest/meta-data/instance-id')
INSTANCE_REGION=$(curl -s 'http://169.254.169.254/latest/dynamic/instance-identity/document' | python -c "import sys, json; print json.load(sys.stdin)['region']")
region=$INSTANCE_REGION

export AWS_DEFAULT_REGION=$INSTANCE_REGION
sudo amazon-linux-extras install nginx1.12 -y
sudo systemctl enable nginx
sudo systemctl start nginx
ENVIRONMENT=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=environment" --query 'Tags[0].Value' --output text)



response=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID")
export asg_name=$(echo $response | jq -r '.Tags[] | select(.Key=="aws:autoscaling:groupName") | .Value')

lifecycle_hook="launch"


retVal=0
export RESULT="CONTINUE"
if [ $retVal -ne 0 ]; then
    echo "Chef did not return 0"
    export RESULT="ABANDON"
fi


response=$(aws autoscaling complete-lifecycle-action \
--lifecycle-hook-name ${lifecycle_hook} \
--auto-scaling-group-name ${asg_name} \
--lifecycle-action-result ${RESULT} \
--instance-id $INSTANCE_ID)
echo $response
