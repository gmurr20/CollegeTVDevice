import web

import WeatherData
import News
import AudioGreeting
import GoogleCalendarEvents

'''
Opens a localhost:8080 that renders the web application together
'''
urls = (
    '/', 'index'
)
render = web.template.render('templates/', base="layout")

class index:
	def GET(self):
		weatherList = WeatherData.pullWeatherData()
		newsList = News.pullNews()
		scheduleList = GoogleCalendarEvents.getSchedule()
		homeworkList = GoogleCalendarEvents.getHomework()
		audioGreeting = AudioGreeting.greeting(weatherList[0], len(scheduleList))
		return render.index(weatherList, newsList, scheduleList, homeworkList, audioGreeting)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
