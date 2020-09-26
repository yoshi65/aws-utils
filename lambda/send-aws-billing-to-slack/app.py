#!/usr/bin/env python
# encoding: utf-8
"""Send aws billing to Slack.

AWSの利用料金をSlackに通知する。

Attributes:
    SLACK_WEBHOOK_URL (str): Key Management Serviceを用いて暗号化された
        環境変数SLACK_WEBHOOK_URLを復号したURL

"""

import json
import os
from base64 import b64decode
from datetime import date, datetime

import boto3
import requests


def lambda_handler(event, context):
    """Lambda handler.

    Args:
        event: イベントデータ
        context: ランタイム情報

    Returns:
        dict: レスポンス

    """
    client = boto3.client('ce', region_name='us-east-1')

    total_billing = get_total_billing(client)
    service_billings = get_service_billings(client)

    (title, detail) = get_message(total_billing, service_billings)

    post_slack(title, detail)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "successfully sent to slack",
        }),
    }


def get_total_billing(client):
    """Get total billing.

    AWS利用料金の合計を取得する

    Args:
        client (CostExplorer.client): AWS Cost Explorer Serviceのクライアント

    Returns:
        dict: {'start': 始まりの日付,
               'end': 終わりの日付,
               'billing': AWS利用料金の合計}

    """
    response = get_response_of_cost_and_usage(client)
    return {
        'start':
        response['ResultsByTime'][0]['TimePeriod']['Start'],
        'end':
        response['ResultsByTime'][0]['TimePeriod']['End'],
        'billing':
        response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'],
    }


def get_service_billings(client):
    """Get service billing.

    AWS利用料金をサービスごとに合計を取得する

    Args:
        client (CostExplorer.client): AWS Cost Explorer Serviceのクライアント

    Returns:
        :obj:`list` of :obj:`dict`: サービス名と利用料金のdict
            降順で利用料金をソートしている

    """
    response = get_response_of_cost_and_usage(client, Total=False)

    return sorted(
        [
            {
                'service_name': item['Keys'][0],
                'billing': float(item['Metrics']['AmortizedCost']['Amount'])
            }
            for item
            in response['ResultsByTime'][0]['Groups']
        ],
        key=lambda k: k['billing'],
        reverse=True
    )


def get_message(total_billing, service_billings):
    """Get message.

    Args:
        total_billing: get_total_billingの戻り値
        service_billings: get_service_billingsの戻り値

    Returns:
        :obj:`str`, :obj:`str`: AWS利用料金の合計, サービスごとの利用料金の合計

    """
    start = datetime.strptime(total_billing['start'],
                              '%Y-%m-%d').strftime('%m/%d')
    end = datetime.strptime(total_billing['end'], '%Y-%m-%d').strftime('%m/%d')
    total = round(float(total_billing['billing']), 2)

    title = f'{start}～{end} total: {total:.2f} USD'

    filtered_billings = [
        item for item in service_billings if item['billing'] > 0.01
    ]
    rows = [
        '- %s: %.2f USD' % (item['service_name'], float(item['billing']))
        for item in filtered_billings
    ]
    return title, '\n'.join(rows)


def post_slack(title, detail):
    """Post slack.

    SLACK_WEBHOOK_URLで表されるSlackのチャンネルに
    AWS利用料金の合計とサービスごとの合計を通知する

    Args:
        title: get_messageの戻り値[0]
        detail: get_messageの戻り値[1]

    """
    SLACK_WEBHOOK_URL = get_slack_webhook_url()
    payload = {
        'username': 'AWS Cost',
        'icon_emoji': ':aws_cost',
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


def get_response_of_cost_and_usage(client, Total=True):
    """Get response of cost and usage.

    月初から今日までのAWS利用料金を取得する

    Args:
        client (CostExplorer.client): AWS Cost Explorer Serviceのクライアント
        Total (bool): Trueなら、AWS利用料金の合計
            Falseなら、AWS利用料金のサービスごとの合計

    Returns:
        dict: get_cost_and_usageの戻り値

    """
    if Total:
        return client.get_cost_and_usage(
            TimePeriod={
                'Start': get_begin_of_month(),
                'End': get_today()
            },
            Granularity='MONTHLY',
            Metrics=['AmortizedCost']
        )
    else:
        return client.get_cost_and_usage(
            TimePeriod={
                'Start': get_begin_of_month(),
                'End': get_today()
            },
            Granularity='MONTHLY',
            Metrics=['AmortizedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )


def get_begin_of_month():
    """Get begin of month.

    月初の日付を返す

    Returns:
        str: 月初の日付

    """
    today = date.today()
    return date(today.year, today.month, 1).isoformat()


def get_today():
    """Get begin of month.

    今日の日付を返す

    Returns:
        str: 今日の日付

    """
    return date.today().isoformat()


def get_slack_webhook_url():
    """Get slack webhook url.

    SLACK_WEBHOOK_URLを取得し、kmsにより復号して返す

    Returns:
        str: SLACK_WEBHOOK_URL

    """
    SLACK_WEBHOOK_URL = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(os.environ['SLACK_WEBHOOK_URL']))['Plaintext']
    return SLACK_WEBHOOK_URL
