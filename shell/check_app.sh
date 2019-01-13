#/**
#* @file   check_app.sh
#* @author josephzeng <josephzeng@by>
#* @date   Thu Jan  3 18:29:56 2019
#* 
#* @brief  
#* 
#* 
#*/


#!/bin/bash

rootDir="/data/server/src/producterServer"

function checkServer_kafka2hdfs() {
	ret=$(ps -ef|grep "consumerServer"|grep "kafka2hdfs"|grep -vc grep)
	echo checkServer_kafka2hdfs $ret
	if [ $ret -eq 0 ] ; then
		test ! -d $rootDir || (cd $rootDir && ./bin/consumerServer --config=$rootDir/src/consumerServer/server.ini --logs=/data/logs/server --server=kafka2hdfs > /dev/null 2>&1 &)
	fi
}

function checkServer_zmq2es() {
	ret=$(ps -ef|grep "consumerServer"|grep "zmq2es"|grep -vc grep)
	echo checkServer_zmq2es $ret
	if [ $ret -eq 0 ] ; then
		test ! -d $rootDir || (cd $rootDir && ./bin/consumerServer --config=$rootDir/src/consumerServer/server.ini --logs=/data/logs/server --server=zmq2es > /dev/null 2>&1 &)
	fi
}

function checkServer_kafka2es() {
	ret=$(ps -ef|grep "consumerServer"|grep "kafka2es"|grep -vc grep)
	echo checkServer_kafka2es $ret
	if [ $ret -eq 0 ] ; then
		test ! -d $rootDir || (cd $rootDir && ./bin/consumerServer --config=$rootDir/src/consumerServer/server.ini --logs=/data/logs/server --server=kafka2es > /dev/null 2>&1 &)
	fi
}

function checkServer_pro() {
	ret=$(ps -ef|grep "./bin/producterServer"|grep -vc grep)
	echo checkServer_pro $ret
	if [ $ret -eq 0 ] ; then
		test ! -d $rootDir || (cd $rootDir && ./bin/producterServer --config=/data/server/src/producterServer/src/producterServer/server.ini --logs=/data/logs/server > /dev/null 2>&1 &)
	fi
}

function main() {
	flock -n 8
	[ $? -eq 1 ] && { echo fail; exit; }
	checkServer_kafka2hdfs
	checkServer_zmq2es
	checkServer_kafka2es
	checkServer_pro
	echo $$
} 8<>mylockfile

main

