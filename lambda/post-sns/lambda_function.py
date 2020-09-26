#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	lambda_function
# CreatedDate:  2020-07-02 19:57:06 +0900
# LastModified: 2020-08-01 11:34:16 +0900
#


import boto3
import os


def lambda_handler(event, context):
    sns = boto3.resource('sns')

    sns.Topic(os.environ['TOPIC_ARN']).publish(
                Message='post sns',
                Subject='from lambda'
            )

    return "Posted sns"
