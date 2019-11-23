from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/<tipe>/', views.akun_register, name='akun_register'),
    path('login/', views.akun_login, name='login'),
    path('logout/', views.akun_logout, name='logout'),
    path('home/', views.home, name='home'),

    #Ini buat ngetest redirect aja nanti kalo mau dibagusin diapus aja ya
    path('log_obat/', views.log_obat, name='log_obat'),
    path('profil/', views.profil, name='profil'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),  
    path('antrian/', views.antrian_pasien, name='antrian'),   
    path('poli/', views.poli, name='poli'), 
    path('petunjuk/', views.petunjuk, name='petunjuk'),
 ]
