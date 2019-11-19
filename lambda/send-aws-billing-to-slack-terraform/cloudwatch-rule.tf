resource "aws_cloudwatch_event_rule" "send-aws-billing-to-slack-rule" {
  name                = "send-aws-billing-to-slack-rule"
  description         = "send-aws-billing-to-slack-rule"
  schedule_expression = "cron(0 3 * * ? *)"
}

resource "aws_cloudwatch_event_target" "send-aws-billing-to-slack-event-target" {
  rule      = "${aws_cloudwatch_event_rule.send-aws-billing-to-slack-rule.name}"
  target_id = "send-aws-billing-to-slack"
  arn       = "${aws_lambda_function.send-aws-billing-to-slack.arn}"
}

resource "aws_lambda_permission" "allow-cloudwatch-to-call-send-aws-billing-to-slack" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.send-aws-billing-to-slack.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.send-aws-billing-to-slack-rule.arn}"
}
