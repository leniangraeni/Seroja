from django.db import models

# Memasukan model dan form
from accounts.models import PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo

# Create your models here.

# Model informasi poli
class PoliInfo(models.Model):
    nama             = models.CharField(max_length=20)
    penanggung_jawab = models.CharField(max_length=20)

    def __str__(self):
        return self.nama

# Model informasi jadwal praktek setiap dokter
class JadwalPraktekInfo(models.Model):
    # Referensi dari model lain (one-to-many)
    dokter = models.ForeignKey(DokterInfo, on_delete=models.CASCADE)
    poli   = models.ForeignKey(PoliInfo, on_delete=models.CASCADE)

    # Informasi tambahan
    hari          = models.DateTiemField()
    waktu_mulai   = models.DateTimeField()
    waktu_selesai = modesl.DateTimeField()

    def __str__(self):
        return "{}, {}".format(self.dokter, self.poli)

# Model informasi obat
class ObatInfo(models.Model):
    nama      = models.CharField(max_length=20)
    deskripsi = models.CharField(max_length=200)

    def __str__(self):
        return self.nama

# Model informasi pengobatan tiap pasien
class PengobatanInfo(models.Model):
    # Referensi dari model lain (one-to-many)
    pasien   = models.ForeignKey(PasienInfo, on_delete=models.CASCADE)
    petugas  = models.ForeignKey(PetugasInfo, on_delete=models.CASCADE, blank=True)
    dokter   = models.ForeignKey(DokterInfo, on_delete=models.CASCADE, blank=True)
    apoteker = models.ForeignKey(ApotekerInfo, on_delete=models.CASCADE, blank=True)
    obat     = models.ForeignKey(ObatInfo, on_delete=models.CASCADE, blank=True)
    jadwal   = models.ForeignKey(JadwalPraktekInfo, on_delete=models.CASCADE, blank=True)

    # Kondisi pengobatan pasien
    sudah_verifikasi = models.BooleanField(default=False)
    sudah_ditangani  = models.BooleanField(default=False)
    sudah_berobat    = models.BooleanField(default=False)
    ditolak          = models.BooleanField(deafult=False)
    pesan_penolakan  = models.CharField(max_length=200, blank=True)

    # Informasi tambahan
    tanggal_berkunjung = models.DateTiemField()
    keluhan            = models.CharField(max_length=200, blank=True)
    rujukan            = models.ImageField(upload_to='/rujukan/', blank=True)
    dosis              = models.PositiveIntegerField(blank=True)
    aturan             = models.CharField(max_length=200, blank=True)
    catatan            = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.pasien.nama
