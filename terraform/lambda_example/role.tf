resource "aws_iam_role" "lambda_role" {
  name                 = "example-lambda"
  max_session_duration = 3600
  description          = "example Lambda Role"
  assume_role_policy   = <<EOF
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
    }
  ]
}
    
EOF

}

resource "aws_iam_role_policy" "example_lambda_policy" {
  name = "example_lambda_permissions"
  role = aws_iam_role.lambda_role.id

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
    },
    {
      "Action": [
        "lambda:InvokeFunction"
      ],
      "Effect": "Allow",
      "Resource": "${aws_lambda_function.moo_organizations_lambda.arn}"
    }
  ]
}
EOF

}

