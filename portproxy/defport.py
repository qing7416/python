# coding = utf-8
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
	fh = logging.FileHandler("./log/config.log", mode = 'a');
	fh.setLevel(logging.DEBUG);	
	formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s');
	fh.setFormatter(formatter);
	logger.addHandler(fh);

	logger.info("开始配置...");
	
	startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
	filecontentnetsh = '::netsh for windows' + '\r\n'
	filecontentnetsh = filecontentnetsh + '::netsh interface portproxy delete v4tov4 listenport=<port>' + '\r\n' 
	filecontentnetsh = filecontentnetsh + '::' + startTime
	for x in appserver:
		#print(x)
		connectinfo = ""
		serverinfo = ""
		#print(list(x.keys()))
		#print(list(x.values()))

		connectinfo = list(x.keys())[0]
		sshclientip = list(connectinfo.split(','))[0]
		listenip = list(connectinfo.split(','))[1]

		serverinfo = list(x.values())[0]
		appserverip = serverinfo['appserverip']
		portproxymaplist = serverinfo['portproxymaplist']
		sshservercode = serverinfo['sshservercode']
		#print(sshservercode)

		if prev_sshclientip != sshclientip:
			filecontentssh = filecontentssh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'
			filecontentnetsh = filecontentnetsh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'

		#匹配sshserver信息
		for x in sshserver:
			#print(x)
			if sshservercode == list(x.keys())[0]:
				sshserverinfo = list(x.values())[0]
				#print(sshserverinfo['sshserverinfo'])
				sshserveruser = sshserverinfo['sshserveruser']
				sshserverip = sshserverinfo['sshserverinfo']

				#--ssh服务端口映（ip:port），如果没有配置，默认为22
				tmp = sshserverip.split(':')
				#print(tmp)
				sshserverip = tmp[0].strip()
				if len(tmp) == 1:
					sshserverport = "22"
				else:
					sshserverport = tmp[1].strip()
				#print('%s,%s,%s,%s,%s,%s,%S   ' %(sshclientip,listenip,appserverip,portproxymaplist,sshserveruser,sshserverip,sshserverport))

				# --端口拆分
				ssh = ''
				netsh = ''
				portproxymap = list(portproxymaplist.split(':'))
				#print(portproxymap)
				for x in portproxymap:
					#print(x)
					tmp = x.split('@')
					#print(tmp)
					listenport = tmp[0].strip()
					if len(tmp) == 1:
						appserverport = tmp[0].strip()
					else:
						appserverport = tmp[1].strip()
					#print(listenport)


					#--生成bat命令
					if sshserverport == "22":
						ssh = ('ssh -L %s:%s:%s:%s %s@%s' %(listenip,listenport,appserverip,appserverport,sshserveruser,sshserverip))
					else:
						ssh = ('ssh -L %s:%s:%s:%s %s@%s -p%s' %(listenip,listenport,appserverip,appserverport,sshserveruser,sshserverip,sshserverport))
					netsh = ('netsh interface portproxy add v4tov4 listenaddress=%s listenport=%s connectaddress=%s connectport=%s protocol=tcp' %(listenip,listenport,appserverip,appserverport))
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
	endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(endTime)
	logger.info("配置成功完成!");

if __name__ == "__main__":
    main(); 
