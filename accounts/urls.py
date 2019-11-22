from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/<tipe>/', views.akun_register, name='akun_register'),
    path('login/', views.akun_login, name='login'),
    path('home/', views.home, name='home'),
 ]
