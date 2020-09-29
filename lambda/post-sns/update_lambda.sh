#!/bin/bash

set -eu

rm -f function.zip
zip -r9 function.zip lambda_function.py

result=$(aws lambda update-function-code --function-name "post-sns" --zip-file fileb://function.zip --publish)
echo "LastUpdateStatus: $(echo $result | jq -r '.LastUpdateStatus')"
