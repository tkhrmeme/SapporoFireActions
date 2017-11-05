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

url_saigai = 'http://www.119.city.sapporo.jp/saigai/sghp.html'
url_geocode = "http://geocode.csis.u-tokyo.ac.jp/cgi-bin/simple_geocode.cgi"

import urllib.request
import xml.etree.ElementTree as ET

def geocodingForAddress(addressStr):
	'''
	CSISシンプルジオコーディング実験利用
		http://newspat.csis.u-tokyo.ac.jp/geocode/modules/geocode/index.php
		
	series=[ADDRESS, STATION, PLACE, FACILITY]
	constraint=''
	'''

	reqStr = "札幌市" + addressStr
	url_addr = urllib.parse.quote(reqStr)
	url_param = "?addr={addr}&charset=UTF8&geosys=world&series=ADDRESS".format(addr=url_addr)
	url = url_geocode + url_param

	result = None
	try:
		req = urllib.request.Request(url)
		res = urllib.request.urlopen(req)

		result = res.read().decode('utf-8')
	except urllib.error.URLError as e:
		sys.stderr.write(e)
	except urllib.error.HTTPError as e:
		sys.stderr.write(e)

	return result

def getCandidateLocation(rootXML):
	loc = None
	candidate = rootXML.find('candidate')
	if candidate is not None:
		lon = candidate.find('longitude')
		lat = candidate.find('latitude')
		loc = (float(lon.text), float(lat.text))
	return loc

def getSoupFromURL(url):
	soup = None
	try:
		req = urllib.request.urlopen(url)
		soup = BeautifulSoup(req.read(), "lxml")
	except IOError as e:
		sys.stderr.write(e)
	except urllib.error.HTTPError as e:
		sys.stderr.write(e)
	return soup

soup = getSoupFromURL(url_saigai)

if soup is None:
	sys.stderr.write("Cannot get a soup.")
	sys.exit()

sys.stdout.write("Load a soup from {}\n".format(url_saigai))

# コンテンツ部分のdiv要素を取り出す
div = soup.find('div', id="tmp_contents")

# 過去の出動情報のテーブル
table = div.find('table')

# テーブルの行リスト
tr_list = table.find_all('tr')

# 2行目のセルのリスト
td_list = tr_list[1].find_all('td')

action_info = {}
action_name = None
adress_list = None

td = td_list[1] # 昨日のセル

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

# 昨日の日付
dt = datetime.today()
ayer = dt + timedelta(hours=-24)

action_info['date'] = datetime.strftime(ayer, "%Y%m%d")

# カレントワーキングディレクトリ
dir_path = os.getcwd()

# JSONのファイル名
filename = '{yy}{mm:02d}{dd:02d}.json'.format(yy=ayer.year, mm=ayer.month, dd=ayer.day)

path = os.path.join(dir_path, filename)

if not os.path.exists(path):
	# 新規ファイル保存
	with open(path, 'w') as fp:
		json.dump(action_info, fp, ensure_ascii=False, indent=None)
		sys.stdout.write("Save {}\n".format(filename))
else:
	sys.stdout.write("File already exists {}\n".format(filename))
