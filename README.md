# CluJoDEn
##Clusters Job Distribution Engine

Workflow

1 master engine:
  - takes in task data
  - split it up into single jobs
  - publish jobs to common database

2 worker engines:
  - periodically check common db
  - pick jobs from the db
    - mark them as processing
  - execute jobs
  - publish resuts to common db
    - mark the as finished

3 master engine:
  - wait until all jobs are finished
  - gather results
  - merge and show
  
# Getting Started
1. 
