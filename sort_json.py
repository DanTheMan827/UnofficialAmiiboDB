#!/usr/bin/env python3
# coding=utf-8

import datetime
import json
import os
import os.path
import re

def sortKeys(file):
    # read the database
    with open(file, encoding='utf-8-sig') as myfile:
        data = myfile.read()

    # parse database
    database = json.loads(data)

    with open(file, 'w', encoding='utf-8-sig') as file:
        json.dump(database, file, sort_keys=True, indent='\t')

sortKeys('database/amiibo.json')
sortKeys('database/games_info.json')
