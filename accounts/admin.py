from django.contrib import admin

# Modeld dan Form dari aplikasi
from accounts.models import SerojaUser, PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo


# Register your models here.
admin.site.register(SerojaUser)
admin.site.register(PasienInfo)
admin.site.register(PetugasInfo)
admin.site.register(DokterInfo)
admin.site.register(ApotekerInfo)
