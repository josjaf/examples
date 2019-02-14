# Run in the Organizations Account with Local Credentials
provider "aws" {
  region     = "us-east-1"
}
# # bucket cannot be a variable
terraform {
  backend "s3" {
    bucket = "FIXME"
    key    = "terraform/iam_role.tfstate"
    region = "us-east-1"
  }
}




