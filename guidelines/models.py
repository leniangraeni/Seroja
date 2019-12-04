from django.db import models

class Guideline(models.Model):
    guide = models.ImageField(upload_to='images/guidelines/')
    keterangan = models.CharField(max_length=200)
