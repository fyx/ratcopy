#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import pyperclip
import requests
import json

import config
api_version = 'v1'
headers = { 'authorization': 'ApiKey ' + config.rattic_user + ':' + config.rattic_key, 'accept': 'application/json' }

def rattic_global_completer(prefix, **kwargs):
  if len(prefix) > 1:
    data = rattic_item_search(prefix)
    list = [ ]
    for item in data['objects']:
      if item['title'].startswith(prefix):
        list.append(item['title'])
      return list

def rattic_item_search(filter):
  reply = requests.get('https://' + config.rattic_server + '/api/' + api_version + '/cred/?title__contains=' + filter, headers=headers)
  reply.raise_for_status()
  return json.loads(reply.content)

def rattic_item_get(filter):
  reply = requests.get('https://' + config.rattic_server + '/api/' + api_version + '/cred/?title__exact=' + filter, headers=headers)
  reply.raise_for_status()
  data = json.loads(reply.content) 
  if data['objects']: 
    id = str(data['objects'][0]['id'])
    reply = requests.get('https://' + config.rattic_server + '/api/' + api_version + '/cred/' + id + '/', headers=headers)
    reply.raise_for_status()
    data = json.loads(reply.content)
    return data['password']
 
parser = argparse.ArgumentParser()
parser.add_argument("item", nargs=1).completer = rattic_global_completer
argcomplete.autocomplete(parser)
args = parser.parse_args()

item = rattic_item_get(args.item[0])
if item:
  pyperclip.copy(item)
  print 'Password for ' + args.item[0] + ' is now in your clipboard'
else:
  print 'Password not found :('
