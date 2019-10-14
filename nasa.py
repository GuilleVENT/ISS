
# ISS api
import json
import requests

import time
import datetime
import icalendar

from termcolor import colored

# user location
#from geopy.distance import vincenty

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
	print(" * * * * * * * * * USER * * * * * * * * * * *")
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	print(r['message'])
	sys.exit()
	location = json.loads(r.text)

	print(colored('Latitude:','blue'))
	print(location['latitude'])
	print(colored('Longitude:','magenta'))
	print(location['longitude'])

	return location['latitude'],location['longitude']


def calculate_distance(iss_lat, iss_lon, user_lat, user_lon):

	print(" * * * * * * * * DISTANCE * * * * * * * * * * ")
	distance = vincenty((iss_lat,iss_lon), (user_lat, user_lon)).meters
	print(distance, 'meters')

	response = requests.request('GET','http://api.open-notify.org/iss-pass.json?lat='+str(user_lat)+'&lon='+str(user_lon)+'&n=5')
	data = json.loads(response.text)

	if data['message'] == 'success':
		print(" success")
		next_times =  data['response']
		for time in next_times:
			print("duration")
			print(time['duration'])
			print("time")
			#print time['risetime']
			print(datetime.datetime.fromtimestamp(time['risetime']).strftime('%Y-%m-%d %H:%M:%S'))


	return distance # new distance not global



def init():
	response = requests.request('GET', 'http://api.open-notify.org/iss-now.json')


	data = json.loads(response.text)

	#print(data)


	if data['message'] == 'success':
		print(colored('SUCCESS','green'))
		iss_lat, iss_lon   = iss_data(data)

	global user_lat, user_lon 

	if user_lat == 0 or  user_lon == 0:
		user_lat, user_lon = user_position()

	distance_new = calculate_distance(iss_lat, iss_lon, user_lat,user_lon)
	distance_arr.append(distance_new)


while True:
	init()
	#time.sleep(5)
	break

# NASA-API
#api_key = "3f5LI3hMi848kx2xL0cWcvQOPasG9kvgeCSoHCPL"