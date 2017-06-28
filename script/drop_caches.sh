#!/bin/bash
#当free -m  cached超过6000 进行释放内存
#第一种写法
str=$( free -m )
arr=(${str// / })
check=$(expr ${arr[12]} + 0)
if [ ${check} -gt 6000  ];then
    ( echo 3 >  /proc/sys/vm/drop_caches )
fi

#第二种写法
freeMem=$(free -m|awk '/buffers\/cache/{print $4}')
MaxValue=6000

if [ ${freeMem} -gt ${MaxValue}  ];then
    ( echo 3 >  /proc/sys/vm/drop_caches )
fi
