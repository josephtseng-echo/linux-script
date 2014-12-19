linux
=====

svn_bak.sh svn备份
------

rsync.py svn自动发布脚本
------
### 使用方法
### vim svn项目/hooks/post-commit
    #!/bin/sh
    REPOS="$1"
    REV="$2"
    su josephzeng -c "/usr/local/bin/python2.7 /data1/tools/svn/rsync.py ${REPOS} ${REV} svn项目"
