#!/usr/bin/env python

from Master import *

master = Master()

master.createTable(
    [
      {'key1' : 'varchar(256)'},
      {'key2' : 'int'},
      {'key3' : 'varchar(1)'},
      {'key4' : 'int'},
      {'res' : 'int'}
    ]
)

params = [
  ['a','b','c','d'],
  [1,2,3,4],
  ['x','y','z'],
  [10,20,30,40]
]
master.setInputParams(params)
master.start()
