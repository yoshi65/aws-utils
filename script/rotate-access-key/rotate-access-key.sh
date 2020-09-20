#!/bin/zsh
#
# FileName: 	rotate-access-key
# CreatedDate:  2020-08-27 12:50:19 +0900
# LastModified: 2020-08-27 13:00:18 +0900
#

current_access_key=$(aws configure get aws_access_key_id)
username=$(aws iam get-user | jq -r '.User.UserName')
new_key=$(aws iam create-access-key --user-name $username)
aws configure set aws_access_key_id $(jq -r '.AccessKey.AccessKeyId' <<< $new_key)
aws configure set aws_secret_access_key $(jq -r '.AccessKey.SecretAccessKey' <<< $new_key)
aws iam delete-access-key --access-key-id $current_access_key
