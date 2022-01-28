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


import logging
import time

import crawl
import lwvb
import orders
import position as p
import sns


# modify the below variables to customize the bot
BASE_ASSET_TICKER = 'BTC'
QUOTE_ASSET_TICKER = 'KRW'
INITIAL_QUOTE_ASSET_AMOUNT = 100000
ENTRY_COEFFICIENT = 1
TAKE_PROFIT_COEFFICIENT = 10.0
STOP_LOSS_COEFFICIENT = 50.0
INTERVAL = 5 # number of minutes per candle; allowed values are 1/5/30/1440


def update_position(position, get_trades_result, bid=False):
    base_asset, quote_asset = BASE_ASSET_TICKER.upper(), QUOTE_ASSET_TICKER.upper()
    if bid:
        base_asset_amount = sum(x['baseAmount'] - x['fee'] for x in get_trades_result)
        price = float(position['quote_asset_amount']) / base_asset_amount
        candles = crawl.candles(base_asset, quote_asset, interval=INTERVAL)
        r_open = lwvb.compute_range(candles)
        p.update(base_asset, base_asset_amount, r_open, price)
        sns.notify_position_update(base_asset_amount, base_asset)
    else:
        quote_asset_amount = sum(x['quoteAmount'] - x['fee'] for x in get_trades_result)
        p.clear(base_asset, quote_asset_amount)
        sns.notify_position_update(quote_asset_amount, QUOTE_ASSET_TICKER.upper())


def recover(position):
    order_id = int(position['order_id'])
    get_trades_result = orders.get_trades_by_order_id(order_id)
    if get_trades_result:
        update_position(position, get_trades_result, position['taken'])


def main():
    if INTERVAL not in [1, 5, 30, 1440]:
        logging.error('interval value is not valid; accepted values are 1, 5, 30, 1440')
        return

    base_asset, quote_asset = BASE_ASSET_TICKER.upper(), QUOTE_ASSET_TICKER.upper()
    position = p.get(INITIAL_QUOTE_ASSET_AMOUNT)
    # Clear position if position.base_asset != BASE_ASSET_TICKER
    if position['taken'] and position['base_asset'] != BASE_ASSET_TICKER:
        position.clear(base_asset, INITIAL_QUOTE_ASSET_AMOUNT)
        return
    candles = crawl.candles(base_asset, quote_asset, interval=INTERVAL)

    # If there was an error, recover
    if 'order_id' in position:
        recover(position)
        return

    # Consider clearing the current position
    if position['taken']:
        current_p = crawl.ticker(base_asset, quote_asset)['ask']
        take_profit = lwvb.lwvb_take_profit(
            current_p, position['price'], position['r_open'], TAKE_PROFIT_COEFFICIENT)
        stop_loss = lwvb.lwvb_stop_loss(
            current_p, position['price'], position['r_open'], STOP_LOSS_COEFFICIENT)
        if take_profit or stop_loss:
            place_order_result = orders.place(
                base_asset, quote_asset, position['base_asset_amount'], side='sell')
            if place_order_result:
                order_id = place_order_result['id']
                time.sleep(1)
                get_trades_result = orders.get_trades_by_order_id(order_id)
                if get_trades_result:
                    update_position(position, get_trades_result, bid=False)
                else:
                    p.set_order_id(position, order_id, base_asset, bid=False)
    # Consider taking a position
    else:
        entry = lwvb.lwvb_entry(candles, ENTRY_COEFFICIENT)
        if entry:
            place_order_result = orders.place(
                base_asset, quote_asset, position['quote_asset_amount'], side='buy')
            if place_order_result:
                order_id = place_order_result['id']
                time.sleep(1)
                get_trades_result = orders.get_trades_by_order_id(order_id)
                if get_trades_result:
                    update_position(position, get_trades_result, bid=True)
                else:
                    p.set_order_id(position, order_id, base_asset, bid=True)
    logging.info('trading_bot_example.py exits at %d', time.time())


if __name__ == '__main__':
    main()
