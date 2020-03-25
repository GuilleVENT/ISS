# Created for fun by Guillermo Ventura 

import json
import requests

import time
import datetime

#import icalendar

# debugging
from termcolor import colored
import sys

# user location
import geopy.distance #from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import geocoder

# parse arguments
import argparse

city_input = False
city = ''

user_lat = 0
user_lon = 0 

distance_arr = []


## parse Input City:
parser = argparse.ArgumentParser(description='INPUT CITY')

parser.add_argument('-city', nargs='?', default='none', help = "Input City [if city-name contains spaces please use apostrophes example: 'New York City' ")
args = parser.parse_args()

if args.city != 'none': 
	city_input = True
	city = args.city

	print('Input City: '+  colored(city,'green'))


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

def city_coordinates(city):

	geolocator = Nominatim(user_agent="my-application")
	loc = geolocator.geocode(city)
	## input city lat and lon:
	#print(loc.latitude)
	#print(loc.longitude)

	return loc.latitude, loc.longitude

def init():
	global user_lat,user_lon
	response = requests.request('GET', 'http://api.open-notify.org/iss-now.json')
	data = json.loads(response.text)

	if data['message'] == 'success':
		print(colored('SUCCESS','green'))
		iss_lat, iss_lon   = iss_data(data)
		
		if city_input == False: # get user position
			if user_lat == 0 and user_lon == 0:
				user_lat, user_lon = user_position()

		else: 
			if user_lat == 0 and user_lon == 0:
				user_lat, user_lon = city_coordinates(city)

		distance_new = calculate_distance(iss_lat, iss_lon, user_lat,user_lon)
		distance_arr.append(distance_new)	

		## follow here: 
		##  https://www.youtube.com/watch?v=8v3how07th4
		## or 
		## this
		## https://python-graph-gallery.com/310-basic-map-with-markers/		
	
	else:
		print(colored('Something went wrong requesting ISS data:','red'))
		print(data)


while True:
	init()
	time.sleep(5)
	print(' - * - * - * - * - * - * - * - * - * - * - * - * - * - * ')
	#break
