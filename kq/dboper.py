# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import dbconn

def insert(id,dept,name,datamonth,data,ncols):
    #print (data)    
    conn = dbconn.connection
    #print ("Opened database successfully");
    c = conn.cursor()

    for i in list(range(1,ncols)):        
        value=(data[i].split('\n'))
        #print(value,len(value))
        dateValue = datamonth + '-'  + ('00' + str(i))[-2:]
        dateValue = dateValue.strip()

        if len(value) >= 2:           
            #print(value[0],value[-1])
            #print(len(value[0].strip()),len(value[-1].strip()))   
            if len(value[0].strip()) > 0:
                sql = "INSERT INTO kq (id,dept,name,kqdate,kqtime) VALUES (" + id + ",'" + dept + "', '" + name + "', '" + dateValue + "', '" + value[0].strip() + "');"  
                #print(sql)             
                c.execute(sql);
            if len(value[-1].strip()) > 0:
                sql = "INSERT INTO kq (id,dept,name,kqdate,kqtime) VALUES (" + id + ",'" + dept + "', '" + name + "', '" + dateValue + "', '"  + value[-1].strip() + "');"
                #print(sql)                
                c.execute(sql);      
    conn.commit()
    #print ("Records created successfully");
    
def select():
    conn = dbconn.connection
    #print ("Opened database successfully");
    c = conn.cursor()
    
    sql = "select name,kqdate, case when min(kqtime) <> max(kqtime) then min(kqtime) when min(kqtime) = max(kqtime) and min(kqtime) <= '12：00' then min(kqtime) else null end first_kqtime, case when min(kqtime) <> max(kqtime) then max(kqtime) when min(kqtime) = max(kqtime) and min(kqtime) >= '12：00' then min(kqtime) else null end last_kqtime, case when max(kqtime) >= '18:30' then max(kqtime) else null end Overtime1,case when max(kqtime) >= '20:00' then max(kqtime) else null end Overtime2 from kq group by name,kqdate"
    #sql = "SELECT id,Name,kqdate,kqtime from kq2"
    cursor = c.execute(sql)    
    for row in cursor:
        '''
        print ("id = ", row[0])
        print ("Name = ", row[1])
        print ("kqdate = ", row[2])
        print ("kqdate = ", row[3])
        print ("kqdate = ", row[4])
        print ("kqtime = ", row[5], "\n")  
        '''
        print (row[0],"\t",row[1],"\t",row[1],"\t",row[2],"\t",row[3],"\t",row[4],"\t",row[5])
    conn.commit()
    #print ("Operation done successfully");
    conn.close()



