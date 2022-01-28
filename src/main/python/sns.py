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


import boto3


def send_email(subject, message):
    sns = boto3.client('sns', region_name='ap-northeast-2')
    account_number = boto3.client('sts').get_caller_identity().get('Account')
    topic_arn = 'arn:aws:sns:ap-northeast-2:%s:EmailNotificationSNSTopic' % account_number
    sns.publish(TopicArn=topic_arn, Subject=subject, Message=message)


def notify_position_update(amount, asset):
    send_email('Position updated', 'New balance: %f %s' % (amount, asset))
