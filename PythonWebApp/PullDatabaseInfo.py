import pymysql
import time
import datetime

connection = pymysql.connect(host='sql9.freemysqlhosting.net', user='sql9178426', password='yuHWs8Hl9y', db='sql9178426', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

#get classes
classes = {}
try:
	with connection.cursor() as cursor:
		sql = "SELECT * FROM CLASS_T"
		cursor.execute(sql)
		result = cursor.fetchone()
		while result:
			classes[result['Class']] = result
			result = cursor.fetchone()
except:
	print "classes query failed"

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

#get homework times
homework = []
today = (datetime.date.today()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")
weekLater = (datetime.date.today()+datetime.timedelta(days=7)).strftime("%Y-%m-%d")
try:
	with connection.cursor() as cursor:
		sql = "SELECT * FROM HOMEWORK_T WHERE dueDate BETWEEN '%s' and '%s'" % (str(today),str(weekLater))
		cursor.execute(sql)
		result = cursor.fetchone()
		while result:
			homework.append(result)
			result = cursor.fetchone()
except:
	print "homework query failed"

#get miscellaneous from schedule
other = []
try:
	with connection.cursor() as cursor:
		sql = "SELECT * FROM OTHER_T WHERE dueDate BETWEEN '%s' and '%s'" % (str(today),str(weekLater))
		cursor.execute(sql)
		result = cursor.fetchone()
		while result:
			other.append(result)
			result = cursor.fetchone()
except:
	print "other query failed"