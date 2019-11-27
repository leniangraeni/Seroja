# Fungsi untuk mengatur routing halaman
from django.urls import path, include
from django.conf.urls import url

# Fungsi untuk mengatur routing file dalam projek
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Memasukan views
from pengobatan import views

app_name = 'pengobatan'
urlpatterns = [
    #Ini buat ngetest redirect aja nanti kalo mau dibagusin diapus aja ya
    path('beranda/', views.beranda, name='beranda'),
    path('pengobatan/<antrian>/', views.detail_pengobatan, name='detail_pengobatan'),
    path('antrian/', views.antrian_pasien, name='antrian'),
    path('poli/', views.poli, name='poli'),
    path('poli/tambah', views.tambah_poli, name='tambah_poli'),
    path('poli/<nama_poli>/<jadwal>/', views.ubah_jadwal, name='ubah_jadwal'),
    path('poli/<nama_poli>/', views.tambah_jadwal, name='tambah_jadwal'),
    path('profil/', views.profil, name='profil'),
    path('profil/ubah/', views.ubah_profil, name='ubah_profil'),
    path('petunjuk/', views.petunjuk, name='petunjuk'),
    path('petunjuk/ubah/<int:id>', views.ubah_petunjuk, name='ubah_petunjuk'),
    path('log_obat/', views.log_obat, name='log_obat'),
    # path('pengaturan/', views.pengaturan, name='pengaturan'),
]
