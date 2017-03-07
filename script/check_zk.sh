#!/bin/bash
#log
LOG="../logs/check_zk.log".`date +"%Y%m%d"`


( /bin/ps -efw | grep '/opt/app/zookeeper-3.4.6/bin/' | grep -v grep )
if [ $? -ne 0 ];then
    echo "`date +"%Y-%m-%d %H:%M:%S"` check zk 异常" >> $LOG
    ( cd /opt/app/zookeeper-3.4.6/ && ./bin/zkServer.sh ./conf/zoo.cfg > /dev/null 2>&1 & )
    echo "`date +"%Y-%m-%d %H:%M:%S"` zk 重新启动" >> $LOG
else
    echo "`date +"%Y-%m-%d %H:%M:%S"` check zk ok" >> $LOG
fi

#当free -m  cached超过6000 进行释放内存
str=$( free -m )
arr=(${str// / })
check=$(expr ${arr[12]} + 0)
if [ ${check} -gt 6000  ];then
    ( echo 1 >  /proc/sys/vm/drop_cache )
fi
