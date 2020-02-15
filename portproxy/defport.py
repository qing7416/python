# coding=utf-8
'''
# Automatically generate port forward\proxy script file
# 2020-02-14 09:00:00
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
	(sshserver) = config.GetConfigsshserver(logger);
	(appserver) = config.GetConfigappserver(logger);
	(portproxy) = config.GetConfigportproxy(logger);
	
	#print(sshserver)
	#print(appserver)
	#print(portproxy)
	logger.info("read config");

	#二、生成cmd脚本(按应用服务器\端口映射循环)
	#--应用服务器
	prev_sshclientip = ''
	filecontentssh = '::ssh' + '\r\n' + '::' + startTime
	filecontentnetsh = '::netsh for windows' + '\r\n' + '::' + startTime
	for x in appserver:
		#print(x)
		appserverip=list(x.keys())[0]
		srvinfo=list(x.values())[0]
		sshclientip=(srvinfo['sshclientip'])		
		sshserveruser=(srvinfo['sshserveruser'])
		sshserverip=(srvinfo['sshserverip'])
		
		#--端口映射（目标端口:源端口），如果没有配置，则监听与服务端口相同
		s=sshserverip.split(':')
		if len(s)==1:
			sshserverip = s[0]
			sshserverport = "22"
		else:
			sshserverip = s[0]
			sshserverport = s[1]

		#print(appserverip)
		#print('%s,%s,%s,%s,%s   ' %(appserverip,sshclientip,sshserveruser,sshserverip,sshserverport))

		if prev_sshclientip != sshclientip:
			filecontentssh = filecontentssh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'
			filecontentnetsh = filecontentnetsh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'

		#--查找该应用服务器的端口映射并生成脚本
		ssh=''
		netsh=''
		for x in portproxy:
			#print(x)
			#print(list(x.keys())[0])
			if appserverip==list(x.keys())[0]:
				appserverPortMapList=list(x.values())[0]
				#print(appserverPortMapList) 
				for x in appserverPortMapList:
					appserverPortMap=x
					#print('%s,%s,%s,%s,%s,%s   ' %(sshclientip,appserverip,appserverPortMap,sshserveruser,sshserverip,sshserverport))
					
					#--端口映射（目标端口:源端口），如果没有配置，则监听与服务端口相同
					s=appserverPortMap.split(':')
					if len(s)==1:
						listenport = s[0]
						appserverport = s[0]
					else:
						listenport = s[0]
						appserverport = s[1]
					
					#--生成bat命令
					if sshserverport == "22":
						ssh = ('ssh -L %s:%s:%s:%s %s@%s' %(sshclientip,listenport,appserverip,appserverport,sshserveruser,sshserverip))
					else:
						ssh = ('ssh -L %s:%s:%s:%s %s@%s -p%s' %(sshclientip,listenport,appserverip,appserverport,sshserveruser,sshserverip,sshserverport))
					netsh = ('netsh interface portproxy add v4tov4 listenaddress=* listenport=%s connectaddress=%s connectport=%s protocol=tcp' %(listenport,appserverip,appserverport))
					#print(ssh)	
					#print(netsh)

					filecontentssh = filecontentssh + '\r\n' + ssh
					filecontentnetsh = filecontentnetsh + '\r\n' + netsh
		
		#--记录ssh客户端，方便标记
		prev_sshclientip = sshclientip
		
		#--添加分隔符
		#filecontentssh = filecontentssh + '\r\n'
		#filecontentnetsh = filecontentnetsh + '\r\n'


	#三.导出命令文件
	filecontentssh = filecontentssh + '\r\n' + '\r\n'
	filecontentnetsh = filecontentnetsh + '\r\n' + '\r\n'
	print(filecontentssh)	
	print(filecontentnetsh)
		
	exportfile.ExportFile('./start', 'ssh.bat', filecontentssh)
	exportfile.ExportFile('./start', 'netsh.bat', filecontentnetsh)
	
	#
	endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(endTime)
	logger.info("配置成功完成!");

if __name__ == "__main__":
    main(); 
