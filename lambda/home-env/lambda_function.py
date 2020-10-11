#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	lambda_function
# CreatedDate:  2020-07-02 19:57:06 +0900
# LastModified: 2020-10-11 09:23:22 +0900
#


import json
import boto3
import requests
import os
from datetime import datetime
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('inkbird')
    d = sorted(table.scan()['Items'], key=lambda x: x['Date'], reverse=True)[0]

    try:
        logger.info(event['dead'])
        if is_dead(d):
            payload = {
                'attachments': [{
                    'color': '#D3D3D3',
                    'pretext': 'Inkbird mini is dead',
                    'text': f'Last updated: {d["Date"]}'
                }]
            }

            post_slack(payload)
    except KeyError as e:
        logger.info(e)
        payload = {
            'attachments': [{
                'color': '#D3D3D3',
                'pretext': f'Date: {d["Date"]}',
                'text': f'Temperature: {d["Temperature"]}℃\nHumidity: {d["Humidity"]}%'
            }]
        }
        post_slack(payload)

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


def post_slack(payload):
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)


def is_dead(d):
    logger.info(f"Now : {datetime.now()}")
    logger.info(f"Last: {datetime.strptime(d['Date'], '%Y-%m-%d %H:%M')}")
    diff = abs(datetime.now() - datetime.strptime(d["Date"], '%Y-%m-%d %H:%M'))  # UTC
    logger.info(diff.seconds)
    return (diff.seconds - 60 * 60 * 9 > 60 * 30)
