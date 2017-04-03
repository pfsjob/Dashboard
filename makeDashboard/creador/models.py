from django.db import models
from django.forms import ModelForm
from .search import tareasIndex

# Create your models here.

# class tareas(models.Model):
#     pid=models.ForeignKey
#     usuario=models.CharField(max_length=100)
#     repositorio=models.CharField(max_length=100)
#     estado=models.BooleanField
    
class tareas(models.Model):
    usuario=models.CharField(max_length=100)
    repositorio=models.CharField(max_length=100)
    estado=models.BooleanField(default=True)
    
    
    def indexing(self):
        obj = tareasIndex(
           meta={'type': "doc_type", 'id': self.usuario+"-"+self.repositorio},
           usuario=self.usuario,
           repositorio=self.repositorio,
           estado=self.estado,
        )
        obj.save(index='tareas')
        return obj.to_dict(include_meta=True)
    
class tareasForm(ModelForm):
    class Meta:
        model = tareas
        fields = '__all__'
    
# class BlogPost(models.Model):
#    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
#    posted_date = models.DateField(default=timezone.now)
#    title = models.CharField(max_length=200)
#    text = models.TextField(max_length=1000)