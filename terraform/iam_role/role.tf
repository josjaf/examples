data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
resource "aws_iam_role" "lambda_role" {
  name = "example-organizations-lambda"
  max_session_duration = 43200
  description = "example Lambda Role"
  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    },
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
    EOF
    tags = {
      Deployment = "Terraform"
  }
}
resource "aws_iam_role_policy" "example_lambda_policy" {
  name = "example_organizations_lambda_permissions"
  role = "${aws_iam_role.lambda_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:GetLogEvents",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource":"arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}


