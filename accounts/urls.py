from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/<tipe>/', views.akun_register, name='akun_register'),
    path('login/', views.akun_login, name='login'),
    path('logout/', views.akun_logout, name='logout'),
    path('home/', views.home, name='home'),
<<<<<<< HEAD
    path('signup/', views.signup, name='signup'),
    path('petugas_signup/', views.petugas_signup, name='petugas_signup'),
    path('dokter_signup/', views.dokter_signup, name='dokter_signup'),
    path('apoteker_signup/', views.apoteker_signup, name='apoteker_signup'),
    # path('', include('django.contrib.auth.urls'))
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('log_obat/', views.log_obat, name='log_obat'),
    path('profil/', views.profil, name='profil'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),  
    path('antrian/', views.antrian_pasien, name='antrian'),   
    path('poli/', views.poli, name='poli'), 
    path('petunjuk/', views.petunjuk, name='petunjuk'),   
 ] 
=======
 ]
>>>>>>> 43e1ff24caf09a50950986b8b13a4b93fbea6ddc
