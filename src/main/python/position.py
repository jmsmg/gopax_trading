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


import ast
import logging


def write(position_dict):
    filename = 'trading_bot_example.position'
    position_file = open(filename, 'w')
    position_file.write(str(position_dict))
    position_file.close()


def get(initial_quote_asset_amount):
    filename = 'trading_bot_example.position'
    position = {
        'taken': False, 'base_asset_amount': 0,
        'quote_asset_amount': initial_quote_asset_amount
    }
    try:
        position = ast.literal_eval(open(filename).read())
    except:
        logging.info('Position file does not exist; first run')
    return position


def set_order_id(position_dict, order_id, base_asset, bid=False):
    position_dict['order_id'] = order_id
    position_dict['taken'] = bid
    position_dict['base_asset'] = base_asset
    write(position_dict)
    return position_dict


def update(base_asset, base_asset_amount, r_open, price):
    position_dict = {
        'taken': True,
        'quote_asset_amount': 0,
        'base_asset': base_asset,
        'base_asset_amount': base_asset_amount,
        'r_open': r_open,
        'price': price
    }
    write(position_dict)


def clear(base_asset, quote_asset_amount):
    position_dict = {
        'taken': False,
        'quote_asset_amount': quote_asset_amount,
        'base_asset': base_asset,
        'base_asset_amount': 0
    }
    write(position_dict)
