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


import json
import sys

import crawl
import lwvb
import trading_bot_example as tbe


def get_backtest_data(lib, force_update=False):
    filename = '%s_%s_%d.txt' % (lib.BASE_ASSET_TICKER, lib.QUOTE_ASSET_TICKER, lib.INTERVAL)
    init = False
    try:
        if not force_update:
            data = json.loads(open(filename).read())
    except:
        init = True
    finally:
        if force_update or init:
            data = crawl.candles(
                lib.BASE_ASSET_TICKER, lib.QUOTE_ASSET_TICKER, num_candles=1000,
                interval=lib.INTERVAL)
            if data:
                datafile = open(filename, 'w')
                datafile.write(str(data))
                datafile.close()
    return data


def backtest(estimated_cost_rate=0.0004):
    candles = get_backtest_data(tbe)

    trades = 0
    balance = 1.0
    position_taken = False
    price = 0
    r_open = 0

    entry_k = tbe.ENTRY_COEFFICIENT
    profit_k = tbe.TAKE_PROFIT_COEFFICIENT
    stop_loss_k = tbe.STOP_LOSS_COEFFICIENT

    for i in range(len(candles) - 20):
        if position_taken:
            p = candles[i+19][4]
            take_profit = lwvb.lwvb_take_profit(p, price, r_open, k=profit_k)
            stop_loss = lwvb.lwvb_stop_loss(p, price, r_open, k=stop_loss_k)
            if  take_profit or stop_loss:
                balance *= p / float(price) * (1 - estimated_cost_rate)
                position_taken = False
                price = p
                trades += 1
                print('selling at price %d, balance is now %f' % (price, balance))
        else:
            if lwvb.lwvb_entry(candles[i:i+20], entry_k):
                balance *= (1 - estimated_cost_rate)
                position_taken = True
                price = candles[i+19][4]
                r_open = lwvb.compute_range(candles[i:i+20])
                trades += 1
                print('timestamp: %d, price: %d, profit: %d, loss: %d, r_open: %f' % (
                    candles[i+19][0],
                    price, int(price * (1.0 + profit_k * r_open + 0.004)),
                    int(price * (1.0 - stop_loss_k * r_open)), r_open
                    ))
    print('Parameters: entry %f, profit %f, stop_loss %f, interval %d minutes' % (
        entry_k, profit_k, stop_loss_k, tbe.INTERVAL))
    print('From %s-%s %d trades, the estimated profit is %.2f%%' % (
        tbe.BASE_ASSET_TICKER, tbe.QUOTE_ASSET_TICKER, trades, (balance - 1) * 100))


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'update_backtest_data':
            get_backtest_data(tbe, force_update=True)
    else:
        backtest()


if __name__ == '__main__':
    main()
