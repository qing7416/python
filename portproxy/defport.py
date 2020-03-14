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
import re

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
	sshclientip = ''
	sshclientgroup = ''
	listenportgroup = []
	listengrouplist = []
	
	filecontentssh = '::ssh' + '\r\n' + '::' + startTime
	filecontentnetsh = '::netsh for windows' + '\r\n'
	filecontentnetsh = filecontentnetsh + '::netsh interface portproxy delete v4tov4 listenport=<port>' + '\r\n'
	filecontentnetsh = filecontentnetsh + '::' + startTime
	filecontentipports = ''

	#tmp1 = ''
	#tmp2 = ''
	filecontentnetshfirewalld = '::netsh advfirewall firewall rule for windows' + '\r\n'
	filecontentnetshfirewalld = filecontentnetshfirewalld + '::' + startTime

	#--循环解析应用配置
	for x in appserver:
		#print(x)
		connectinfo = ""
		serverinfo = ""
		#print(list(x.keys()))
		#print(list(x.values()))
		prev_sshclientip = sshclientip
		prev_sshclientgroup = sshclientgroup

		connectinfo = list(x.keys())[0]
		sshclientip = list(connectinfo.split(','))[0]
		listenip = list(connectinfo.split(','))[1]

		sshclientgroup = re.sub('[0-9]', '', list(connectinfo.split(','))[2])

		serverinfo = list(x.values())[0]
		appserverip = serverinfo['appserverip']
		portproxymaplist = serverinfo['portproxymaplist']
		sshservercode = serverinfo['sshservercode']
		#print(sshservercode)
		if prev_sshclientip != sshclientip:
			filecontentssh = filecontentssh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'
			filecontentnetsh = filecontentnetsh + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'

		#--匹配sshserver信息
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

		#--端口拆分
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
			#print(0, sshclientip, sshclientgroup,listenport)

			#--生成端口转发\端口代理命令
			if sshserverport == "22":
				ssh = ('ssh -L %s:%s:%s:%s %s@%s' %(listenip,listenport,appserverip,appserverport,sshserveruser,sshserverip))
			else:
				ssh = ('ssh -L %s:%s:%s:%s %s@%s -p%s' %(listenip,listenport,appserverip,appserverport,sshserveruser,sshserverip,sshserverport))
			netsh = ('netsh interface portproxy add v4tov4 listenaddress=%s listenport=%s connectaddress=%s connectport=%s protocol=tcp' %(listenip,listenport,appserverip,appserverport))
			#print(ssh)	
			#print(netsh)
			filecontentssh = filecontentssh + '\r\n' + ssh
			filecontentnetsh = filecontentnetsh + '\r\n' + netsh

			#--生成端口检测列表
			if sshclientip == '192.168.30.13':
				filecontentipports = filecontentipports + '\n' + "172.35.117.16" + ' ' + listenport

			#--端口防火墙分组
			if prev_sshclientgroup != '' and prev_sshclientgroup != sshclientgroup:
				#print(1, prev_sshclientip, prev_sshclientgroup, listenportgroup)
				s = prev_sshclientip + ':' + prev_sshclientgroup + ':' + listenip + ":" + ",".join(listenportgroup)
				listengrouplist.append(s)

				prev_sshclientgroup = sshclientgroup
				listenportgroup = []
			#--添加端口列表
			listenportgroup.append(listenport)

	#三.生成防火墙配置命令，按分组写配置文件
	#--末组端口防火墙（必须加！）
	s = prev_sshclientip + ':' + prev_sshclientgroup + ':' + listenip + ":" + ",".join(listenportgroup)
	listengrouplist.append(s)

	#--解析
	#print(listengrouplist)
	prev_sshclientgroup = ''
	del_netshfirewallrule = ''
	add_netshfirewallrule  = ''
	for x in listengrouplist:
		print(x)
		s = x.split(':')
		sshclientip = s[0]
		sshclientgroup = s[1]
		listenip = s[2]
		listenportgroup = s[3]
		#print(1, prev_sshclientip, prev_sshclientgroup, listenportgroup, sshclientip, sshclientgroup)

		if prev_sshclientip != sshclientip:
			filecontentnetshfirewalld = filecontentnetshfirewalld + '\r\n' + '\r\n' + '::在 ' + sshclientip + ' 上运行'

		#if sshclientip != "":  # in ('192.168.18.128','192.168.30.13'):
		tmp1 = ('netsh advfirewall firewall delete rule name = ".ENJOY_%s" dir = in ' % (sshclientgroup))
		tmp2 = ('netsh advfirewall firewall add rule name=".ENJOY_%s" dir=in action=allow protocol=TCP localport=%s remoteip=%s' % (sshclientgroup, listenportgroup, listenip))

		filecontentnetshfirewalld = filecontentnetshfirewalld + '\r\n' + tmp1
		filecontentnetshfirewalld = filecontentnetshfirewalld + '\r\n' + tmp2

		prev_sshclientip = sshclientip
		prev_sshclientgroup = sshclientgroup

		#--写配置文件
		(portproxy) = config.writeConf(sshclientip + ',' + sshclientgroup,listenportgroup,logger);


	#四.导出命令文件
	filecontentssh = filecontentssh + '\r\n' + '\r\n'
	filecontentnetsh = filecontentnetsh + '\r\n' + '\r\n'
	filecontentnetshfirewalld = filecontentnetshfirewalld + '\r\n' + '\r\n'
	filecontentipports = filecontentipports + '\n'

	#print(filecontentssh)
	#print(filecontentnetsh)
	#print(filecontentnetshfirewalld)

	exportfile.ExportFile('./start', 'ssh.bat', filecontentssh)
	exportfile.ExportFile('./start', 'netsh.bat', filecontentnetsh)
	exportfile.ExportFile('./start', 'netsh_advfirewall.bat', filecontentnetshfirewalld)
	exportfile.ExportFile('./start', 'ip-ports.txt', filecontentipports)

	#
	endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(endTime)
	logger.info("配置成功完成!");


if __name__ == "__main__":
    main(); 
