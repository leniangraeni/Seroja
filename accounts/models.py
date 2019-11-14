from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'petugas'),
      (2, 'dokter'),
      (3, 'apoteker'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    
    nomor_pegawai = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='images/',blank=True)
    surat_tugas = models.ImageField(upload_to='images/',blank=True)