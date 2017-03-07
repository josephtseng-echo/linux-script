#!/bin/bash
# -------------------------------------------------------------------------------
# 用于快速定位svn修改的代码
# 修改SVN_BIN svn的路径
# 使用：如 ./svn_find_about.sh /josephzeng/svn/test/api/v2 getMttInfo
# -------------------------------------------------------------------------------

SVN_BIN="/usr/bin/svn"
FIND_DIR=$1
FIND_ABOUT=$2
if [[ $FIND_DIR == "" ]]
then
	echo "请输入查找的目录" 如：./svn_find_about.sh /josephzeng/svn/test/api/v2 getMttInfo
fi
if [[ $FIND_ABOUT == "" ]]
then
	echo "请输入查找的关键字" 如：./svn_find_about.sh /josephzeng/svn/test/api/v2 getMttInfo
fi
for file in `grep -irl --no-messages --exclude=\*.tmp --exclude=\.svn $FIND_ABOUT $FIND_DIR`;     do
    revs="`$SVN_BIN log $file 2> /dev/null | awk '/^r[0-9]+ \|/ { sub(/^r/,"",$1); print  $1  }'`";
    for rev in $revs; do
            diff=`$SVN_BIN diff $file -r$[rev-1]:$rev \
                 --diff-cmd /usr/bin/diff -x "-Ew -U5 --strip-trailing-cr" 2> /dev/null`
            context=`echo "$diff" \
                 | grep -i --color=none -U5 "^\(+\|-\).*$FIND_ABOUT" \
                 | grep -i --color=always -U5             $FIND_ABOUT  \
                 | grep -v '^+++\|^---\|^===\|^Index: ' \
                 `
            if [[ $context ]]; then
                info=`echo "$diff" | grep '^+++\|^---'`
                log=`$SVN_BIN log $file -r$rev`
                echo "========================================================================"
                echo "========================================================================"
                echo "$log"
                echo "$info"
                echo "$context"
                echo
            fi;
    done;
done;
