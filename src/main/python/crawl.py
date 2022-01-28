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


import time
import json
import requests


API_URL = 'https://api.gopax.co.kr'


def candles(base_asset, quote_asset, num_candles=20, interval=5):
    end = int(time.time() * 1000)
    start = end - 60 * 1000 * interval * num_candles
    req_path = '/trading-pairs/%s-%s/candles?start=%d&end=%d&interval=%d' % (
        base_asset, quote_asset, start, end, interval)

    result, req = [], requests.get(url=API_URL+req_path)
    if req.ok:
        result = json.loads(req.text)
    return result


def ticker(base_asset, quote_asset):
    req_path = '/trading-pairs/%s-%s/ticker' % (base_asset, quote_asset)
    result, req = [], requests.get(url=API_URL+req_path)
    if req.ok:
        result = json.loads(req.text)
    return result
