from django.db import models
from django.contrib import admin

class Corpus(models.Model):
    name = models.CharField(max_length=300,null=True)
    source = models.CharField(max_length=1000)
    typ = models.CharField(max_length=20)
    tim = models.CharField(max_length=300)
