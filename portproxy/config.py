# coding:utf-8
import configparser
import os
import MyConfigParser

def GetConfigsshserver(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")

		o1 = config.options("sshserver")
		sshserver = []
		for x in o1:
			sshservercode=[]
			sshservercode.append(x)

			sshitem=['sshserveruser','sshserverinfo']
			sshinfo=config.get("sshserver", x).split(',')

			sshserverinfo=[]
			sshserverinfo.append(dict(zip(sshitem,sshinfo)))

			sshserver.append(dict(zip(sshservercode,sshserverinfo)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (sshserver);

def GetConfigappserver(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")

		o1 = config.options("appserver")
		appserver = []
		for x in o1:
			connectinfo=[]
			connectinfo.append(x)

			appitem=['appserverip','portproxymaplist','sshservercode']
			appinfo=config.get("appserver", x).split(',')

			serverinfo=[]
			serverinfo.append(dict(zip(appitem,appinfo)))

			appserver.append(dict(zip(connectinfo,serverinfo)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (appserver);

def GetConfigportproxy(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")

		o1 = config.options("portproxy")
		#print(config.options("portproxy"))
		portproxy = []
		for x in o1:
			serverip=[]
			serverip.append(x)

			portproxymaplist=[]
			portproxymaplist.append(config.get("portproxy", x).split(','))

			portproxy.append(dict(zip(serverip,portproxymaplist)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (portproxy);

def writeConf(a,b,logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")
		config.set("portproxy", a, b)
		with open('./conf/config.ini', "w") as f:
			config.write(f)
	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return ('Write finished!');