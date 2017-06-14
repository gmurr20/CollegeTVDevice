import pymysql
import datetime
import time

'''
Query the classes table
:return a dictionary of classes that maps class name to class object
'''
def queryClasses():
	connection = pymysql.connect(host='sql9.freemysqlhosting.net', user='sql9178426', password='yuHWs8Hl9y', db='sql9178426', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	#get classes
	classes = []
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM CLASS_T"
			cursor.execute(sql)
			result = cursor.fetchone()
			while result:
				classes.append(result)
				result = cursor.fetchone()
	except:
		print "classes query failed"
	return classes

'''
Query the alarms table
:return a dictionary of alarms that maps day to alarm object
'''
def queryAlarms():
	connection = pymysql.connect(host='sql9.freemysqlhosting.net', user='sql9178426', password='yuHWs8Hl9y', db='sql9178426', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	#get alarm times
	alarms = {}
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM ALARM_T"
			cursor.execute(sql)
			result = cursor.fetchone()
			while result:
				classes[result['DayOfWeek']] = result
				result = cursor.fetchone()
	except:
		print "alarm query failed"
	return alarms

'''
Query the homework table for all homework in the next week
:return a list of homework objects
'''
def queryHomework():
	connection = pymysql.connect(host='sql9.freemysqlhosting.net', user='sql9178426', password='yuHWs8Hl9y', db='sql9178426', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	homework = []
	twoDaysAgo = (datetime.date.today()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")
	weekLater = (datetime.date.today()+datetime.timedelta(days=7)).strftime("%Y-%m-%d")
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM HOMEWORK_T WHERE dueDate BETWEEN '%s' and '%s'" % (str(twoDaysAgo),str(weekLater))
			cursor.execute(sql)
			result = cursor.fetchone()
			while result:
				homework.append(result)
				result = cursor.fetchone()
	except:
		print "homework query failed"
	return homework

'''
Query the other table for all miscellaneous schedule items in the next week
:return a list of schedule objects
'''
def queryOtherSchedule():
	connection = pymysql.connect(host='sql9.freemysqlhosting.net', user='sql9178426', password='yuHWs8Hl9y', db='sql9178426', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	other = []
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM OTHER_T WHERE dueDate BETWEEN '%s' and '%s'" % (str(twoDaysAgo),str(weekLater))
			cursor.execute(sql)
			result = cursor.fetchone()
			while result:
				other.append(result)
				result = cursor.fetchone()
	except:
		print "other query failed"
	return other

def processTodaysSchedule():
	classes = queryClasses()
	today = str(time.strftime('%a'))[0:3]
	schedule = []
	for c in classes:
		if today in c['DaysOfWeek']:
			schedule.append((c['Class'], c['StartTime'], c['EndTime'], True))
	other = queryOtherSchedule()
	for o in other:
		if today in o['dueDate'].strftime('%a')[0:3]:
			schedule.append((o['Title'], o['StartTime'], o['EndTime'], False))
	schedule = sorted(schedule, key=lambda x:x[1])
	return schedule

def processHomework():
	homework = queryHomework()
	sortedHwk = []
	for h in homework:
		info = h['dueDate'].strftime('%a')[0:3]+": "+h['Class']+"-"+h['Title']
		sortedHwk.append((info, h['Exam'], h['dueDate']))
	sortedHwk = sorted(sortedHwk, key=lambda x:x[2])
	return sortedHwk