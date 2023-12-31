#!/usr/bin/env python3
# coding=utf-8

import datetime
import json
import os
import os.path
import re

# read the database
with open('database/amiibo.json', encoding='utf-8-sig') as myfile:
	data = myfile.read()

# parse database
database = json.loads(data)

# compile the regex
amiibo_series_regex = re.compile('^0x[0-9a-f]{2}')
amiibo_regex = re.compile('^0x[0-9a-f]{16}$')
character_regex = re.compile('^0x[0-9a-f]{4}')
game_series_regex = re.compile('^0x[0-9a-f]{3}')
types_regex = re.compile('^0x[0-9a-f]{2}')
game_id_regex = re.compile('^[0-9A-F]{16}')
date_regex = re.compile('^\d{4}-\d{2}-\d{2}')

# set success exit code
exit_code = 0

used_amiibo_series = []
used_amiibo_character = []
used_amiibo_game_series = []
used_amiibo_types = []
warnings = []
errors = []

def printWarning(text):
	global warnings
	warnings.append('\033[1;33;40m' + text + '\x1b[0m')
	return

def printError(code, text):
	global errors
	global exit_code
	exit_code = code
	errors.append('\033[1;31;40m' + text + '\x1b[0m')
	return

def validateDate(date_text):
	try:
		datetime.datetime.strptime(date_text, '%Y-%m-%d')
		return True
	except ValueError:
		return False

# check amiibos keys
for key in database['amiibos']:
	if bool(amiibo_regex.match(key)):
		amiibo = database['amiibos'][key]
		character = '0x' + key[2:6]
		game_series = '0x' + key[2:5]
		amiibo_series = '0x' + key[14:16]
		type = '0x' + key[8:10]

		if character not in used_amiibo_character:
			used_amiibo_character.append(character)

		if game_series not in used_amiibo_game_series:
			used_amiibo_game_series.append(game_series)

		if amiibo_series not in used_amiibo_series:
			used_amiibo_series.append(amiibo_series)

		if type not in used_amiibo_types:
			used_amiibo_types.append(type)

		# check if name is set
		if 'name' not in amiibo:
			printError(1, 'Name not set for: ' + key)
		else:
			if amiibo['name'] == None:
				printError(1, 'Name not set for: ' + key)

		# check if mapped_id is set
		if 'mapped_id' in amiibo:
			if amiibo['mapped_id'] is not None:
				if key[:10] != amiibo['mapped_id'][:10]:
					printWarning('mapped_id character mismatch for: ' + key)

		# check if release is set
		if 'release' in amiibo:
			release = amiibo['release']

			if 'au' in release:
				if release['au'] is not None:
					if validateDate(release['au']) == False:
						printError(1, 'Formatting error on AU release for: ' + key)
				else:
					printWarning('AU release is null for: ' + key)

			else:
				printError(1, 'AU release not set for: ' + key)

			if 'eu' in release:
				if release['eu'] is not None:
					if validateDate(release['eu']) == False:
						printError(1, 'Formatting error on EU release for: ' + key)
				else:
					printWarning('EU release is null for: ' + key)

			else:
				printError(1, 'EU release not set for: ' + key)

			if 'jp' in release:
				if release['jp'] is not None:
					if validateDate(release['jp']) == False:
						printError(1, 'Formatting error on JP release for: ' + key)
				else:
					printWarning('\033[1;33;40mJP release is null for: ' + key)

			else:
				printError(1, 'JP release not set for: ' + key)

			if 'na' in release:
				if release['na'] is not None:
					if validateDate(release['na']) == False:
						printError(1, 'Formatting error on NA release for: ' + key)
				else:
					printWarning('NA release is null for: ' + key)

			else:
				printError(1, 'NA release not set for: ' + key)
		else:
			printError(1, 'Release not set for: ' + key)

		# check if corresponding amiibo_series key exists
		if amiibo_series not in database['amiibo_series']:
			printError(1, 'Unknown amiibo series: ' + amiibo_series)

		# check if corresponding characters key exists
		if character not in database['characters']:
			printError(1, 'Unknown character: ' + character)

		# check if corresponding game_series key exists
		if game_series not in database['game_series']:
			printError(1, 'Unknown game series: ' + game_series)

		# check if corresponding types key exists
		if type not in database['types']:
			printError(1, 'Unknown type: ' + type)

		# check if corresponding icon file exists
		if not os.path.isfile('images/icon_' + key[2:10] + '-' + key[10:18] + '.png'):
			printError(1, 'Missing icon for: ' + key)

	else:
		printError(1, 'Formatting error on amiibo key: ' + key)

# check amiibo_series keys
for key in database['amiibo_series']:
	if bool(amiibo_series_regex.match(key)) == False:
		printError(1, 'Formatting error on amiibo series key: ' + key)
	else:
		if key not in used_amiibo_series:
			printError(1, 'Extraneous amiibo series: ' + key)

# check characters keys
for key in database['characters']:
	if bool(character_regex.match(key)) == False:
		printError(1, 'Formatting error on amiibo character key: ' + key)
	else:
		if key not in used_amiibo_character:
			printError(1, 'Extraneous amiibo character: ' + key)


# check game_series keys
for key in database['game_series']:
	if bool(game_series_regex.match(key)) == False:
		printError(1, 'Formatting error on amiibo game series key: ' + key)
	else:
		if key not in used_amiibo_game_series:
			printError(1, 'Extraneous amiibo game series: ' + key)

# check types keys
for key in database['types']:
	if bool(types_regex.match(key)) == False:
		printError(1, 'Formatting error on amiibo type key: ' + key)
	else:
		if key not in used_amiibo_types:
			printError(1, 'Extraneous amiibo type: ' + key)

warnings = list(set(warnings))
warnings.sort()

for warning in warnings:
	print(warning, flush=True)

errors = list(set(errors))
errors.sort()

for error in errors:
	print(error, flush=True)

os._exit(exit_code)
