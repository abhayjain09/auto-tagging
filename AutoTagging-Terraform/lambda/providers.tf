terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "~> 1.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 2.0"
    }
  }
}
