from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='tindex'),
    url(r'^lista/$', views.TareaList.as_view(), name='tlist'),
    url(r'^add/$', views.add_tarea, name='tadd'),
    url(r'^delete/$', views.delete_tarea, name='tdelete'),
]
