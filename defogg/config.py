# coding:utf-8
import configparser
#import MyConfigParser

def GetConfigdb(logger):
	try:
		db = configparser.ConfigParser()
		#db = MyConfigParser.ConfigParser()
		db.read("./conf/configdb.ini")
		
		src_os = db.get("extract", "os")
		src_dbtype = db.get("extract", "dbtype")
		src_host = db.get("extract", "host")
		src_port = db.get("extract", "mgrport")
		src_db = db.get("extract", "db")
		src_user = db.get("extract", "username")
		src_pwd = db.get("extract", "password")

		tgt_os = db.get("replicat", "os")
		tgt_dbtype = db.get("replicat", "dbtype")		
		tgt_host = db.get("replicat", "host")
		tgt_port = db.get("replicat", "mgrport")
		tgt_db = db.get("replicat", "db")
		tgt_user = db.get("replicat", "username")
		tgt_pwd = db.get("replicat", "password")

		deploy_path = db.get("path", "deploy_path")
		dirdef_path = db.get("path", "dirdef_path")
		dirprm_source = db.get("path", "dirprm_source")
		dirprm_target = db.get("path", "dirprm_target")
		
		if src_dbtype.lower() == 'mssql':
			trailpath = 'ms'
		elif src_dbtype.lower() == 'oracle':
			trailpath = 'or'
		elif src_dbtype.lower() == 'postgresql':
			trailpath = 'pg'
		else:
			trailpath = 'xx'
	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (src_os,src_dbtype,src_host,src_port,src_db,src_user,src_pwd,tgt_os,tgt_dbtype,tgt_host,tgt_port,tgt_db,tgt_user,tgt_pwd,deploy_path,dirdef_path,dirprm_source,dirprm_target,trailpath);
	

def GetConfigGroup(logger):
	try:
		ogg = configparser.ConfigParser()
		ogg.read("./conf/configgroup.ini")

		trail = ogg.get("tablegroup", "trail")
		trailname = ogg.get("tablegroup", "trailname")
		o1 = ogg.options("tablemap")

		defgen_table = ''
		map_table = ''
		trandata_table = ''
		truncate_table = ''
		for x in o1:
			#--print(x)
			defgen_table = defgen_table + 'TABLE ' + x + ';' + '\n'
			map_table = map_table + 'MAP ' + x + ', TARGET ' + ogg.get("tablemap", x) + ';' + '\n'
			trandata_table = trandata_table + 'ADD TRANDATA ' + x + '\n'
			truncate_table = truncate_table + 'TRUNCATE TABLE ' + ogg.get("tablemap", x) + ';' + '\n'
	except:
		logger.error("读取配置文件出错!");
		raise Exception("");
	return (defgen_table,map_table,trandata_table,truncate_table,trail,trailname);
	