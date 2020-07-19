#!/bin/bash

set -eu

rm -f function.zip
zip -r9 function.zip lambda_function.py

aws s3 cp function.zip s3://<bucket-for-lambda>/lambda/post_sns/function.zip
