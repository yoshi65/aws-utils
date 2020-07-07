#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	lambda_function
# CreatedDate:  2020-07-02 19:57:06 +0900
# LastModified: 2020-07-07 09:07:00 +0900
#


import json
import boto3
import requests
import os


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('inkbird')
    d = sorted(table.scan()['Items'], key=lambda x:x['Date'], reverse=True)[0]
    post_slack(d)

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
    
    
def post_slack(d):
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
    payload = {
        'attachments': [{
            'color': '#D3D3D3',
            'pretext': f'Date: {d["Date"]}',
            'text'   : f'Temperature: {d["Temperature"]}℃\nHumidity: {d["Humidity"]}%'
        }]
    }

    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
