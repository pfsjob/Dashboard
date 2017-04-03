from django.shortcuts import render, render_to_response
from django.template import Context

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from creador.models import tareasForm
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from .models import tareas
from .search import tareasIndex
from elasticsearch import Elasticsearch
import elasticsearch_dsl
import time

class TareaList(ListView):
    model = tareas

def index(request):
    return render_to_response('index.html')

def lista_tareas(request):
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
    req = req.source(['usuario', 'repositorio', 'estado'])
    resp = req.scan()
#     lista=[]
#     for commit in response:
#         t=tareas(commit.usuario,commit.repositorio,commit.estado)
#         lista.append(t)
#     print(lista)
    return render(request, 'tareas_list.html', {'object_list': resp})

def add_tarea(request):
    if request.method == 'POST':
        form = tareasForm(request.POST)
        if form.is_valid():
            new_tarea = form.save()
            return HttpResponseRedirect(reverse('utareas:tlist'))
    else:
        form = tareasForm()

    return render(request, 'tarea_form.html', {'form': form})

def delete_tarea(request):
    elemento=request.POST.get('delete')
    es = Elasticsearch()
    request = tareasIndex.get(id=elemento, using=es, index='tareas')
    request.delete()
    time.sleep(1)
    return HttpResponseRedirect(reverse('utareas:tlist'))
