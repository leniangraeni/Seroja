from django.db import models

class Guideline(models.Model):
    guide = models.ImageField(upload_to='images/guidelines/')
