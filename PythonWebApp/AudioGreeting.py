from gtts import gTTS
import time
import WeatherData
def greeting(weather,count):
	text = "Good morning Greg! "

	hour = int(time.strftime('%I'))
	day = int(time.strftime('%d'))
	suffix = ""
	if 4 <= day <= 20 or 24 <= day <= 30:
		suffix = "th"
	else:
		suffix = ["st", "nd", "rd"][day % 10 - 1]
	date = "Today is "+str.lower(time.strftime('%A the '))+str(day)+suffix+". The current time is "+str(hour)
	date+=" "+time.strftime("%M %p.")
	text+=date
	if weather.condition == "clear sky":
		weather.condition = "clear skies"
	w = " It is currently "+weather.condition+" outside with a high of "+str(weather.tempMax)+" and a low of "+str(weather.tempMin)+" degrees. "
	text+=w

	text+="You have "+str(count)+" events scheduled for today.\n\n\n"
	return text