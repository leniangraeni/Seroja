from django.contrib import admin

from pengobatan.models import PoliInfo, JadwalPraktekInfo, ObatInfo, PengobatanInfo

# Register your models here.
admin.site.register(PoliInfo)
admin.site.register(JadwalPraktekInfo)
admin.site.register(ObatInfo)
admin.site.register(PengobatanInfo)
