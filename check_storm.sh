#!/bin/bash
#log
LOG="../logs/check_storm.log".`date +"%Y%m%d"`

export PATH=$PATH:/opt/app/jdk1.7.0_51/bin


( /bin/ps -efw | grep 'backtype.storm.daemon.nimbus' | grep -v grep )
if [ $? -ne 0 ];then
    echo "`date +"%Y-%m-%d %H:%M:%S"` check nimbus 异常" >> $LOG
    ( cd /opt/app/apache-storm-0.9.5 && ./bin/storm nimbus > /dev/null 2>&1 & )
    echo "`date +"%Y-%m-%d %H:%M:%S"` nimbus 重新启动" >> $LOG
else
    echo "`date +"%Y-%m-%d %H:%M:%S"` check nimbus ok" >> $LOG
fi

( /bin/ps -efw | grep 'backtype.storm.daemon.supervisor' | grep -v grep )
if [ $? -ne 0 ];then
    echo "`date +"%Y-%m-%d %H:%M:%S"` check supervisor 异常" >> $LOG
    ( cd /opt/app/apache-storm-0.9.5 && ./bin/storm supervisor  > /dev/null 2>&1 & )
    echo "`date +"%Y-%m-%d %H:%M:%S"` supervisor 重新启动" >> $LOG
else
    echo "`date +"%Y-%m-%d %H:%M:%S"` check supervisor ok" >> $LOG
fi

( /bin/ps -efw | grep 'backtype.storm.ui' | grep -v grep )
if [ $? -ne 0 ];then
    echo "`date +"%Y-%m-%d %H:%M:%S"` check ui 异常" >> $LOG
    ( cd /opt/app/apache-storm-0.9.5 && ./bin/storm ui > /dev/null 2>&1 & )
    echo "`date +"%Y-%m-%d %H:%M:%S"` ui 重新启动" >> $LOG
else
    echo "`date +"%Y-%m-%d %H:%M:%S"` check ui ok" >> $LOG
fi

str=$(/opt/app/apache-storm-0.9.5/bin/storm list | grep ACTIVE | grep -v grep )
arr=(${str// / })
if [ "${arr[1]}" == "ACTIVE" ];then
    echo "`date +"%Y-%m-%d %H:%M:%S"` check storm list ok" >> $LOG
else
    echo "`date +"%Y-%m-%d %H:%M:%S"` check storm list 异常" >> $LOG
    ( cd /opt/app/apache-storm-0.9.5 && ./bin/storm jar /opt/app/test/test-analysis-0.0.1-SNAPSHOT.jar com.zshuiquan.test.AnalysisClient )
    echo "`date +"%Y-%m-%d %H:%M:%S"`  重新提交Topology " >> $LOG
fi
