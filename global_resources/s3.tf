data "aws_caller_identity" "current" {}


resource "aws_s3_bucket" "b" {
  bucket = "autotag-bucket-${data.aws_caller_identity.current.account_id}"
  acl    = "private"

  tags = {
    "Name" = "mybucket-c29df1-abhay",
    "Company" = "Abhay"
  }
  provider = "aws.us-east-1"
  
}
resource "aws_s3_bucket_object" "Global-tag" {
    bucket = "${aws_s3_bucket.b.id}"
    acl    = "private"
    key    = "Global-tag/"
    provider = "aws.us-east-1"
    #source = "/dev/null"
}

resource "aws_s3_bucket_object" "App-tag" {
    bucket = "${aws_s3_bucket.b.id}"
    acl    = "private"
    key    = "App-tag/"
    provider = "aws.us-east-1"
    #source = "/dev/null"
}
resource "aws_s3_bucket_object" "object" {
  bucket = aws_s3_bucket.b.id
  key    = "Global-tag/global.json"
  acl    = "private"  # or can be "public-read"
  source = "../outputs/global.json"
  provider = "aws.us-east-1"
  etag = filemd5("../outputs/global.json")   #tag is given to find if the file has been changed from its last upload using md5 sum.
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.S3-Event-Invoke-TagAutomation.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.b.arn
  provider = "aws.us-east-1"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.b.id
  
  lambda_function {
    lambda_function_arn = aws_lambda_function.S3-Event-Invoke-TagAutomation.arn
    events              = ["s3:ObjectCreated:*"]
    
    #filter_prefix       = "/"
    #filter_suffix       = ".log"
  }
  provider = "aws.us-east-1"
  depends_on = [aws_lambda_permission.allow_bucket]
}