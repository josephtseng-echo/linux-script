#!/bin/sh

LOG="/data1/logs/check_php_load.log.`date +"%Y%m%d"`"
PHPVER=$(/usr/local/php/bin/php -i | head |grep "PHP Version"|awk '{print $4}')
HOSTLOAD=$(cat /proc/loadavg | awk '{print $1}' | awk -F . '{print $1}')
HILOAD=30

if [ $HOSTLOAD -gt $HILOAD ]
then
	if [ "$PHPVER" == "5.2.14" ]
	then
		/usr/local/php/sbin/php-fpm restart
		if [ $? -ne 0 ]
		then
			killall -9 php-cgi
			/usr/local/php/sbin/php-fpm restart
		fi
	fi
	if [ "$PHPVER" == "5.3.17" ]
	then
		killall -9 php-fpm;/usr/local/php/sbin/php-fpm
		if [ $? -ne 0 ]
		then
			killall -9 php-fpm;/usr/local/php/sbin/php-fpm
		fi
	fi
	echo "`date +"%Y-%m-%d %H:%M:%S"` check the host load over $HILOAD, restart php $PHPVER" >>$LOG
fi

