terraform {
    backend "s3"{
        bucket = "terraform-abhay-backend"
        key = "terraform.tfstate"
        region = "ap-south-1"

    }
}