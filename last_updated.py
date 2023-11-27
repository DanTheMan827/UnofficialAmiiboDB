#!/usr/bin/env python
# coding=utf-8

# MIT License
#
# Copyright (c) 2017 Nevin Vu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import hashlib
import json


class LastUpdated():
    def __init__(self, file='last-updated.json'):
        self.file = file

    def read(self):
        with open(self.file, 'r') as f:
            data = json.load(f)

        return {
            'amiibo_sha1': data['amiibo_sha1'],
            'game_info_sha1': data['game_info_sha1'],
            'timestamp': datetime.datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f'),
        }

    def read_timestamp(self):
        return self.read()['timestamp']

    def write(self, amiibo_sha1, game_info_sha1, timestamp):
        with open(self.file, 'w') as f:
            json.dump({
                'amiibo_sha1': amiibo_sha1,
                'game_info_sha1': game_info_sha1,
                'timestamp': timestamp.isoformat(),
            }, f, sort_keys=True)

    def hash(self, data):
        return hashlib.sha1(data).hexdigest()

    def update(self, data, data1):
        amiibo_sha1 = self.hash(data)
        game_info_sha1 = self.hash(data1)
        try:
            last_update = self.read()
        except Exception as e:
            print(e)
            last_update = None

        updated = False
        if last_update is None or last_update['amiibo_sha1'] != amiibo_sha1 or last_update['game_info_sha1'] != game_info_sha1:
            last_update = {
                'amiibo_sha1': amiibo_sha1,
                'game_info_sha1': game_info_sha1,
                'timestamp': datetime.datetime.utcnow(),
            }
            self.write(**last_update)
            updated = True

        return last_update, updated


if __name__ == '__main__':
    last_updater = LastUpdated()
    with open('database/amiibo.json', 'rb') as f:
        with open('database/games_info.json', 'rb') as g:
            last_update, updated = last_updater.update(f.read(), g.read())

    if updated:
        print('Updated: {}'.format(last_updater.file))

    print('amiibo_sha1: {}'.format(last_update['amiibo_sha1']))
    print('game_info_sha1: {}'.format(last_update['game_info_sha1']))
    print('timestamp: {}'.format(last_update['timestamp'].isoformat()))
