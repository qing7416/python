### 自动生成ogg部署配置文件
### 适用范围:mssql2oracle(源端SQLSERVER,目标端Oracle)
### 适合有一定ogg部署经验者使用
### python3.6测试通过
### 2018-11-22

1. ogg部署  
    默认在源端部署抽取和传输进程，在目标端部署复制应用进程  
    ogg自行部署，本项目仅自动生成ogg抽取、传输及复制等各步骤之配置文件（包括初始化配置）  

2. 关于 configdb.ini文件配置，请参考配置样例阅读  
	[extract] #抽取\传输（源端）  
	[extract]  
	os=windows		#windows,linux  
	dbtype=Oracle	#源数据库类型 mssql,oracle  
	host=源库IP  
	mgrport=端口号	#默认7809  
	db=源数据库ODBC连接名称	#此处是mssql  
	username=源库用户名  
	password=源库密码  

	[replicat]#复制（目标端）  
	[replicat]  
	os=linux  
	dbtype=oracle	#目标数据库类型  mssql,oracle    
	host=目标库IP  
	mgrport=端口号	#默认7809  
	db==目标库TNS服务名  
	username=目标库用户名  
	password==目标库密码

	[path]#生成配置的存放目录（可使用相对目录或者绝对目录）  
	deploy_path=./ogg/deploy  
	dirdef_path=./ogg/dirdef  
	dirprm_source=./ogg/dirprm_source  
	dirprm_target=./ogg/dirprm_target  

3. 关于 configogg.ini文件配置，请参考配置样例阅读  
   [tablegroup]  
		trail:抽取序列，仅1位字母  
		trailname:非空英文字母数字，建议4位长度  
   [tablegmap]  
		table映射，格式:源schema.源表名=目标schema.目标表名  


4. 目录说明  
   1. 存放ogg简要实施步骤及命令文件的目录  
.\ogg\deploy  

   2. 需要放在ogg源端的配置文件  
.\ogg\dirprm_source  

   3. 需要放在目标端端的配置文件  
.\ogg\dirprm_target  

   4. 需要放在源端和目标端的表定义文件  
.\ogg\dirdef  

5. 使用方法  
   1. 进入工作目录(假设是E:\defoggdemo)  
cd /D E:\defoggdemo  

   2. 修改配置文件（参考样本自行修改）  
./conf/configdb.ini  
./conf/configgroup.ini  

   3. 运行脚本，自动生成ogg的global,mgr配置文件  
cd /D E:\defoggdemo  
.\defogg.py  

   4. 运行脚本，自动生成ogg进程组配置参数（每个进程组分别配置）  
cd /D E:\defoggdemo  
.\defgroup.py  

   5. 检查上述目录文件  
dir .\ogg\deploy\  
dir .\ogg\dirprm_source\  
dir .\ogg\dirprm_target\  

6. 根据实施步骤及命令文件部署ogg（样例）  
.\ogg\deploy\deploy_or03.sql  

