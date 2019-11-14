from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('petugas_signup/', views.petugas_signup, name='signup'),
    path('dokter_signup/', views.dokter_signup, name='dokter_signup'),
    path('apoteker_signup/', views.apoteker_signup, name='apoteker_signup'),
    # path('', include('django.contrib.auth.urls'))
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
 ] 
