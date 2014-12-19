# -*- coding: utf-8 -*-
# author:josephzeng email:josephzeng36@gmail.com
# des: svn自动发布脚本
import locale
language_code, encoding = locale.getdefaultlocale()
if language_code is None:
    language_code = 'zh_CN'
if encoding is None:
    encoding = 'UTF-8'
if encoding.lower() == 'utf':
    encoding = 'UTF-8'
locale.setlocale( locale.LC_ALL, '%s.%s' % (language_code, encoding))

import sys
import pysvn
import os
import time
import urllib
import codecs

svnurl = "svn://127.0.0.1:1234/"
svntmp = "/data1/tools/svn/svn_tmp/"
rsync_server = {
    'www.com':['www@127.0.0.1::www.com'],
    'www.com':['www@127.0.0.1::www.com', "www2@127.0.0.1::www2.com"]
}

def get_login(*args):
    return True, "test", "123456", False
 

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        print "params error!"
	sys.exit()
    repos = args[1]
    rev = args[2]
    project = args[3]
    revision_min = pysvn.Revision( pysvn.opt_revision_kind.number, int(rev) )
    revision_max = pysvn.Revision( pysvn.opt_revision_kind.number, int(rev) )
    #svn地址
    svnClient = pysvn.Client()
    svnClient.callback_get_login = get_login
    svnurl = svnurl + project
    svntmp = svntmp + project
    logs = svnClient.log(svnurl,
                     revision_min,
                     revision_max,
                     discover_changed_paths=True,
                     strict_node_history=True,
                     limit=0)
    rsync_todo_lists = []
    for log in logs:
        for i in log['changed_paths']:
            rsync_todo = rsync_server.get(project)
	    if rsync_todo == None:
                pass
            else:
                tmp = {}
                tmp['team'] = project
                tmp['number'] = log.revision.number
                tmp['author'] = log["author"]
                tmp['message'] = log["message"]
                tmp['date'] = log['date']
                tmp['todofile'] = None
                tmp['todotype'] = None
                filecheck = None
                todotype = None
                #print filecheck
            	if i['action'] == 'D':
            	    filecheck = svntmp + i['path']
                    todotype = 'delete'
            	if i['action'] == 'M' or i['action'] == 'A':
            	    filecheck = svntmp + i['path']
		    exp_url = svnurl+i['path']
		    exp_url_des = filecheck[0:filecheck.rfind("/")]
		    if not os.path.exists(exp_url_des):
		        os.makedirs(exp_url_des)
		    try:
		        svnClient.export(exp_url, filecheck, False, revision_max)
		    except:
		        pass
                    todotype = 'update'
                tmp['todofile'] = filecheck
                tmp['todotype'] = todotype
                tmp['todopath'] = i['path']
                tmp['todoserver'] = rsync_todo
                rsync_todo_lists.append(tmp)
    todo_lists_tmp = []
    if len(rsync_todo_lists) > 0:
        for item in rsync_todo_lists:
            todofile = item['todofile']
            checktodofile = svntmp + '/' + item['team']
            if todofile != checktodofile:
                todo_lists_tmp.append(item)
    todo_cmds = []
    if len(todo_lists_tmp) > 0:
       	log_txt = time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt'
        fp = open('/data1/tools/svn/logs/'+log_txt, 'ab+')
        for item in todo_lists_tmp:
            todoserver = item['todoserver']
            if len(todoserver) > 0:
                for i in todoserver:
                    if item['todotype'] == 'update':
                        cmd = '/usr/bin/rsync -CavuR '
                        todopath = item['todopath'].split('/')[2:-1]
			todopathstr = "/".join(todopath)
			todofilerootdir = item['todofile'].split('/')[0:6]
			todofileupload = item['todofile'].split('/')[6:]
			todofilerootdirstr = "/".join(todofilerootdir)
			todofileuploadstr = "/".join(todofileupload);
			newcmd = 'cd '+todofilerootdirstr+ '; ' + cmd + todofileuploadstr + ' ' + i
			os.system(newcmd)
                        fp.write(item['team']+"#"+item['author']+"#"+str(item['number']) +"#"+\
                                     "update#" +str(newcmd)+"#"+time.strftime('%Y-%m-%d %H:%M:%S', \
                                     time.localtime(time.time()))+"\n")
                    if item['todotype'] == 'delete':
                        cmd = '/usr/bin/rsync -avz '
                        todopath = item['todopath'].split('/')[2:-1]
			todopathstr = "/".join(todopath)
			todofilerootdir = item['todofile'].split('/')[6:-1]
			todofileupload = item['todofile'].split('/')[-1:]
			todofilerootdirstr = "/".join(todofilerootdir)
			todofileuploadstr = "/".join(todofileupload);
			cdrootdir = item['todofile'].split('/')[0:-1]
			chrootdirstr = "/".join(cdrootdir);
                        try:
			    if(os.path.isfile(item['todofile'])):
			        d_cmd = 'rm -rf '+item['todofile'];
				os.system(d_cmd)
			    if(os.path.exists(item['todofile'])):
			        d_cmd = 'rm -rf '+item['todofile'];
				os.system(d_cmd)
			    cmd = 'cd ' + chrootdirstr + '; ' + cmd + ' --include="'+todofileuploadstr+'" --exclude="*" --delete --delete-during ./ '+ str(i) + '/' + todofilerootdirstr + '/'
			    os.system(cmd)
			    #print cmd
			except:
			    pass
                        fp.write(item['team']+"#"+item['author']+"#"+ str(item['number'])+"#"+\
                                     "delete#" +str(cmd)+"#"+time.strftime('%Y-%m-%d %H:%M:%S', \
                                     time.localtime(time.time()))+"\n")
        fp.close() 
    sys.exit()
    	
