# coding=utf-8
'''
# Automatically generate oracle goldengate configuration file
# python3.6
# 2017-03-10 16:16:32
# 2018-10-19 16:44
# 2018-11-08 12:20 生成“简要实施步骤及命令”文件
# 2018-11-21 11:47 自动创建目录，按trail备份配置
# 2018-12-26 15:48 优化replicat配置
# ogg文件形如:ed000*,rd000*
# ogg进程形如:einit_ed,rinit_ed,ems_or04,pms_or04,rms_or04
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

	logger.info("开始生成进程组配置...");
	
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
	#-- 1.defgen
	dirdef_file = 'dbo.' + et + '.def'
	defgen_name = 'defgentable_' + et
	defgen_file = defgen_name + '.prm'
	defgen = ''
	defgen = defgen + '-- 表定义\n'
	defgen = defgen + '-- ' + nowTime + '\n'
	defgen = defgen + 'DEFSFILE ./dirdef/' + dirdef_file + '\n'
	defgen = defgen + 'SOURCEDB ' + src_db + ', USERID ' + src_user + ', PASSWORD ' + src_pwd + '\n'
	defgen = defgen + defgen_table + '\n'
	print (defgen);

	#-- 2.einit
	einit_name = 'einit_' + et
	rinit_name = 'rinit_' + et
	einit_file = einit_name + '.prm'
	einit = ''
	einit = einit + '-- 初始化抽取(直接推送)\n'
	einit = einit + '-- ' + nowTime + '\n'
	einit = einit + 'EXTRACT ' + einit_name + '\n'
	einit = einit + 'SOURCEDB ' + src_db + ', USERID ' + src_user + ', PASSWORD ' + src_pwd + '\n'
	einit = einit + 'RMTHOST ' + tgt_host + ', MGRPORT ' + tgt_port + '' + '\n'
	einit = einit + 'RMTTASK REPLICAT, GROUP ' + rinit_name + '\n'
	einit = einit + defgen_table + '\n'
	print (einit);

	#-- 3.rinit
	rinit_file = rinit_name + '.prm'
	rinit = ''
	rinit = rinit + '-- 初始化日志应用(自动启动)\n'
	rinit = rinit + '-- ' + nowTime + '\n'
	rinit = rinit + 'REPLICAT ' + rinit_name + '\n'
	rinit = rinit + 'USERID ' + tgt_user + '@' + tgt_db + ', PASSWORD ' + tgt_pwd + '\n'
	rinit = rinit + 'DISCARDFILE ./dirrpt/' + rinit_name + '.dsc, PURGE' + '\n'
	rinit = rinit + 'SOURCEDEFS ./dirdef/' + dirdef_file + '\n'
	rinit = rinit + map_table + '\n'
	print (rinit);

	#-- 4.inext
	inext_name = 'inext_' + et
	inext_file = inext_name + '.prm'
	inext = ''
	inext = inext + '-- 初始化抽取(中间文件)\n'
	inext = inext + '-- ' + nowTime + '\n'
	inext = inext + 'SOURCEISTABLE' + '\n'
	inext = inext + 'SOURCEDB ' + src_db + ', USERID ' + src_user + ', PASSWORD ' + src_pwd + '\n'
	inext = inext + 'RMTHOST ' + tgt_host + ', MGRPORT ' + tgt_port + '\n'
	inext = inext + 'RMTFILE ./dirdat/init/' + et + '\n'
	inext = inext + defgen_table + '\n'
	print (inext);

	#-- 5.inload
	inload_name = 'inload_' + et
	inload_file = inload_name + '.prm'
	inload = ''
	inload = inload + '-- 初始化日志应用(人工启动)\n'
	inload = inload + '-- ' + nowTime + '\n'
	inload = inload + 'SPECIALRUN' + '\n'
	inload = inload + 'END RUNTIME' + '\n'
	inload = inload + 'USERID ' + tgt_user + '@' + tgt_db + ', PASSWORD ' + tgt_pwd + '\n'
	inload = inload + 'EXTFILE ./dirdat/init/' + et + '\n'
	inload = inload + 'SOURCEDEFS ./dirdef/' + dirdef_file + '\n'
	inload = inload + map_table + '\n'
	print (inload);

	#-- 6.ems
	ems_name = 'ems_' + trailname
	ems_file = ems_name + '.prm'
	ems = ''
	ems = ems + '-- 抽取进程\n'
	ems = ems + '-- ' + nowTime + '\n'
	ems = ems + 'EXTRACT ' + ems_name + '\n'
	ems = ems + 'SETENV (NLS_LANG = "SIMPLIFIED CHINESE.ZHS16GBK" )' + '\n'
	ems = ems + 'SOURCEDB ' + src_db + ', USERID ' + src_user + ', PASSWORD ' + src_pwd + '\n'
	ems = ems + 'EXTTRAIL ./dirdat/' + trailpath + '/' + et + '\n'
	ems = ems + '-- GETTRUNCATES' + '\n'
	ems = ems + 'TRANLOGOPTIONS MANAGESECONDARYTRUNCATIONPOINT' + '\n'
	ems = ems + 'REPORT AT 08:00' + '\n'
	ems = ems + 'REPORTCOUNT EVERY 30 MINUTES, RATE' + '\n'
	ems = ems + 'REPORTROLLOVER AT 20:00' + '\n'
	ems = ems + 'DISCARDFILE ./dirrpt/' + ems_name + '.dsc, APPEND, MEGABYTES 1024' + '\n'
	ems = ems + 'DISCARDROLLOVER AT 20:00' + '\n'
	ems = ems + defgen_table + '\n'
	print (ems);

	#-- 7.pms
	pms_name = 'pms_' + trailname
	pms_file = pms_name + '.prm'
	pms = ''
	pms = pms + '-- 传输进程\n'
	pms = pms + '-- ' + nowTime + '\n'
	pms = pms + 'EXTRACT ' + pms_name + '\n'
	pms = pms + 'PASSTHRU' + '\n'
	pms = pms + 'RMTHOST ' + tgt_host + ', MGRPORT ' + tgt_port + ', COMPRESS' + '\n'
	pms = pms + 'RMTTRAIL ./dirdat/' + trailpath + '/' + rt + '\n'
	pms = pms + 'REPORT AT 08:00' + '\n'
	pms = pms + 'REPORTCOUNT EVERY 30 MINUTES, RATE' + '\n'
	pms = pms + 'REPORTROLLOVER AT 20:00' + '\n'
	pms = pms + 'DISCARDFILE ./dirrpt/' + pms_name + '.dsc, APPEND, MEGABYTES 1024' + '\n'
	pms = pms + 'DISCARDROLLOVER AT 20:00' + '\n'
	pms = pms + defgen_table + '\n'
	print (pms);

	#-- 8.rms
	rms_name = 'rms_' + trailname
	rms_file = rms_name + '.prm'
	rms = ''
	rms = rms + '-- 日志应用进程\n'
	rms = rms + '-- ' + nowTime + '\n'
	rms = rms + 'REPLICAT ' + rms_name + '\n'
	rms = rms + 'SETENV (NLS_LANG=AMERICAN_AMERICA.AL32UTF8)' + '\n'
	rms = rms + 'SETENV (ORACLE_SID="pdb1.petrochina.com")' + '\n'
	rms = rms + 'SETENV (ORACLE_HOME="/u01/app/oracle/product/12.2.0/dbhome_1/")' + '\n'
	rms = rms + 'USERID ' + tgt_user + '@' + tgt_db + ', PASSWORD ' + tgt_pwd + '\n'
	rms = rms + 'SOURCEDEFS ./dirdef/' + dirdef_file + '\n'
	rms = rms + 'REPORT AT 08:00' + '\n'
	rms = rms + 'REPORTCOUNT EVERY 30 MINUTES, RATE' + '\n'
	rms = rms + 'REPORTROLLOVER AT 20:00' + '\n'
	rms = rms + '-- HANDLECOLLISIONS' + '\n'
	rms = rms + 'REPERROR DEFAULT, ABEND' + '\n'
	rms = rms + 'REPERROR -1, IGNORE' + '\n'
	rms = rms + 'DISCARDFILE ./dirrpt/' + rms_name + '.dsc, APPEND, MEGABYTES 1024' + '\n'
	rms = rms + 'DISCARDROLLOVER AT 20:00' + '\n'
	rms = rms + map_table + '\n'
	print (rms);

	#-- 9.生成实施配置命令
	install_file = 'deploy_' + trailname + '.sql'
	install = '' 
	install = install + '-- ogg进程组简要实施步骤及命令' + '\n'
	install = install + '-- ' + nowTime + '\n'
	install = install + '-- ' + src_dbtype + '2' + tgt_dbtype + '\n'
	install = install + '-- trail:' + et + '\n'
	install = install + '-- trailname:' + trailname + '\n'
	install = install + '-- 根据需要自行调整参数！' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 一、生成表定义' + '\n'
	install = install + '-- 1.源端生成表定义文件 cmd\shell>' + '\n'
	install = install + 'defgen PARAMFILE ./dirprm/' + defgen_file + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 二、复制上述（5+3+1*2=10个）配置文件到对应目录 shell>' + '\n'
	install = install + 'scp ./dirprm_source/' + defgen_file + ' oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_source/' + einit_file + ' oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_source/' + inext_file + ' oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_source/' + ems_file + ' oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_source/' + pms_file + ' oracle@' + src_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + '\n'
	install = install + 'scp ./dirprm_target/' + rinit_file + ' oracle@' + tgt_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_target/' + inload_file + ' oracle@' + tgt_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + 'scp ./dirprm_target/' + rms_file + ' oracle@' + tgt_host + ':${GG_HOME}/dirprm/' + '\n'
	install = install + '\n'
	install = install + 'scp ./dirdef/' + dirdef_file + ' oracle@' + src_host + ':${GG_HOME}/dirdef/' + '\n'
	install = install + 'scp ./dirdef/' + dirdef_file + ' oracle@' + tgt_host + ':${GG_HOME}/dirdef/' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 三、初始化抽取(选择1个方案即可)' + '\n'
	install = install + '-- 初始化目标表(选用)' + '\n'
	install = install + '/*' + '\n'
	install = install + truncate_table
	install = install + '*/' + '\n' + '\n'

	install = install + '-- （一）直接初始化(推荐)' + '\n'
	install = install + '-- 1.源端增加EXTRACT初始化进程组 ggsci>' + '\n'
	install = install + 'ADD EXTRACT ' + einit_name + ', SOURCEISTABLE' + '\n' + '\n'

	install = install + '-- 2.目标端增加REPLICAT初始化进程组 ggsci>' + '\n'
	install = install + 'ADD REPLICAT ' + rinit_name + ', SPECIALRUN' + '\n' + '\n'

	install = install + '-- 3.源端启动初始化 ggsci>' + '\n'
	install = install + 'START EXTRACT ' + einit_name + '\n' + '\n'

	install = install + '-- 初始化监控 ggsci>' + '\n'
	install = install + 'view report ' + einit_name + '\n'
	install = install + 'view report ' + rinit_name + '\n' + '\n'

	install = install + '-- （二）间接初始化(中间文件)' + '\n'
	install = install + '-- 1.源端提取初始化数据(生成中间文件并上传到目标端) cmd\shell>' + '\n'
	install = install + 'extract PARAMFILE ./dirprm/' + inext_file + ' REPORTFILE ./dirrpt/' + inext_name +'.rpt' + '\n' + '\n'

	install = install + '-- 2.目标端检查中间文件' + '\n'
	install = install + 'll ${GG_HOME}/dirdat/init/' + '\n' + '\n'

	install = install + '-- 3.目标端应用初始化数据 cmd\shell>' + '\n'
	install = install + 'replicat PARAMFILE ./dirprm/' + inload_file + ' REPORTFILE ./dirrpt/' + inload_name +'.rpt' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 四、配置同步抽取' + '\n'
	install = install + '-- 1.源端登录 cmd\shell>' + '\n'
	install = install + 'DBLOGIN SOURCEDB ' + src_db + ', USERID ' + src_user + ', PASSWORD ' + src_pwd + '\n' + '\n'

	install = install + '-- 2.添加抽取事务表 ggsci>' + '\n'
	install = install + trandata_table + '\n'

	install = install + '-- 3.添加抽取和传输进程 ggsci>' + '\n'
	install = install + 'ADD EXTRACT ' + ems_name + ', tranlog, BEGIN NOW' + '\n'
	install = install + 'ADD EXTTRAIL ./dirdat/' + trailpath + '/' + et + ', EXTRACT ' + ems_name + ', MEGABYTES 128' + '\n' + '\n'

	install = install + 'ADD EXTRACT ' + pms_name + ', EXTTRAILSOURCE ./dirdat/' + trailpath + '/' + et + ', BEGIN NOW' + '\n'
	install = install + 'ADD RMTTRAIL ./dirdat/' + trailpath + '/' + rt + ', EXTRACT ' + pms_name + ', MEGABYTES 128' + '\n' + '\n'

	install = install + '-- 4.目标端登录 cmd\shell>' + '\n'
	install = install + 'DBLOGIN USERID ' + tgt_user + '@' + tgt_db + ', PASSWORD ' + tgt_pwd + '\n' + '\n'

	install = install + '-- 5.添加日志应用进程 ggsci>' + '\n'
	install = install + 'ADD REPLICAT ' + rms_name + ', EXTTRAIL ./dirdat/' + trailpath + '/' + rt + ', CHECKPOINTTABLE ggadmin.chkpt' + '\n' + '\n'


	install = install + '\n'
	install = install + '-- 五、启动同步进程' + '\n'
	install = install + '-- 1.源端启动抽取和传输进程 ggsci>' + '\n'
	install = install + 'START EXTRACT ' + ems_name + '' + '\n'
	install = install + 'START EXTRACT ' + pms_name + '' + '\n' + '\n'

	install = install + '-- 2.目标端启动日志应用进程 ggsci>' + '\n'
	install = install + 'START REPLICAT ' + rms_name + '\n' + '\n'
	print(install)


	#三.导出配置文件
	exportfile.ExportFile(dirprm_source, defgen_file, defgen)

	exportfile.ExportFile(dirprm_source, einit_file, einit)
	exportfile.ExportFile(dirprm_target, rinit_file, rinit)
	exportfile.ExportFile(dirprm_source, inext_file, inext)
	exportfile.ExportFile(dirprm_target, inload_file, inload)

	exportfile.ExportFile(dirprm_source, ems_file, ems)
	exportfile.ExportFile(dirprm_source, pms_file, pms)
	exportfile.ExportFile(dirprm_target, rms_file, rms)

	exportfile.ExportFile(deploy_path, install_file, install)

	
	#四、备份配置
	shutil.copy("./conf/configdb.ini","./conf/bak/" + et + "_configdb.ini")
	shutil.copy("./conf/configgroup.ini","./conf/bak/" + et + "_configgroup.ini")
	
	logger.info("进程组配置成功完成!");

if __name__ == "__main__":
    main(); 
