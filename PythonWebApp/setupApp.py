import GoogleCalendarEvents
import os
import datetime
def scheduleStart():
	now = datetime.datetime.now()
	dayOfWeek = datetime.datetime.today().weekday()
	time = GoogleCalendarEvents.getWakeupTime()
	os.system("crontab -l > mycron")
	os.system("echo '"+str(time[1])+" "+str(time[0])+" "+str(now.day)+" "+str(now.month)+" "+str(dayOfWeek)+" startServer.py' >> mycron")
	os.system("echo '"+str(time[1])+" "+str(time[0])+" "+str(now.day)+" "+str(now.month)+" "+str(dayOfWeek)+" midori localhost:8080 -e Fullscreen' >> mycron") 
	killHour = time[0]
	killMin = time[1]
	if killMin+10 > 60:
		killMin = killMin +10 - 60
		killHour = killHour + 1
	else:
		killMin += 10
	os.system("echo '"+str(killMin)+" "+str(killHour)+" "+str(now.day)+" "+str(now.month)+" "+str(dayOfWeek)+" pkill -9 python' >> mycron")
	os.system("echo '"+str(killMin)+" "+str(killHour)+" "+str(now.day)+" "+str(now.month)+" "+str(dayOfWeek)+" pkill -9 midori' >> mycron")
	os.system("crontab mycron")
	os.system("rm mycron")

scheduleStart()
