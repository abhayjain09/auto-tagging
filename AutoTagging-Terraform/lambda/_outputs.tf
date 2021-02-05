output "name" {
  value = aws_lambda_function.lambda.function_name
}

output "arn" {
  value = aws_lambda_function.lambda.arn
}

output "role" {
  value       = module.role
  description = "The details for the Lambda role."
}

output "invoke_policy" {
  value = {
    document = data.aws_iam_policy_document.invoke.json
  }
}

output "dead_letter_queue_arn" {
  value = module.dead-letter-queue.arn
}
