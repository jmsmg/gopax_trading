# Copyright 2020-present Streami Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import base64
import hashlib
import hmac
import json
import time

import requests

import api_key


APIKEY = api_key.KEY
SECRET = api_key.SECRET
API_URL = 'https://api.gopax.co.kr'


def place(base_asset, quote_asset, amount, side):
    timestamp = str(int(time.time() * 1000))
    method = 'POST'
    request_path = '/orders'
    request_body = {
        'amount': amount,
        'side': side,
        'tradingPairName': '%s-%s' % (base_asset, quote_asset),
        'type': 'market'
    }

    # generate signature
    what = 't' + timestamp + method + request_path + json.dumps(
        request_body)
    decoded_secret = base64.b64decode(SECRET)
    signature = hmac.new(
        decoded_secret, str(what).encode('utf-8'), hashlib.sha512)
    signature_b64 = base64.b64encode(signature.digest())
    custom_headers = {
        'API-Key': APIKEY,
        'Signature': signature_b64,
        'Timestamp': timestamp
    }

    req = requests.post(url=API_URL + request_path,
                        headers=custom_headers, json=request_body)
    result = []
    print(req.text)
    if req.ok:
        result = json.loads(req.text)
    return result


def get(order_id):
    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    request_path = '/orders/%d' % order_id

    # generate signature
    what = 't' + timestamp + method + request_path
    key = base64.b64decode(SECRET)
    signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
    signature_b64 = base64.b64encode(signature.digest())
    custom_headers = {
        'API-Key': APIKEY,
        'Signature': signature_b64,
        'Timestamp': timestamp
    }

    req = requests.get(url=API_URL + request_path, headers=custom_headers)
    result = []
    if req.ok:
        result = json.loads(req.text)
    return result


def get_trades():
    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    request_path = '/trades'

    what = 't' + timestamp + method + request_path
    key = base64.b64decode(SECRET)
    signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
    signature_b64 = base64.b64encode(signature.digest())
    custom_headers = {
        'API-Key': APIKEY,
        'Signature': signature_b64,
        'Timestamp': timestamp
    }

    req = requests.get(url=API_URL + request_path, headers=custom_headers)
    result = []
    if req.ok:
        result = json.loads(req.text)
    return result


def get_trades_by_order_id(order_id):
    return [x for x in get_trades() if x['orderId'] == order_id]
