from django.contrib import admin 
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

app_name = 'guideline'

urlpatterns = [
    path('upload/', views.guide_view, name = 'upload'),
    path('', views.display_guideline, name = 'display'),
    path('edit/<int:id>', views.edit, name='edit'),
 ] 
  
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)