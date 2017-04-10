#! /usr/bin/env python3 

#import time
import shlex, subprocess
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl import DocType, String, Boolean


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
#         repo_url = 'https://github.com/'+commit.usuario+'/'+commit.repositorio+'.git'
#         cmd = "p2o.py --enrich --index git_raw --index-enrich git \-e http://localhost:9200 --no_inc --debug \git "+repo_url+""
#         cmd = shlex.split(cmd)
#         subprocess.call(cmd)
#         
#         cmd3 = "kidash.py --elastic_url-enrich http://locahost:9200 \--import /tmp/git-dashboard.json"
#         cmd3 = shlex.split(cmd3)
#         subprocess.call(cmd3)
        req = tareasIndex.get(id=commit.usuario+"-"+commit.repositorio, using=es, index='tareas')
        req.update(estado=True)
    else:
        print("Tarea ya realizada")