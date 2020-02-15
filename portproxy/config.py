# coding:utf-8
import configparser
import MyConfigParser

def GetConfigsshserver(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")

		o1 = config.options("sshserver")
		sshserver = []
		for x in o1:			
			infoitem=['sshserveruser','sshserverip','sshserverport']
			info=config.get("sshserver", x).split(',')		

			srvcode=[]
			srvcode.append(x)			
			srvinfo=[]			
			srvinfo.append(dict(zip(infoitem,info)))

			sshserver.append(dict(zip(srvcode,srvinfo)))

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
			infoitem=['sshclientip','sshserveruser','sshserverip']
			info=config.get("appserver", x).split(',')		

			srvcode=[]
			srvcode.append(x)			
			srvinfo=[]			
			srvinfo.append(dict(zip(infoitem,info)))

			appserver.append(dict(zip(srvcode,srvinfo)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (appserver);

def GetConfigportproxy(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/config.ini")

		o1 = config.options("portproxy")
		portproxy = []
		for x in o1:
			srvcode=[]
			srvcode.append(x)
			srvdb=[]
			srvdb.append(config.get("portproxy", x).split(','))

			portproxy.append(dict(zip(srvcode,srvdb)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (portproxy);
	
