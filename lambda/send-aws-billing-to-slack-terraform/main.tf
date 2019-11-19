provider "aws" {
  region = "${var.region}"
}

terraform {
  required_version = ">= 0.12.13"

  backend "s3" {
    bucket                  = "<bucket-for-terraform>"
    key                     = "lambda/send-aws-billing-to-slack-terraform/terraform-lambda.tfstate"
    region                  = "ap-northeast-1"
    shared_credentials_file = "~/.aws/credentials"
    profile                 = "default"
  }
}
