



resource "aws_sns_topic" "alarm_topic" {
  name = "alarm_topic"
}


resource "aws_cloudwatch_metric_alarm" "foobar" {
  alarm_name                = "BillingAlarm-Terraform"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "EstimatedCharges"
  namespace                 = "AWS/Billing"
  period                    = "${6*60*60}"
  statistic                 = "Maximum"
  threshold                 = "10"
  alarm_description         = "BillingAlarm"
  #insufficient_data_actions = []
  treat_missing_data        = "missing"
  dimensions = {
    Currency = "USD"
  }
  alarm_actions     = ["${aws_sns_topic.alarm_topic.arn}"]
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = "${aws_sns_topic.alarm_topic.arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.alarm_lambda.arn}"
}
resource "aws_lambda_permission" "with_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.alarm_lambda.arn}"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alarm_topic.arn}"
}
resource "null_resource" "alarm_sub" {
  provisioner "local-exec" {
    command = "python subscribe.py"
    environment {
      EMAIL = "${var.email}"
      TOPIC_ARN = "${aws_sns_topic.alarm_topic.arn}"
      BAZ = "true"
    }
  }
}