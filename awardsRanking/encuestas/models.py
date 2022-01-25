from django.db import models
from django.utils import timezone
import datetime


class Pregunta(models.Model):
    pregunta_text = models.CharField(max_length= 200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.pregunta_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        
    
class Opciones(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_text = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.opcion_text

    
