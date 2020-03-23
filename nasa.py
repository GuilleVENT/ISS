# Created for fun by Guillermo Ventura 

import json
import requests

import time
import datetime

#pimport icalendar

# debugging
from termcolor import colored
import sys

# user location
import geopy.distance #from geopy.distance import vincenty
import geocoder

user_lat = 0
user_lon = 0 
distance_arr = []


def iss_data(data):
	print(" * * * * * * * * * * * * * * * * * * * * * * ")
	print(" * * * * * * * * * ISS * * * * * * * * * * * ")
	iss_position = data['iss_position']

	print(colored('Latitude:','blue'))
	print(iss_position['latitude'])
	print(colored('Longitude:','magenta'))
	print(iss_position['longitude'])

	return iss_position['latitude'], iss_position['longitude']



def user_position():
	print(" * * * * * * * * * USER * * * * * * * * * * * ")
	g = geocoder.ip('me')
	print(g.latlng)
	lat=g.latlng[0]
	lng=g.latlng[1]

	return lat, lng


def calculate_distance(iss_lat, iss_lon, user_lat, user_lon):

	print(" * * * * * * * * DISTANCE * * * * * * * * * * ")
	distance = geopy.distance.geodesic((iss_lat,iss_lon), (user_lat, user_lon)).meters
	print(distance, 'kilometers')

	return distance # new distance not global



def init():
	global user_lat,user_lon
	response = requests.request('GET', 'http://api.open-notify.org/iss-now.json')
	data = json.loads(response.text)

	if data['message'] == 'success':
		print(colored('SUCCESS','green'))
		iss_lat, iss_lon   = iss_data(data)
		if user_lat == 0 and user_lon == 0:
			user_lat, user_lon = user_position()

		distance_new = calculate_distance(iss_lat, iss_lon, user_lat,user_lon)
		distance_arr.append(distance_new)	
	
	else:
		print(colored('Something went wrong requesting ISS data:','red'))
		print(data)


while True:
	init()
	time.sleep(5)
	print(' - * - * - * - * - * - * - * - * - * - * - * - * - * - * ')
	#break
