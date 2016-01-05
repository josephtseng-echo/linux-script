linux
=====

drop_caches.sh
------
    当free -m  cached超过6000 进行释放内存

    使用方法
    设置定时任务......

check_zk.sh
------
    zk检测
 
	使用方法
	mkdir -p /data2/check_zk/src
    mkdir -p /data2/check_zk/logs
    
    设置定时任务
    #check storm
	*/10 * * * * ( cd /data2/check_zk/src/ && /bin/sh check_zk.sh > /dev/null 2>&1 & )

check_storm.sh
------
    storm检测

	使用方法
	mkdir -p /data2/check_storm/src
    mkdir -p /data2/check_storm/logs
    
    设置定时任务
    #check storm
	*/10 * * * * ( cd /data2/check_storm/src/ && /bin/sh check_storm.sh > /dev/null 2>&1 & )

check_php_load.sh
------
	监听php情况并重启

    使用方法
    设置定时任务......

svn_bak.sh
------
	svn + rsync 备份

rsync.py
------
	svn自动发布脚本

    使用方法
    vim svn项目/hooks/post-commit
    #!/bin/sh
    REPOS="$1"
    REV="$2"
    su josephzeng -c "/usr/local/bin/python2.7 /data1/tools/svn/rsync.py ${REPOS} ${REV} svn项目"

ffmpeg_core.py
------
	ffmpeg压制类库

    使用方法 略
