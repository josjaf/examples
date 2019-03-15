provider "aws" {
  region     = "us-east-1"
}
# # bucket cannot be a variable
# # dynamodb cannot be a variable
terraform {
  backend "s3" {
    bucket = "sample"
    key    = "terraform/billing_alarm/alarm_example.tfstate"
    region = "us-east-1"
    # dynamodb_table = "TerraformLock"
  }
}




