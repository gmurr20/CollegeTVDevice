#!/bin/bash

#scheduleProcess.sh min hour day month dayNum

if [[ $# -ne 5 ]];
then
	echo "Illegal number of args"
fi

closeMin=$(( ($1+10) % 60))
closeHour=$2
day=$3
month=$4
dayNum=$5

if [[ $(($1+10)) > 59 ]];
then
	closeHour=$(( ($2 + 1) % 24))
fi

#write out current crontab
crontab -l > mycron

#echo new crons into cron file
echo "$1 $2 $day $month $dayNum setTvSettings.sh" >> mycron
echo "$1 $2 $day $month $dayNum startServer.py" >> mycron
echo "$1 $2 $day $month $dayNum openApplication.sh" >> mycron
echo "$closeMin $closeHour $day $month $dayNum shutDown.sh" >> mycron

#install new cron file
crontab mycron
rm mycron