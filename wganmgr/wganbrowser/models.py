from django.db import models

# Create your models here.

class modelSnapshot(models.Model):
    modelRun = models.ForeignKey(modelRun)
    checkpoint = models.IntegerField(default=0)
    path = models.CharField(max_length=512) 

class modelRun(models.Model):
    model = models.ForeignKey(model)
    path = models.CharField(max_length=512)
    name = models.CharField(max_length=512)

class model(models.Model):
    name = models.CharField(max_length=512)
    dataset = models.ForeignKey(dataset)


    #https://docs.djangoproject.com/en/4.1/intro/tutorial02/