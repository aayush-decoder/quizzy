from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
   path('login/', views.login_view, name='login'),
   path('signup/', views.signup_view, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)