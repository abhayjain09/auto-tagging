resource "aws_cloudwatch_event_rule" "Cloudwatch-event" {
  name        = "Resources-Tag-Automation"
  description = "Event of Resources-Tag-Automation that Runs every day 1:00 AM UTC."
  schedule_expression = "cron(0 1 * * ? *)"
  provider = "aws.us-east-1"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.Cloudwatch-event.name
  #target_id = "SendToSNS"
  arn       = aws_lambda_function.S3-Event-Invoke-TagAutomation.arn
  provider = "aws.us-east-1"
}
