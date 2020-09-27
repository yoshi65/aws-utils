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

result=$(aws lambda update-function-code --function-name "home-env" --zip-file fileb://function.zip --publish)
echo "LastUpdateStatus: $(echo $result | jq -r '.LastUpdateStatus')"
