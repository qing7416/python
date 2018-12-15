# -*- coding: utf-8 -*-

import datetime
import xlrd
import dboper
import dbconn

def read_excel():
    startTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #1.打开文件
    workbook = xlrd.open_workbook(r'.\data\员工刷卡记录表.xls')

    #2.获取所有sheet 
    print (workbook.sheet_names()) 
    # [u'员工刷卡记录表']
    sheetname = workbook.sheet_names()[0]
    #print (sheetname);
    #print (('dsfd '+d).strip());   return
    
    #3.根据sheet索引或者名称获取sheet内容
    #sheetdata = workbook.sheet_by_index(0) # sheet索引从0开始
    #print (sheetdata);
    sheetdata = workbook.sheet_by_name(sheetname)
    #print (sheetdata);
    
    #4.sheet的名称，行数，列数
    print (sheetdata.name,sheetdata.nrows,sheetdata.ncols)
    nrows=sheetdata.nrows
    ncols=sheetdata.ncols
    
    #5.获取考勤日期
    kqdate=sheetdata.row_values(2)    
    value=(kqdate[25].split('～'))
    startdate=value[0][11:15] + '-' + value[0][5:10]
    enddate=value[1][6:10] + '-' + value[1][0:5]
    print('考勤日期：',startdate,'~',enddate)
    datamonth=startdate[0:7]  


    #print(datamonth)

    #6.获取考勤记录
    #删除目标表考勤记录
    conn = dbconn.connection
    conn.execute('delete from kq') 
    conn.commit() 
    
    #从第4行开始（索引值，实际数据第5行）
    #大部分人员考勤信息有3行（人员信息，考勤日期ID，考勤信息），个别人员考勤信息多出1行
    rows=4
    while rows <= nrows - 3:
        #print(rows)
        PersonKqInfo = sheetdata.row_values(rows)
        checkInfo = u'工号：' in PersonKqInfo
        if checkInfo is True :
            #print(checkInfo)
            PersonKqData = sheetdata.row_values(rows+2)
            #cols = sheet2.col_values(1)
            #print (PersonKqInfo)
            #print (PersonKqData)
            id = PersonKqInfo[3]
            dept = PersonKqInfo[18]
            name = PersonKqInfo[11]
            dboper.insert(id,dept,name,datamonth,PersonKqData,ncols)

        #--处理考dbconn录多出1行的
        if rows <= nrows - 4:
            PersonKqInfo = sheetdata.row_values(rows+3)
            checkInfo = u'工号：' in PersonKqInfo
            if checkInfo is False :
                PersonKqData = sheetdata.row_values(rows+3)
                #cols = sheet2.col_values(1)
                #print (PersonKqData)
                dboper.insert(id,dept,name,datamonth,PersonKqData,ncols)
                rows=rows+1
        rows=rows+3
        #print(rows)
    endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('处理时间：',startTime,'~',endTime)

 
