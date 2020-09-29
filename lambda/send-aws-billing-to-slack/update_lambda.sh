#!/bin/bash

set -eu

rm -f function.zip
rm -rf package
mkdir -p package
pip install --target ./package requests
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip app.py

aws lambda update-function-code --function-name "send-aws-billing-to-slack" --zip-file fileb://function.zip --publish
result=$(aws lambda update-function-code --function-name "send-aws-billing-to-slack" --zip-file fileb://function.zip --publish)
echo "LastUpdateStatus: $(echo $result | jq -r '.LastUpdateStatus')"
