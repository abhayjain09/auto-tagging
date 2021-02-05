resource "aws_lambda_function_event_invoke_config" "config" {
  function_name                = aws_lambda_function.lambda.function_name
  maximum_event_age_in_seconds = var.maximum_event_age_in_seconds
  maximum_retry_attempts       = var.maximum_retry_attempts
  destination_config {
    on_failure {
      destination = module.dead-letter-queue.arn
    }
    dynamic "on_success" {
      for_each = local.has_success_destination
      content {
        destination = var.on_success_destination
      }
    }
  }
}
