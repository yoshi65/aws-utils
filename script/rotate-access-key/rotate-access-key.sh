#!/bin/bash
#
# FileName: 	rotate-access-key
# CreatedDate:  2020-08-27 12:50:19 +0900
# LastModified: 2022-12-20 09:13:02 +0900
#

set -ex

if [ "$1" = "" ]; then
  PROFILE="default"
else
  PROFILE=$1
fi

current_access_key=$(aws configure get aws_access_key_id --profile ${PROFILE})
username=$(aws iam get-user --profile ${PROFILE} | jq -r '.User.UserName')
echo "Create new access key for user ${username}"
new_key=$(aws iam create-access-key --profile ${PROFILE} --user-name $username)
aws configure set aws_access_key_id $(jq -r '.AccessKey.AccessKeyId' <<< ${new_key}) --profile ${PROFILE}
aws configure set aws_secret_access_key $(jq -r '.AccessKey.SecretAccessKey' <<< ${new_key}) --profile ${PROFILE}
sleep 10 && aws iam delete-access-key --profile ${PROFILE} --access-key-id $current_access_key
