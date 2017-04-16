#! /usr/bin/env python3 

#import time
import shlex, subprocess
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl import DocType, String, Boolean
import time
from datetime import datetime


class tareasIndex(DocType):
        usuario = String()
        repositorio = String()
        estado = Boolean()

es = Elasticsearch()
requ = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
requ = requ.source(['usuario', 'repositorio', 'estado'])
resp = requ.scan()

for commit in resp:
    if commit.estado==False:
        print("Empezando a ejecutar...")
        req = tareasIndex.get(id=commit.usuario+"-"+commit.repositorio, using=es, index='tareas')
        req.update(using=es, inicioEjecucion=datetime.now())
        repo_url = 'https://github.com/'+commit.usuario+'/'+commit.repositorio+'.git'
        cmd = "p2o.py --enrich --index git_raw --index-enrich git \-e http://localhost:9200 --no_inc --debug \git "+repo_url+""
        cmd = shlex.split(cmd)
        p1 = subprocess.Popen(cmd)
#         
        cmd3 = "kidash.py --elastic_url-enrich http://locahost:9200 \--import /tmp/git-dashboard.json"
        cmd3 = shlex.split(cmd3)
        p2 = subprocess.Popen(cmd3)
        p1.wait()
        p2.wait()
        #req = tareasIndex.get(id=commit.usuario+"-"+commit.repositorio, using=es, index='tareas')
        req.update(using=es, estado=True, finEjecucion=datetime.now())
    else:
        print("Tarea ya realizada")