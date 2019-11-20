from django.contrib import admin
from accounts.models import PetugasInfo, DokterInfo, ApotekerInfo

# Register your models here.
admin.site.register(PetugasInfo)
admin.site.register(DokterInfo)
admin.site.register(ApotekerInfo)
