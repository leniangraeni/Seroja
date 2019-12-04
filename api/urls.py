from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views

urlpatterns = [
    path('guideline/', views.guideline_view, name="guideline_pasien"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.register, name="register_pasien"),
    path('pasien/', views.pasien_view, name="pasien_pasien"),
    path('status/', views.status_pendaftaran, name='status_pendaftaran'),

]
