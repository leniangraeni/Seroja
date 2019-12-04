from django.urls import path

# Memasukan views
from api import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('guideline/', views.guideline_response, name='guideline_response'),
    path('pasien_register/', views.pasien_register, name='pasien_register'),
    path('pasien_login/', views.pasien_login, name='pasien_login'),
    path('testing/', views.testing, name='testing'),
    path('daftar_pengobatan/', views.daftar_pengobatan, name='daftar_pengobatan'),
    path('status_pasien/', views.status_pasien, name='status_pasien'),
]
