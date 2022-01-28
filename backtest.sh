#!/bin/bash
echo 'Stopping trading bot'
sudo supervisorctl stop trading_bot_example
echo 'Trading bot stopped'
python3 src/main/python/backtest.py
