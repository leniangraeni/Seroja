# Fungsi untuk pengaturan Django
from django.conf import settings

# Fungsi untuk views admin bawaan Django
from django.contrib import admin

# Fungsi untuk mengatur routing halaman
from django.urls import path, include
from django.conf.urls import url

# Fungsi untuk mengatur routing file dalam projek
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Memasukan views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name="welcome"),
    path('guidelines/', include('guidelines.urls')),
    path('accounts/', include('accounts.urls')),
    path('<tipe>/', include('pengobatan.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
