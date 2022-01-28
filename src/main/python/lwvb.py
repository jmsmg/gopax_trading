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


def compute_range(candles):
    return sum([(x[2] - x[1]) / float(x[4]) for x in candles]) / float(len(candles))


def lwvb_entry(candles, k=1.0):
    recent = int(-1 * len(candles) / 4)
    return compute_range(candles[recent:]) > compute_range(candles) * k


def lwvb_take_profit(p, p_open, r_open, k=10.0):
    if p > int(p_open * (1.0 + k * r_open + 0.004)) and p > p_open * 1.005:
        return 1
    return 0


def lwvb_stop_loss(p, p_open, r_open, k=25.0):
    if p < int(p_open * (1.0 - k * r_open)):
        return -1
    return 0
