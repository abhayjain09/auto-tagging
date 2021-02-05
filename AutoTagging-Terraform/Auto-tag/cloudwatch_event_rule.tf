resource "aws_cloudwatch_event_rule" "Cloudwatch-event" {
  name        = "Resources-Tag-Automation"
  description = "Event of Resources-Tag-Automation that Runs every midnight 1:00 AM Local time zone."
  schedule_expression = "cron(0 1 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.Cloudwatch-event.name
  #target_id = "SendToSNS"
  arn       = aws_lambda_function.Resources-Tag-Automation.arn
}
