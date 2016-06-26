import _mysql
import MySQLdb
from random import randint
import hashlib
import time
from contextlib import closing
import db_info
import threading 
import multiprocessing
import sys

class Worker:

  def __init__(self, wait=30, numThreads=-1):
    self.wait = wait
    if numThreads < 1:
      cores = multiprocessing.cpu_count()
      print "Setting number of threads to CPU cores: " + str(cores)
      numThreads = cores

    self.numThreads = numThreads
    

  def start(self, function):
    for i in range(self.numThreads):
      thread = WorkerThread('Thread_' + str(i), self.wait, function)
      thread.start()

    while True:
      time.sleep(1)

class WorkerThread (threading.Thread):

  def __init__(self, name, wait, function):
    self.NAME = str(randint(0,999999999))
    threading.Thread.__init__(self)
    self.daemon = True
    self.name = name
    self.wait = wait
    self.function = function
    self.DB = db_info.getConnection()

  def run(self):
    while True:
      try:
        with closing( self.DB.cursor(MySQLdb.cursors.DictCursor) ) as cursor:
          print self.name + ": checking for data"
          # UPDATE ROW
          cursor.execute(self.getProcessingQuery())
          self.DB.commit()

          # SELECT ROW
          cursor.execute(self.getSelectReadyQuery())
          self.processing = cursor.fetchall()

          # PROCESS JOB
          for combination in self.processing:
            print self.name + ": processing data for id: " + str(combination['id'])
            res = self.function(combination)
            # SET RESULT & COMPLETE
            cursor.execute(self.getCompleteQuery(res, combination['id']))
            self.DB.commit()
      except:
        print self.name + ": an error occoured. Reconnecting..."
        print "Unexpected error:", sys.exc_info()[0]
        self.processing = []
        cursor.close()
        self.DB.close()
        time.sleep(1)
        self.DB = db_info.getConnection()

      if len(self.processing) == 0:
        print self.name + ": no data found. Retrying in " + str(self.wait) + "s"
        time.sleep(self.wait)

  def getProcessingQuery(self):
    query = '''UPDATE Input SET '''
    query += '''status = "processing",'''
    query += '''worker = "''' + self.NAME + '''" WHERE status = "ready" LIMIT 1'''
    return query

  def getSelectReadyQuery(self):
    query = '''SELECT * FROM Input WHERE status = "processing" AND worker = "''' + self.NAME + '''"'''
    return query

  def getCompleteQuery(self, res, rowId):
    query = '''UPDATE Input SET '''
    query += '''status = "complete",'''
    for key in res:
      query += str(key) + ''' = "''' + str(res[key]) + '''",''' 
    
    query = query[:len(query)-1]
    query += ''' WHERE id=''' + str(rowId)
    return query
