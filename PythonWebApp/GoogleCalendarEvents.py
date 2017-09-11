#Reskinned from GoogleCalendarAPI starter script from their site. Cannot take credit for majority of this code.

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from datetime import timedelta
import calendar

'''
Class to store relevant information for a scheduled event or homework
'''
class scheduleEvent:
    start = ""
    end = ""
    location = ""
    name = ""
    description = ""
    day = ""
    isClass = False
    isExam = False
    def __init__(self, start, end, loc, name, description):
        self.start = start
        self.end = end
        self.location = loc
        self.name = name
        self.description = description

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

'''
Get everything on my calendar for the next 24 hours
'''
def getSchedule():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #get all events for the next 24 hours
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    later = (datetime.datetime.utcnow() + timedelta(hours=24) ).isoformat() + 'Z'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=later, maxResults=8, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    scheduleList = []
    if not events:
        print('No events for today')
    else:
        for event in events:

            #try and get the name, continue if its homework
            try:
                name = str(event.get('summary'))
                if "hwk" in str.lower(name) or "homework" in str.lower(name):
                    continue
            except:
                continue

            #get the start and end dates if they exist
            try:
                start = event['start']['dateTime']
                start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S-05:00").strftime('%I:%M')
                end = event['end']['dateTime']
                end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S-05:00").strftime('%I:%M%p')
            except:
                start = ""
                end = ""

            #get the location if it exist
            try:
                location = event.get('location')
            except:
                location = ""

            #get the description and see if its a class
            isClass = False
            try:
                description = str(event['description'])
                if "hwk" in str.lower(description) or "homework" in str.lower(description):
                    continue
                if "class" in str.lower(description):
                    isClass = True
            except:
                description = ""

            sched = scheduleEvent(start, end, location, name, description)
            sched.isClass = isClass
            scheduleList.append(sched)

    return scheduleList

'''
Get all the homework for the next 168 hours
'''
def getHomework():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #get the events for the next week
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    later = (datetime.datetime.utcnow() + timedelta(hours=168) ).isoformat() + 'Z'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=later, maxResults=8, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    scheduleList = []
    if not events:
        print('No events for today')
    else:
        for event in events:

            #extract name and see if it is an exam
            isExam = False
            try:
                name = str(event.get('summary'))
                if "exam" in str.lower(name) or "midterm" in str.lower(name):
                    isExam = True
                elif "hwk" not in str.lower(name) and "homework" not in str.lower(name):
                    continue
            except:
                continue

            #get the start and end date if it exist
            try:
                start = event['start']['dateTime']
                start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S-05:00").strftime('%I:%M')
                end = event['end']['dateTime']
                end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S-05:00").strftime('%I:%M%p')
            except:
                start = ""
                end = ""

            #get the location
            try:
                location = event.get('location')
            except:
                location = ""

            #Get the description and see if it is an exam or homework
            try:
                description = event['description']
                if "exam" in str.lower(description) or "midterm" in str.lower(description):
                    isExam = True
                elif "hwk" not in str.lower(description) and "homework" not in str.lower(description):
                    continue
            except:
                description = ""

            #get the date and day
            try:
                date = event['start']['date']
                date = date.split('-')
                dayDigit = calendar.weekday(int(date[0]), int(date[1]), int(date[2]))
                day = calendar.day_name[dayDigit][0:3]
            except:
                continue

            sched = scheduleEvent(start, end, location, name, description)
            sched.day = day
            sched.isExam = isExam
            scheduleList.append(sched)

    return scheduleList

def getWakeupTime():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	#get the events for the next week
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	later = (datetime.datetime.utcnow() + timedelta(hours=24) ).isoformat() + 'Z'
	eventsResult = service.events().list()
	calendarId='primary', timeMin=now, timeMax=later, maxResults=8, singleEvents=True,
        orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	if not events:
        	print('No events for today')
	else:
		for event in events:

            	#get the start and end date if it exist
            		try:
                		start = event['start']['dateTime']
                		start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S-05:00").strftime('%I:%M')
                		hour = start.split(':')[0]
                		minute = int(start.split(':')[1])-45
                		if minute < 0:
                    			minute = 60+minute
                    			hour = hour - 1
                		return (hour, minute)
            		except:
                		continue

	return (6, 45)
