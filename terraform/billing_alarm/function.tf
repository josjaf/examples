resource "aws_lambda_function" "alarm_lambda" {
  filename = "${data.archive_file.foo.output_path}"
  function_name = "alarm_lambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "index.lambda_handler"
  source_code_hash = "${data.archive_file.foo.output_base64sha256}"
  runtime = "python3.6"
  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }
}