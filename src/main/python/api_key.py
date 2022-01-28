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


# Your API key and secret
# DO NOT EXPOSE THESE VALUES TO OTHERS AT ALL TIMES!
# NEVER UPLOAD THEM TO GITHUB, etc.!
KEY = 'TO_BE_FILLED'
SECRET = 'TO_BE_FILLED'


def main():
    import base64
    import hashlib
    import hmac
    import requests
    import time

    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    api_url = 'https://api.gopax.co.kr'
    request_path = '/balances'

    what = 't' + timestamp + method + request_path
    key = base64.b64decode(SECRET)
    signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
    signature_b64 = base64.b64encode(signature.digest())
    custom_headers = {
        'API-Key': KEY,
        'Signature': signature_b64,
        'Timestamp': timestamp
    }

    req = requests.get(url=api_url+request_path, headers=custom_headers)
    if req.ok:
        print('OK')
    else:
        print('Incorrect API key; please check')


if __name__ == '__main__':
    main()
