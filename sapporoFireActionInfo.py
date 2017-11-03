#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import json

import urllib.request

from bs4 import BeautifulSoup
from bs4 import element

from datetime import datetime
from datetime import timedelta

url = 'http://www.119.city.sapporo.jp/saigai/sghp.html'

def getSoupFromURL(url):
	soup = None
	try:
		req = urllib.request.urlopen(url)
		soup = BeautifulSoup(req.read(), "lxml")
	except IOError as e:
		print(e)
	except urllib.error.HTTPError as e:
		print(e)
	return soup

soup = getSoupFromURL(url)

if soup is None:
	sys.stdout.write("Cannot get a soup.")
	sys.exit()

sys.stdout.write("Load a soup from {}\n".format(url))

div = soup.find('div', id="tmp_contents")

table = div.find('table')

tr_list = table.find_all('tr')

td_list = tr_list[1].find_all('td')

action_info = {}
action_name = None
adress_list = None

td = td_list[1] # 昨日
for data in td.contents:
	if type(data) == element.NavigableString:
		s = data.string.strip()
		if len(s) > 0:
			if s[0] == '●':
				if action_name is not None:
					action_info[action_name] = adress_list
				adress_list = []
				action_name = s[1:]
			elif s[0] == '・':
				u = s[1:]
				p = u.find('（')
				adrs = u[:p]
				tthm = u[p+1:-1]
				adress_list.append((adrs, tthm))

if action_name is not None:
	action_info[action_name] = adress_list

dt = datetime.today()
ayer = dt + timedelta(hours=-24)

action_info['date'] = datetime.strftime(ayer, "%Y%m%d")

dir_path = os.getcwd()

filename = '{yy}{mm:02d}{dd:02d}.json'.format(yy=ayer.year, mm=ayer.month, dd=ayer.day)

path = os.path.join(dir_path, filename)

if not os.path.exists(path):
	with open(path, 'w') as fp:
		json.dump(action_info, fp, ensure_ascii=False, indent=None)
		sys.stdout.write("Save {}\n".format(filename))
else:
	sys.stdout.write("File already exists {}\n".format(filename))
