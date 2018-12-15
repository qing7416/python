#encoding=UTF-8

import readexcel
import dboper

if __name__ == '__main__':
    #从EXCEL读入到sqlite
    readexcel.read_excel()
    
    #查看考勤数据
    dboper.select()
    
    #导出考勤报告
    #exportexcel.export_excel()