#!/usr/bin/env python

from Worker import Worker 
from time import sleep

def function(inputs):
  sleep(3)
  return {
    "res": inputs['key2'] * 2
  }

worker = Worker(5,)


worker.start(function)

