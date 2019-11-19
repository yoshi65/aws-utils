variable "slack_url" {
  type        = "string"
  description = "Slack URL"
}

variable "kms_arn" {
  type        = "string"
  description = "Kms ARN"
}

variable "region" {
  default     = "ap-northeast-1"
  description = "Aws region"
}

variable "bucket" {
  default     = "<bucket-for-terraform>"
  description = "Bucket to put lambda function"
}
