#!/bin/bash
# bak svn and rsync bak file
# author:josephzeng email:josephzeng36@gmail.com
# des: svn备份 初始化 增量备份
# date:2014-12-17
# edit by josephzeng add msg tip 2014-12-18
# Release: 0.1

#svn 项目列表
SVN_PROJECTS="test a"

#svn 项目路径
SVN_DIR="/data2/svndata"

#svn 备份路径
SVN_BAK_DIR="/data2/svn_backup"

#记录log日志路径
SVN_PROJECTS_LOG_DIR="/root/tools/log"

#脚本执行记录日志文件
TODO_LOG_FILE="$SVN_PROJECTS_LOG_DIR/todo.log"

#rsync主机
RSYNC_CONFIG="root@127.0.0.1::test"

#短信接收人多个的话使用“;”分开
MSG_USERS="josephzeng"

BIN_SVNLOOK="/usr/bin/svnlook youngest"
BIN_SVNADMIN="/usr/bin/svnadmin"
BIN_GZIP="/bin/gzip"
BIN_RSYNC="/usr/bin/rsync"
BIN_CURL="/usr/bin/curl -s"

DATE=`date +%Y%m%d`
NOW_TIME=`date +%Y-%m-%d-%H:%M:%S`
if [ ! -d $SVN_BAK_DIR ]
then
	/bin/mkdir $SVN_BAK_DIR -p
fi
if [ ! -d $SVN_PROJECTS_LOG_DIR ]
then
	/bin/mkdir $SVN_PROJECTS_LOG_DIR -p
fi

#rsync 失败后会重试一次并发短信报警
function todo_rsync()
{
    cd $4
	${BIN_RSYNC} -CavuR $1 $2 > /dev/null
	if [ $? -ne 0 ];then
        cd $4
		${BIN_RSYNC} -CavuR $1 $2 > /dev/null
        if [ $? -ne 0 ];then
            #msg
		    echo "${NOW_TIME} | ${BIN_RSYNC} -CavuR $1 $2 | todo rsync fail" >> ${TODO_LOG_FILE}
            ${BIN_CURL} "短信接口"
        fi
		echo "${NOW_TIME} | ${BIN_RSYNC} -CavuR $1 $2 | todo rsync again" >> ${TODO_LOG_FILE}
    fi
}

