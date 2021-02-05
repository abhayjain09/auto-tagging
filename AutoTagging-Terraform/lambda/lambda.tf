data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.root}/.artifacts/aws/lambda/${var.name}.zip"
}

resource "random_pet" "lambda" {
  keepers = {
    hash = data.archive_file.lambda.output_base64sha256
  }
  length = 2
}

resource "aws_s3_bucket_object" "lambda" {
  bucket = var.bucket
  key    = "lambda/${var.name}-${random_pet.lambda.id}.zip"
  source = data.archive_file.lambda.output_path
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = 14
  tags              = local.tags
}

resource "aws_lambda_function" "lambda" {
  function_name                  = var.name
  role                           = module.role.arn
  runtime                        = var.runtime
  handler                        = var.handler
  layers                         = var.layers
  timeout                        = var.timeout
  memory_size                    = var.memory_size
  reserved_concurrent_executions = var.reserved_concurrent_executions

  tracing_config {
    mode = var.enable_active_tracing ? "Active" : "PassThrough"
  }

  dynamic "environment" {
    for_each = local.has_env
    content {
      variables = var.env
    }
  }

  dynamic "vpc_config" {
    for_each = local.has_vpc_name
    content {
      subnet_ids = data.aws_subnet_ids.private[0].ids
      security_group_ids = concat(
        [data.aws_security_group.egress[0].id],
        var.egress_security_groups
      )
    }
  }

  s3_bucket = var.bucket
  s3_key    = aws_s3_bucket_object.lambda.id
  tags      = local.tags
}

data "aws_iam_policy_document" "invoke" {
  statement {
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [
      aws_lambda_function.lambda.arn
    ]
  }
}

