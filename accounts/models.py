from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (0, 'none'),
      (1, 'petugas'),
      (2, 'dokter'),
      (3, 'apoteker'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=0)
    
    avatar = models.ImageField(upload_to='images/',blank=True)
    surat_tugas = models.ImageField(upload_to='images/',blank=True)