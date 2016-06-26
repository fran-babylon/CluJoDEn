import MySQLdb
from contextlib import closing
import db_info

class Master:

  def __init__(self):
    self.DB = db_info.getConnection()

  def start(self):
    combination = [0] * len(self.params)
    self.combinations(0, combination)

  def combinations(self, i, combination):
    if i == len(self.params):
      print combination
      with closing( self.DB.cursor(MySQLdb.cursors.DictCursor) ) as cursor:
        query = self.getTableQuery(combination)
        cursor.execute(query)
        self.DB.commit()
      return

    for p in self.params[i]:
      combination[i] = p
      self.combinations(i+1, combination)

  
  def getTableQuery(self, combination):
    query = '''INSERT INTO Input SET '''
    for i in range(len(combination)):
      query += self.inputTableParams[i].keys()[0] + ''' = "''' + str(combination[i]) + '''", '''
    query += '''status = "ready"'''
    return query

  def setInputParams(self, params):
    self.params = params

  def cleanInputTable(self):
   self.DB.query( '''DELETE FROM Input''' )

  def createTable(self, inputTableParams):
    self.inputTableParams = inputTableParams
    with closing( self.DB.cursor(MySQLdb.cursors.DictCursor) ) as cursor:
      cursor.execute( '''DROP TABLE IF EXISTS Input''' )
      self.DB.commit()
      cursor.execute( self.getTableSQL("Input", inputTableParams) )
      self.DB.commit()
    print "Table Input created"

  def getTableSQL(self, table, params):
    query = '''
      CREATE TABLE ''' + table + '''
      (
        id INT PRIMARY KEY AUTO_INCREMENT,
      '''
    for param in params:
      key = param.keys()[0]
      val = param[key]
      query += str(key) + ' ' + str(val) + ','
        
    query += '''status varchar(256),'''
    query += '''worker varchar(256)'''
    query += '''); '''
    return query
