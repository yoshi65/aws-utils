#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import os

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    (title, detail) = generate_message(event)
    logger.info(f"title: {title}")
    logger.info(f"detail: {detail}")

    post_slack(title, detail)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "successfully sent to slack",
        }),
    }


def generate_message(event):
    records = event['Records']
    logger.info(f"{records}")
    detail = records[0]['Sns']['Message']
    return 'Lambda failure alert', detail


def post_slack(title, detail):
    SLACK_WEBHOOK_URL = get_slack_webhook_url()
    payload = {
        'attachments': [{
            'color': '#D3D3D3',
            'pretext': title,
            'text': detail
        }]
    }

    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)


def get_slack_webhook_url():
    return os.environ['SLACK_WEBHOOK_URL']
