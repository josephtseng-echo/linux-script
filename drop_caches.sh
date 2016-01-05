#!/bin/bash
#当free -m  cached超过6000 进行释放内存
str=$( free -m )
arr=(${str// / })
check=$(expr ${arr[12]} + 0)
if [ ${check} -gt 6000  ];then
    ( echo 1 >  /proc/sys/vm/drop_cache )
fi
