import requests
import json
import datetime
import calendar
import time

import properties

'''
WeatherUnit is a class containing necessary info to show 
the weather info and render appropriate images
'''
class weatherUnit:
	condition = ""
	temp = 0.0
	tempMin = 0.0
	tempMax = 0.0
	sunrise = ""
	sunset = ""
	city = ""
	icon = ""
	day = ""

	'''
	Initialize object, and pad the temperature for single digits
	'''
	def __init__(self, condition, tempMin, tempMax, icon, day):
		self.condition = condition
		self.icon = icon
		self.day = day

		#pad temperature
		self.tempMin = int(round(tempMin))
		if(self.tempMin < 10 and self.tempMin >=0):
			self.tempMin = "0"+str(self.tempMin)
		elif(self.tempMin > -10 and self.tempMin < 0):
			self.tempMin = "-0"+str(abs(self.tempMin))
		self.tempMax = int(round(tempMax))
		if(self.tempMax < 10 and self.tempMax >=0):
			self.tempMax = "0"+str(self.tempMax)
		elif(self.tempMax > -10 and self.tempMax < 0):
			self.tempMax = "-0"+str(abs(self.tempMax))
		
	'''
	Set additional fields for today's weather to show
	'''
	def setToday(self, city, temp, sunrise, sunset):
		self.city = city
		self.sunrise = sunrise
		self.sunset = sunset

		#pad temperature
		self.temp = int(round(temp))
		if(self.temp < 10 and self.temp >= 0):
			self.temp = "0"+self.temp
		elif(self.temp > -10 and self.temp < 0):
			self.temp = "-0"+str(abs(self.temp))
		
'''
pull today's weather from openweathermap api
'''
def pullToday():
	todayForecast = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+properties.weatherId+'&units=imperial&APPID='+properties.weatherApiKey)
	today = json.loads(todayForecast.text)
	cond = today['weather'][0]['description']
	temp = today['main']['temp']
	tempMin = today['main']['temp_min']
	tempMax = today['main']['temp_max']
	icon = today['weather'][0]['icon']
	icon = "http://openweathermap.org/img/w/"+icon+".png"
	city = today['name']
	sunrise = today['sys']['sunrise']
	day = datetime.datetime.fromtimestamp(int(sunrise)).strftime('%a')
	sunrise = datetime.datetime.fromtimestamp(int(sunrise)).strftime('%H:%M')+"AM"
	sunset = today['sys']['sunset']
	sunsetH = datetime.datetime.fromtimestamp(int(sunset)).strftime('%H')
	sunsetH = "0"+str(int(sunsetH)-12)
	sunsetM = datetime.datetime.fromtimestamp(int(sunset)).strftime('%M')
	sunset = sunsetH+":"+sunsetM+"PM"
	todaysWeather = weatherUnit(cond, tempMin, tempMax, icon, day)
	todaysWeather.setToday(city, temp, sunrise, sunset)
	return todaysWeather

'''
pull future weather from openweathermap api
'''
def pullFutureWeather(weatherList, currentDay):
	dailyRequest = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?id='+properties.weatherId+'&units=imperial&APPID='+properties.weatherApiKey)
	daily = json.loads(dailyRequest.text)
	dailyList = daily['list']
	count = 0
	for i in range(len(dailyList)):
		if count == 4:
			break
		day = dailyList[i]
		dt = datetime.datetime.fromtimestamp(int(day['dt'])).strftime('%a')
		if currentDay == dt or calendar.timegm(time.gmtime()) >= int(day['dt']):
			continue
		cond = day['weather'][0]['description']
		tempMin = day['temp']['min']
		tempMax = day['temp']['max']
		icon = day['weather'][0]['icon']
		icon = "http://openweathermap.org/img/w/"+icon+".png"
		weather = weatherUnit(cond, tempMin, tempMax, icon, dt)
		weatherList.append(weather)
		count += 1

'''
pull weather data from openweathermap api
'''
def pullWeatherData():
	weatherList = []
	today = pullToday()
	weatherList.append(today)
	pullFutureWeather(weatherList,today.day)
	return weatherList

