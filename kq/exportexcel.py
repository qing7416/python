# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from xlwt import *

#MASTER_COLS = ['rowid', 'type','name','tbl_name', 'rootpage','sql']
def sqlite_get_col_names(cur, table):
  query = 'select * from %s' % table
  cur.execute(query)
  return [tuple[0] for tuple in cur.description]
def sqlite_query(cur, table, col = '*', where = ''):
  if where != '':
    query = 'select %s from %s where %s' % (col, table, where)
  else:
    query = 'select %s from %s ' % (col, table)
  cur.execute(query)
  return cur.fetchall()
def sqlite_to_workbook(cur, table, workbook):
  ws = workbook.add_sheet(table)
  print ('create table %s.' % table)
  for colx, heading in enumerate(sqlite_get_col_names(cur, table)):
      ws.write(0,colx, heading)
  for rowy,row in enumerate(sqlite_query(cur, table)):
    for colx, text in enumerate(row):
      ws.write(rowy+ 1, colx, text)
def main(dbpath):
  xlspath = dbpath[0:dbpath.rfind('.')] + '.xls'
  print ("<%s> --> <%s>"% (dbpath, xlspath))
  db = sqlite.connect(dbpath)
  cur = db.cursor()
  w = Workbook()
  for tbl_name in [row[0] for row in sqlite_query(cur, 'sqlite_master', 'tbl_name', 'type = \'table\'')]:
    sqlite_to_workbook(cur,tbl_name, w)
  cur.close()
  db.close()
  if tbl_name !=[]: w.save(xlspath)

if name == "main":
  # arg == database path
  main(sys.argv[1])
  

