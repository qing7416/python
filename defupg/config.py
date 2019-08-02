# coding:utf-8
import configparser
import MyConfigParser

def GetConfigInstance(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/configupg.ini")

		o1 = config.options("instance")
		instance = []
		for x in o1:			
			infoitem=['ip','port','user','pwd']
			info=config.get("instance", x).split(',')		

			srvcode=[]
			srvcode.append(x)			
			srvinfo=[]			
			srvinfo.append(dict(zip(infoitem,info)))

			instance.append(dict(zip(srvcode,srvinfo)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (instance);

def GetConfigDatabase(logger):
	try:
		config = configparser.ConfigParser()
		config.read("./conf/configupg.ini")

		o1 = config.options("database")
		database = []
		for x in o1:
			srvcode=[]
			srvcode.append(x)
			srvdb=[]
			srvdb.append(config.get("database", x).split(','))

			database.append(dict(zip(srvcode,srvdb)))

	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (database);
	