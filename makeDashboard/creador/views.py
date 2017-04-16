from django.shortcuts import render, render_to_response, redirect
from django.template import Context

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from creador.models import tareasForm
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from .models import tareas
from .search import tareasIndex
from elasticsearch import Elasticsearch
import elasticsearch_dsl
import time
import requests
import json

class TareaList(ListView):
    model = tareas

def index(request):
    return render_to_response('index.html')

def indexregistrado(request):

    client_id='bd2ade5d39bb1b529fb7'
    client_secret='35b46ffbac1f02ea2ca84f44d2450fd00ffd6f40'
    codigo = request.GET.get('code')
    print(codigo)
    url = 'https://github.com/login/oauth/access_token'
    header = {'content-type':'application/json'}
    payload = {}
    payload['client_id']=client_id
    payload['client_secret']=client_secret
    payload['code']=codigo

    res = requests.post(
        url,
        data = json.dumps(payload),
        headers=header
        )
    
    #print(res.content)
    #j = json.dumps(res.text)
    return HttpResponse(res.content)
#     print(j)
#     token = j['token']
#     print ('New token: %s' % token)

def redirigir(request):
    return redirect('https://github.com/login/oauth/authorize?client_id=bd2ade5d39bb1b529fb7')

def lista_tareas_usuario(request):
    usuario=request.path.split('/tareas/listausuario/')
    url='https://api.github.com/users/'+usuario[1]+'/repos'
    res = requests.get(
        url,
        #data = json.dumps(payload),
        )
    #print(res.content)
    salidaaux=json.loads(res.content)#,indent=2)
    salida=json.dumps(salidaaux,indent=2)
    for x in salidaaux:
        print(x['name'])
    return HttpResponse(salida, content_type='application/json')
    

def lista_tareas(request):
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)
    #print(salida)
    return HttpResponse(salida, content_type='application/json')
#     req = req.source(['usuario', 'repositorio', 'estado'])
#     resp = req.scan()
#     
#     return render(request, 'tareas_list.html', {'object_list': resp})

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
