data "archive_file" "send-aws-billing-to-slack" {
  type        = "zip"
  source_dir  = "lambda-code"
  output_path = "lambda-code/function.zip"
}

resource "aws_lambda_function" "send-aws-billing-to-slack" {
  function_name = "send-aws-billing-to-slack"
  description   = "[util] send aws billing to slack function"
  tags = {
    owner = "yamazaki"
  }

  # The bucket name as created earlier with "aws s3api create-bucket"
  s3_bucket = "${var.bucket}"
  s3_key    = "send-aws-billing-to-slack/function.zip"

  handler = "app.lambda_handler"
  runtime = "python3.6"

  role = "${aws_iam_role.lambda-send-aws-billing-to-slack-role.arn}"

  environment {
    variables = {
      SLACK_WEBHOOK_URL = "${var.slack_url}"
    }
  }
}

resource "aws_iam_role" "lambda-send-aws-billing-to-slack-role" {
  name = "lambda-send-aws-billing-to-slack-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda-send-aws-billing-to-slack-policy" {
  name        = "lambda-send-aws-billing-to-slack-policy"
  description = "lambda send aws billing to slack policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "ce:GetCostAndUsage"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "kms:Decrypt"
      ],
      "Effect": "Allow",
      "Resource": "${var.kms_arn}"
    }

  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda-send-aws-billing-to-slack-poliy-attach" {
  role       = "${aws_iam_role.lambda-send-aws-billing-to-slack-role.name}"
  policy_arn = "${aws_iam_policy.lambda-send-aws-billing-to-slack-policy.arn}"
}
