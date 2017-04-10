from django.conf.urls import url, include
from social_django.urls import urlpatterns as social_django_urls
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='tindex'),
    #url(r'^indexreg/', views.indexregistrado, name='tindex'),
    #url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^lista/$', views.lista_tareas, name='tlist'),
    url(r'^add/$', views.add_tarea, name='tadd'),
    url(r'^delete/$', views.delete_tarea, name='tdelete'),
    url(r'^inicio/$', views.redirigir, name='tinicio'),
]