for i in $SVN_PROJECTS
do
	$BIN_SVNLOOK $SVN_DIR/$i >> $SVN_PROJECTS_LOG_DIR/$i.log
	#write log
	echo "$NOW_TIME | $BIN_SVNLOOK $SVN_DIR/$i >> $SVN_PROJECTS_LOG_DIR/$i.log" >> $TODO_LOG_FILE

	head_REV=`head -1 $SVN_PROJECTS_LOG_DIR/$i.log`

	#初始化 init
	count_REV=`tac $SVN_PROJECTS_LOG_DIR/$i.log | wc -l`
	if [[ $count_REV == 1 ]];then
		$BIN_SVNADMIN dump $SVN_DIR/$i -r 1:${head_REV}  > $SVN_BAK_DIR/${DATE}_init_$i.dump
		echo "$NOW_TIME | $BIN_SVNADMIN dump $SVN_DIR/$i -r 1:${head_REV}  > $SVN_BAK_DIR/${DATE}_init_$i.dump" >> $TODO_LOG_FILE
		#gzip
		$BIN_GZIP -9 -c $SVN_BAK_DIR/${DATE}_init_$i.dump > $SVN_BAK_DIR/${DATE}_init_$i.dump.gz
		echo "$NOW_TIME | $BIN_GZIP -9 -c $SVN_BAK_DIR/${DATE}_init_$i.dump > $SVN_BAK_DIR/${DATE}_init_$i.dump.gz" >> $TODO_LOG_FILE
		#todo rsync bak file
        todo_rsync ${DATE}_init_$i.dump.gz ${RSYNC_CONFIG} $i ${SVN_BAK_DIR}
		echo "$NOW_TIME | ${BIN_RSYNC} -CavuR ${DATE}_init_$i.dump.gz ${RSYNC_CONFIG}" >> $TODO_LOG_FILE
		#todo rm bak file
		rm ${SVN_BAK_DIR}/${DATE}_init_$i.dump
		rm ${SVN_BAK_DIR}/${DATE}_init_$i.dump.gz
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_init_$i.dump" >> $TODO_LOG_FILE
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_init_$i.dump.gz" >> $TODO_LOG_FILE
	fi

	old_REV=$[${head_REV}+1]
	last_REV=`tac $SVN_PROJECTS_LOG_DIR/$i.log|sed -ne 2p`
	start_REV=$[${last_REV}+1]
	end_REV=`tac $SVN_PROJECTS_LOG_DIR/$i.log|head -1`
	DAY=`cal |grep -v '^$'|tail -1 |awk '{print $NF}'`
	NOW_DAY=`date +%d`
	while [[ ${last_REV} -lt ${end_REV} ]];
	do
		#todo day bak
		$BIN_SVNADMIN dump $SVN_DIR/$i -r ${start_REV}:${end_REV} --incremental > $SVN_BAK_DIR/${DATE}_$i.dump
		echo "$NOW_TIME | $BIN_SVNADMIN dump $SVN_DIR/$i -r ${start_REV}:${end_REV} --incremental > $SVN_BAK_DIR/${DATE}_$i.dump" >> $TODO_LOG_FILE
		#gzip
		$BIN_GZIP -9 -c $SVN_BAK_DIR/${DATE}_$i.dump > $SVN_BAK_DIR/${DATE}_$i.dump.gz
		echo "$NOW_TIME | $BIN_GZIP -9 -c $SVN_BAK_DIR/${DATE}_$i.dump > $SVN_BAK_DIR/${DATE}_$i.dump.gz" >> $TODO_LOG_FILE
		#todo rsync bak file
        todo_rsync ${DATE}_$i.dump.gz ${RSYNC_CONFIG} $i ${SVN_BAK_DIR}
		echo "$NOW_TIME | ${BIN_RSYNC} -CavuR ${DATE}_$i.dump.gz ${RSYNC_CONFIG}" >> $TODO_LOG_FILE
		#todo rm bak file
		rm ${SVN_BAK_DIR}/${DATE}_$i.dump
		rm ${SVN_BAK_DIR}/${DATE}_$i.dump.gz
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_$i.dump" >> $TODO_LOG_FILE
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_$i.dump.gz" >> $TODO_LOG_FILE
		break
	done
	if [ ${NOW_DAY} -eq $DAY -a ${head_REV} -lt ${end_REV} ];then
		#todo month bak 
		$BIN_SVNADMIN dump ${SVN_DIR}/$i -r ${old_REV}:${end_REV} --incremental > ${SVN_BAK_DIR}/${DATE}_$i_month.dump 
		echo "$NOW_TIME | $BIN_SVNADMIN dump ${SVN_DIR}/$i -r ${old_REV}:${end_REV} --incremental > ${SVN_BAK_DIR}/${DATE}_$i_month.dump" >> $TODO_LOG_FILE
		#gzip
		$BIN_GZIP -9 -c ${SVN_BAK_DIR}/${DATE}_$i_month.dump > ${SVN_BAK_DIR}/${DATE}_$i_month.dump.gz
		echo "$NOW_TIME | $BIN_GZIP -9 -c ${SVN_BAK_DIR}/${DATE}_$i_month.dump > ${SVN_BAK_DIR}/${DATE}_$i_month.dump.gz" >> $TODO_LOG_FILE
		#todo rsync bak file
        todo_rsync ${DATE}_$i_month.dump.gz ${RSYNC_CONFIG} $i
		echo "$NOW_TIME | ${BIN_RSYNC} -CavuR ${DATE}_$i_month.dump.gz ${RSYNC_CONFIG}" >> $TODO_LOG_FILE
		#todo rm bak file
		rm ${SVN_BAK_DIR}/${DATE}_$i_month.dump
		rm ${SVN_BAK_DIR}/${DATE}_$i_month.dump.gz
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_$i_month.dump" >> $TODO_LOG_FILE
		echo "$NOW_TIME | rm ${SVN_BAK_DIR}/${DATE}_$i_month.dump.gz" >> $TODO_LOG_FILE
	fi
done
