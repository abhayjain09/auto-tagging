provider "aws" {
  region = var.AWS_REGION
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}