#!/bin/bash
bucket=josjaf-examples
region=us-east-1
aws s3 mb s3://$bucket --region $region
aws s3api put-bucket-versioning --bucket $bucket --versioning-configuration Status=Enabled --region $region
aws s3api put-public-access-block \
--region $region \
--bucket $bucket \
--public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"