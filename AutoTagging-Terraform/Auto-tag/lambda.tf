locals {
  lambda_zip_location = "outputs/AWS-Autotagging.zip"
  S3-Event-Invoke-TagAutomation_zip = "outputs/lambda_function.zip"
}

data "archive_file" "Resources-Tag-Automation" {
  type        = "zip"
  source_dir = "AWS-Autotagging"
  output_path = "${local.lambda_zip_location}"
  #source_dir  = var.source_dir
  #output_path = "${path.root}/.artifacts/aws/lambda/${var.name}.zip"
}

resource "aws_lambda_function" "Resources-Tag-Automation" {
  filename      =  "${local.lambda_zip_location}"
  function_name = "Resources-Tag-Automation"
  role          = aws_iam_role.Auto-Tag-All-Resources.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 900
  memory_size   = 2048
  description = "Automation to Tag all Resources in same region with Global and company specific tags."
  source_code_hash = "${filebase64sha256(local.lambda_zip_location)}"
  runtime = "python3.8"
  tags = {
    "CreatedBy" = "Terraform-Pipeline"
  }
}

data "archive_file" "S3-Event-Invoke-TagAutomation" {
  type        = "zip"
  source_dir = "S3-Event-Invoke-TagAutomation"
  output_path = "${local.S3-Event-Invoke-TagAutomation_zip}"
  #source_dir  = var.source_dir
  #output_path = "${path.root}/.artifacts/aws/lambda/${var.name}.zip"
}

resource "aws_lambda_function" "S3-Event-Invoke-TagAutomation" {
  filename      =  "${local.S3-Event-Invoke-TagAutomation_zip}"
  function_name = "S3-Event-Invoke-TagAutomation"
  role          = aws_iam_role.Lambda-invoke-role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 300
  memory_size   = 128
  description = "Function to invoke lambda for all regions to apply Tag, once any changes found in S3 bucket."
  source_code_hash = "${filebase64sha256(local.lambda_zip_location)}"
  runtime = "python3.8"
  tags = {
    "CreatedBy" = "Terraform-Pipeline"
  }
}



/*
# Data Source: aws_lambda_invocation

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation

data "aws_lambda_invocation" "example" {
  function_name = aws_lambda_function.Resources-Tag-Automation.function_name

  input = <<JSON
{
  "key1": "value1",
  "key2": "value2"
}
JSON
}

output "result_entry" {
  value = jsondecode(data.aws_lambda_invocation.example.result)
}


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
*/
