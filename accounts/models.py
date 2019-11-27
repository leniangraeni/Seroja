from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

# Model ekstensi dari User
class SerojaUser(AbstractUser):
    # Pilihan Masukan
    TIPE_CHOICES = (
        ('admin', 'Admin'),
        ('pasien', 'Pasien'),
        ('petugas', 'Petugas'),
        ('dokter', 'Dokter'),
        ('apoteker', 'Apoteker'),
    )

    tipe = models.CharField(max_length=10, choices=TIPE_CHOICES, default='admin')

# Model Abstrak untuk semua akun
class Akun(models.Model):
    # Untuk Autentikasi
    # username = username (pasien), nomor_pegawai (petugas)
    # password
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Pilihan Masukan
    JK_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    # Informasi data diri Akun
    nama          = models.CharField(max_length=20)
    tempat_lahir  = models.CharField(max_length=20)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=JK_CHOICES)
    nomor_telepon = models.CharField(max_length=15)
    alamat        = models.TextField()

    class Meta():
        abstract = True

# Model untuk Pasien (turunan Akun)
class PasienInfo(Akun):
    # Informasi data diri khusus Pasien
    nomor_bpjs  = models.CharField(max_length=13, blank=True)
    bpjs        = models.ImageField(upload_to='akun/media/pasien/bpjs', blank=True)
    rekam_medik = models.CharField(max_length=13, blank=True)
    profil      = models.ImageField(upload_to='akun/media/pasien/profil', blank=True)

    # Meta untuk Pasien
    class Meta():
        db_table = 'PasienInfo'

    def __str__(self):
        return self.nama

# Model untuk Petugas (turunan Akun)
class PetugasInfo(Akun):
    # Informasi data diri khusus Petugas
    surat_tugas    = models.ImageField(upload_to='akun/media/petugas/surat_tugas', blank=True)
    profil         = models.ImageField(upload_to='akun/media/petugas/profil', blank=True)

    # Meta untuk Petugas
    class Meta():
        db_table = 'PetugasInfo'

    def __str__(self):
        return self.nama

# Model untuk Dokter (turunan Akun)
class DokterInfo(Akun):
    # Informasi data diri khusus Dokter
    surat_tugas    = models.ImageField(upload_to='akun/media/dokter/surat_tugas', blank=True)
    profil         = models.ImageField(upload_to='akun/media/dokter/profil', blank=True)
    # poli        = models.ForeignKey(Poli, on_delete=models.CASCADE)

    # Meta untuk Dokter
    class Meta():
        db_table = 'DokterInfo'

    def __str__(self):
        return self.nama

# Model untuk Apoteker (turunan Akun)
class ApotekerInfo(Akun):
    # Informasi data diri khusus Apoteker
    surat_tugas    = models.ImageField(upload_to='akun/media/apoteker/surat_tugas', blank=True)
    profil         = models.ImageField(upload_to='akun/media/apoteker/profil', blank=True)

    # Meta untuk Apoteker
    class Meta():
        db_table = 'ApotekerInfo'

    def __str__(self):
        return self.nama
