# -*- coding: utf-8 -*-
import re
import requests
import datetime
from decimal import *
from time import time
from calendar import timegm

#Access token will not work forever
ACCESS_TOKEN = '' 

FREQUENCY = 2 #In hours

def get_groups(): #Finds the FB groups a user is in  
	token = ACCESS_TOKEN
	payload = {'access_token': token, 'fields': 'name,id' }
	url = 'https://graph.facebook.com/v2.3/me/groups'
	r = requests.get(url, params=payload)
	if r.status_code == 200:
		data = r.json()['data']
		groups = []
		for group in data:
			info = (group['name'],group['id'])
			groups.append(info)
		return groups
	else:
		return None

def process_groups(groups): #Determines which groups are commerce-related
	words = ["auction", "buy","sale","sell","trade"]
	sale_groups = []
	for group in groups:
		lowercase_name = group[0].lower()
		for word in words:
			if word in lowercase_name:
				sale_groups.append(group)
				break
	return sale_groups

def get_posts(group):
	token = ACCESS_TOKEN
	until = int(time())

	since = until - (FREQUENCY * 60 * 60)
	payload = {'access_token': token, 'fields': 'message,id,created_time', 'since': since, 'until': until, 'time_format': 'U'}


	url = 'https://graph.facebook.com/' + group + "/feed"
	r = requests.get(url, params=payload)


	if r.status_code != 200:
		return None
	data = r.json()['data']

	if not data:
		del payload['since']
		del payload['until']
		del payload['time_format']
		payload['limit'] = FREQUENCY*5
		r = requests.get(url, params=payload)
		if r.status_code!=200:
			return None
		data = r.json()['data']
		return time_filter(data, since)
	return data

def time_filter(posts, time):
	intime = []
	for post in posts:
		if iso_to_seconds(post['created_time']) >= time:
			intime.append(post)
	return intime

def iso_to_seconds(ts):
	"""Credit: Ronak @ StackOverflow, http://stackoverflow.com/questions/12223284/"""
	dt = datetime.datetime.strptime(ts[:-5],'%Y-%m-%dT%H:%M:%S')-\
	datetime.timedelta(hours=int(ts[-5:-3]), minutes=int(ts[-2:]))*int(ts[-6:-5]+'1')
	seconds = timegm(dt.timetuple()) + dt.microsecond/1000000
	return seconds

def input_filter(posts, phrase, maxprice=0):
	filtered = []
	if maxprice > Decimal(0):
		for post in posts:
			msg = post['message'].lower()
			if 'free' in msg:
				filtered.append(post)
				pass;
			prices = re.findall(ur'([$])(\d+(?:\.\d{2})?)', post['message'])
			print msg 
			print prices
			for price in prices:
				if Decimal(price[1]) <= maxprice:
					filtered.append(post)
					break;
	if not filtered:
		if maxprice > 0:
			return None
		else:
			filtered = list(posts)
	filtered[:] = [x for x in filtered if phrase in x['message'].lower()]
	return filtered

# def main():
	# groups = get_groups()
	# sale_groups = process_groups(groups)

# if __name__ == "__main__":
# 	main()