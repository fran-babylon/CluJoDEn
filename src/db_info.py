#!/usr/bin/env python
import MySQLdb

def getConnection():
  return MySQLdb.connect(
    host='localhost',
    user='user',
    passwd='pass',
    db='clujoden'
  )


