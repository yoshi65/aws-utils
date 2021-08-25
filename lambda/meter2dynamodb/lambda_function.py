#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	lambda_function
# CreatedDate:  2021-04-27 20:41:27 +0900
# LastModified: 2021-08-25 10:14:25 +0900
#


import boto3
import json
import logging
from os import getenv
import requests
from datetime import datetime, timezone, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    table_name = getenv('table_name')
    logger.info(f"table_name: {table_name}")

    access_token = getenv('access_token')
    logger.info("Access token is gotten")

    header = {"Authorization": access_token}

    response = requests.get(
        "https://api.switch-bot.com/v1.0/devices",
        headers=header
    )
    devices = json.loads(response.text)
    device_ids = get_device_id(devices)

    if len(device_ids) == 1:
        date_now = get_date_now_JST()
        meter_result = get_meter_result(device_ids[0], header)
        logger.info(meter_result)
    else:
        return {"text": "device_id is not identified"}

    resource = boto3.resource('dynamodb')
    table = resource.Table(table_name)

    insert_meter_result(table, meter_result, date_now)
    return {"text": f"Inserted meter_result to {table} at {date_now.strftime('%Y-%m-%d %H:%M')}"}


def insert_meter_result(table, meter_result: dict, date_now) -> None:
    table.put_item(
        Item={
            'Id': int(date_now.timestamp()),
            'Date': date_now.strftime('%Y-%m-%d %H:%M'),
            'Temperature': meter_result["temperature"],
            'Humidity': meter_result["humidity"],
        }
    )


def get_date_now_JST():
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST)


def get_device_id(devices: dict) -> list:
    return [device['deviceId'] for device in devices['body']['deviceList'] if 'Meter' in device['deviceType']]


def get_meter_result(device_id: str, header: str) -> dict:
    url = f"https://api.switch-bot.com/v1.0/devices/{device_id}/status"
    response = requests.get(url, headers=header)

    return json.loads(response.text)["body"]
