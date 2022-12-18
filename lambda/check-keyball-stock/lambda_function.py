#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import os

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    confirm_status()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "successfully sent to line",
        }),
    }


def confirm_status():
    logger.info("start confirm_status")

    url = get_url()
    site = requests.get(url)
    data = BeautifulSoup(site.text, "html.parser")
    messages = []
    is_stock = False

    items = data.find_all('li', attrs={'class': 'grid__item'})
    for item in items:
        name = item.find_all('a', attrs={'class': 'full-unstyled-link'})[0].get_text().strip()
        logger.info(f"confirming {name}")
        if name.startswith('Keyball'):
            status = "在庫あり"
            if find := item.find('span', class_="badge badge--bottom-left color-inverse"):
                status = find.get_text()
                is_stock = True

            result = f"{name}: {status}"
            logger.info(result)
            messages.append(result)

    if is_stock:
        logger.info("stock exists")
        send_line_notify('\n' + '\n'.join(messages))


def send_line_notify(notification_message):
    line_notify_token = get_line_notify_token()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers=headers, data=data)


def get_url():
    return os.environ['URL']


def get_line_notify_token():
    return os.environ['LINE_NOTIFY_TOKEN']
