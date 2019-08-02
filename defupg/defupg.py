# coding=utf-8
'''
# Automatically generate mssql upgrade script file
# 2019-07-07 15:00:00
'''
import os
import logging
import datetime
import config
import exportfile

def main(): 
	logger = logging.getLogger("config");  
	logger.setLevel(logging.DEBUG);
	try:
		os.curdir
		os.mkdir('./log');
	except:
		None;
	try:
		os.curdir
		os.mkdir('./start');
	except:
		None;
	fh = logging.FileHandler("./log/config.log", mode='a');
	fh.setLevel(logging.DEBUG);	
	formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s');
	fh.setFormatter(formatter);
	logger.addHandler(fh);

	logger.info("开始配置...");
	
	startTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(startTime)

	#一、GetConfig
	(instance) = config.GetConfigInstance(logger);
	(database) = config.GetConfigDatabase(logger);
	
	#print(instance)
	#print(database)
	logger.info("read config");

	#二、生成cmd脚本(按服务器实例\数据库循环)
	#--实例
	startfile=''
	for x in instance:
		#print(x)
		srvcode=list(x.keys())[0]
		srvinfo=list(x.values())[0]
		ip=(srvinfo['ip'])		
		port=(srvinfo['port'])
		user=(srvinfo['user'])
		pwd=(srvinfo['pwd'])
		
		filecontent=''
		#--查找该实例的数据库并生成脚本
		for x in database:
			#print(x)
			if srvcode==list(x.keys())[0]:
				srvdb=list(x.values())[0]
				#print(srvdb) 
				for x in srvdb:
					dbname=x
					#print('sqlcmd -I -S %s,%s    -U %s    -P %s    -d %s     -i .\bos_oilpump\stat_bos_oilpumpsum.sql' %(ip,port,user,pwd,dbname))
					filecontent = filecontent + ('sqlcmd -I -S %s,%s    -U %s    -P %s    -d %s     -i .\\bos_oilpump\\stat_bos_oilpumpsum.sql\n' %(ip,port,user,pwd,dbname))
		filecontent = filecontent + 'exit\n'
		#print(filecontent)		
		#--按服务器导出命令文件
		filename=srvcode + '.bat'
		exportfile.ExportFile('.\start', filename, filecontent)

		#--按服务器生成start执行命令
		startfile = startfile + (':%s \n' %(srvcode))
		startfile = startfile + ('echo.\n')
		startfile = startfile + ('echo %s \n' %(srvcode))
		startfile = startfile + ('start %s > .\log\%s.log\n\n' %(filename,srvcode))

	#三.导出start命令文件
	exportfile.ExportFile('.\start', 'start.bat', startfile)


	#
	endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(endTime)
	logger.info("配置成功完成!");

if __name__ == "__main__":
    main(); 
