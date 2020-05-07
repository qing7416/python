#coding = utf-8
#get-svninfo
import os

#os.system("svn info https://192.168.0.210:8443/svn/JiaoTongTing/")

def getsvninfo(svnurl):
  #svnurl = "https://192.168.0.210:8443/svn/JiLinChinaPetro/"

  info=os.popen("svn info " + svnurl).read() 
  #print(info)
  
  p1 = info.find('Path:')
  p2 = info.find('URL')
  p3 = info.find('Last Changed Author:')
  p4 = info.find("Last Changed Rev:")
  p5 = info.find("Last Changed Date:")
  p6 = info.find("+0800")

  path = info[p1+6:p2-1]
  author = info[p3+21:p4-1]
  rev = info[p4+18:p5-1]
  date = info[p5+19:p6-1]
  print(path,'\t',author,'\t',rev,'\t',date)


#getsvninfo("https://192.168.0.210:8443/svn/DianZiDiTu/")
getsvninfo("https://192.168.0.210:8443/svn/财务/")
getsvninfo("https://192.168.0.210:8443/svn/StationCollect/")
getsvninfo("https://192.168.0.210:8443/svn/HeiLongJiangFJ/")
getsvninfo("https://192.168.0.210:8443/svn/FileTransfer/")
getsvninfo("https://192.168.0.210:8443/svn/HeiLongJiangChinaPetro/")
getsvninfo("https://192.168.0.210:8443/svn/WindowOpen/")
getsvninfo("https://192.168.0.210:8443/svn/JiangSuBMP3.0/")
getsvninfo("https://192.168.0.210:8443/svn/jifenAPP/")
getsvninfo("https://192.168.0.210:8443/svn/StationUpdate/")
getsvninfo("https://192.168.0.210:8443/svn/HeiLongJiangPetroChina/")
getsvninfo("https://192.168.0.210:8443/svn/DianLiAPP/")
getsvninfo("https://192.168.0.210:8443/svn/Zb/")
getsvninfo("https://192.168.0.210:8443/svn/Chengchao/")
getsvninfo("https://192.168.0.210:8443/svn/Daduhe/")
getsvninfo("https://192.168.0.210:8443/svn/MeiShan/")
getsvninfo("https://192.168.0.210:8443/svn/JiLinChinaPetro/")
getsvninfo("https://192.168.0.210:8443/svn/JiaoTongTing/")
#getsvninfo("https://192.168.0.210:8443/svn/zxgk/")