resource "aws_lambda_function" "moo_organizations_lambda" {
  //  depends_on = [archive_file.foo ]

  filename         = data.archive_file.moo.output_path
  function_name    = "moo_organizations_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.lambda_handler"
  source_code_hash = filebase64sha256(data.archive_file.moo.output_path)
  runtime          = "python3.6"
}

resource "aws_lambda_function" "foo_organizations_lambda" {
  filename         = data.archive_file.foo.output_path
  function_name    = "foo_organizations_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.lambda_handler"
  source_code_hash = filebase64sha256(data.archive_file.foo.output_path)
  runtime          = "python3.6"
  environment {
    variables = {
      moo_function_name = aws_lambda_function.moo_organizations_lambda.function_name
    }
  }
}

