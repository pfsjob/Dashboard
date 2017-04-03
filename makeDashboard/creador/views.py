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

class TareaList(ListView):
    model = tareas

def index(request):
    return render_to_response('index.html')

def lista_tareas(request):
    es = Elasticsearch()
    request = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
    request = request.source(['usuario', 'repositorio', 'estado'])
    response = request.scan()
    lista=[]
    for commit in response:
        t=tareas(commit.usuario,commit.repositorio,commit.estado)
        lista.append(t)
    print(lista)
    return render(request, 'tareas_list.html', {'object_list': lista})

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
    return HttpResponseRedirect(reverse('utareas:tlist'))
