#!/bin/bash

set -eu

rm -f function.zip
rm -rf package
mkdir -p package
pip install --target ./package requests
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py

aws s3 cp function.zip s3://<bucket-for-lambda>/lambda/response-home-env/function.zip
