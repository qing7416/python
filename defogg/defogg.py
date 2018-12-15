# coding=utf-8
'''
# Automatically generate oracle goldengate configuration file
# python3.6
# 2018-11-24 22:51 生成ogg源端和目标端的global,mgr配置文件
# Author:piao
# E-mail:qingang@sina.com
'''
import os
import logging
import datetime
import shutil
import config
import exportfile

def main(): 
	logger = logging.getLogger("config");  
	logger.setLevel(logging.DEBUG);
	try:
		os.curdir
		if not os.path.exists('./log'):
			os.mkdir('./log');
		if not os.path.exists('./conf/bak'):
			os.mkdir('./conf/bak');
	except:
		None;
	fh = logging.FileHandler("./log/config.log", mode='a');
	fh.setLevel(logging.DEBUG);	
	formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s');
	fh.setFormatter(formatter);
	logger.addHandler(fh);

	logger.info("开始生成global,mgr参数配置...");
	
	nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


	#一、GetConfig
	(src_os,src_dbtype,src_host,src_port,src_db,src_user,src_pwd,tgt_os,tgt_dbtype,tgt_host,tgt_port,tgt_db,tgt_user,tgt_pwd,deploy_path,dirdef_path,dirprm_source,dirprm_target,trailpath) = config.GetConfigdb(logger);
	(defgen_table,map_table,trandata_table,truncate_table,trail,trailname) = config.GetConfigGroup(logger);
	logger.info(trailname);
	
	#--序列名
	et = 'e' + trail[0]
	rt = 'r' + trail[0]

	#--创建目录
	if not os.path.exists(deploy_path):
		os.makedirs(deploy_path);
	if not os.path.exists(dirprm_source):
		os.makedirs(dirprm_source);
	if not os.path.exists(dirprm_target):
		os.makedirs(dirprm_target);
	if not os.path.exists(dirdef_path):
		os.makedirs(dirdef_path);
			

	#二、生成prm信息
	globals = ''
	globals = globals + '-- globals' + '\n'
	globals = globals + '-- ' + nowTime + '\n'

	#-- 1.src_globals
	src_globals = globals
	if src_os == 'windows':
		src_globals = src_globals + 'MGRSERVNAME GGSMGR' + '\n'
	print (src_globals);

	#-- 2.tgt_globals
	tgt_globals = globals
	if tgt_os == 'windows':
		tgt_globals = tgt_globals + 'MGRSERVNAME GGSMGR' + '\n'
	tgt_globals = tgt_globals + 'ggschema ggadmin' + '\n'
	tgt_globals = tgt_globals + 'checkpointtable ggadmin.chkpt' + '\n'
	print (tgt_globals);
	
	#-- 3.src_mgr
	src_mgr = ''
	src_mgr = src_mgr + '-- mgr' + '\n'
	src_mgr = src_mgr + '-- ' + nowTime + '\n'
	src_mgr = src_mgr + 'PORT ' + src_port + '\n'
	src_mgr = src_mgr + 'DYNAMICPORTLIST 7840-7850' + '\n'
	src_mgr = src_mgr + 'LAGREPORTHOURS 1' + '\n'
	src_mgr = src_mgr + 'LAGINFOMINUTES 30' + '\n'
	src_mgr = src_mgr + 'LAGCRITICALMINUTES 45' + '\n'
	src_mgr = src_mgr + 'AUTOSTART extract *' + '\n'
	src_mgr = src_mgr + 'AUTORESTART extract *,retries 5,waitminutes 3,resetminutes 60' + '\n'
	src_mgr = src_mgr + 'PURGEOLDEXTRACTS ./dirdat/' + trailpath + '/e*,usecheckpoints, minkeepdays 3' + '\n'
	print (src_mgr);
	
	#-- 4.tgt_mgr
	tgt_mgr = ''
	tgt_mgr = tgt_mgr + '-- mgr' + '\n'
	tgt_mgr = tgt_mgr + '-- ' + nowTime + '\n'
	tgt_mgr = tgt_mgr + 'PORT ' + tgt_port + '\n'
	tgt_mgr = tgt_mgr + 'DYNAMICPORTLIST 7840-7850' + '\n'
	tgt_mgr = tgt_mgr + 'LAGREPORTHOURS 1' + '\n'
	tgt_mgr = tgt_mgr + 'LAGINFOMINUTES 30' + '\n'
	tgt_mgr = tgt_mgr + 'LAGCRITICALMINUTES 45' + '\n'
	tgt_mgr = tgt_mgr + 'AUTOSTART replicat *' + '\n'
	tgt_mgr = tgt_mgr + 'AUTORESTART replicat *,retries 5,waitminutes 3,resetminutes 60' + '\n'
	tgt_mgr = tgt_mgr + 'PURGEOLDEXTRACTS ./dirdat/' + trailpath + '/r*,usecheckpoints, minkeepdays 3' + '\n'
	tgt_mgr = tgt_mgr + 'ACCESSRULE, PROG *, IPADDR ' + src_host + ', ALLOW' + '\n'
	print (tgt_mgr);
	
	#-- 5.生成实施配置命令
	install_file = 'deploy.sql'
	install = '' 
	install = install + '-- ogg简要实施步骤及命令' + '\n'
	install = install + '-- ' + nowTime + '\n'
	install = install + '-- ' + src_dbtype + '2' + tgt_dbtype + '\n'
	install = install + '-- 根据需要自行调整参数！' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 一、复制参数配置文件到对应目录 shell>' + '\n'
	install = install + 'scp ./dirprm_source/globals.prm oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_source/mgr.prm oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'

	install = install + 'scp ./dirprm_target/globals.prm oracle@' + tgt_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_target/mgr.prm oracle@' + tgt_host + ':${GG_HOME}/dirprm/' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 二、启动管理进程' + '\n'
	install = install + '-- 1.源端启动管理进程 ggsci>' + '\n'
	install = install + 'START mgr' + '\n' + '\n'

	install = install + '-- 2.目标端启动管理进程 ggsci>' + '\n'
	install = install + 'START mgr' + '\n' + '\n'
	print(install)
	
	#三.导出配置文件
	exportfile.ExportFile(dirprm_source, 'globals.prm', src_globals)
	exportfile.ExportFile(dirprm_source, 'mgr.prm', src_mgr)

	exportfile.ExportFile(dirprm_target, 'globals.prm', tgt_globals)
	exportfile.ExportFile(dirprm_target, 'mgr.prm', tgt_mgr)

	exportfile.ExportFile(deploy_path, install_file, install)
		
	logger.info("配置成功完成!");

if __name__ == "__main__":
    main(); 
