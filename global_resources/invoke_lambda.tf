locals {
  S3-Event-Invoke-TagAutomation_zip = "../outputs/lambda_function.zip"
  lambda_zip_location = "../outputs/AWS-Autotagging.zip"
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
  timeout       = 600
  memory_size   = 128
  description = "Function to invoke lambda for all regions to apply Tag, once any changes found in S3 bucket."
  source_code_hash = "${filebase64sha256(local.lambda_zip_location)}"
  runtime = "python3.8"
  tags = {
    "CreatedBy" = "Terraform-Pipeline"
  }
  provider = "aws.us-east-1"
}

