"""
URL configuration for quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.load_all_quizes, name='all_quizzes'),
    path('save-result/', views.save_quiz_result, name='save_quiz_result'),
    path('leaderboard/', views.load_leaderboard, name="load_leaderboard"),
    path('leaderboard/<str:quiz_name>/', views.leaderboard_view, name='leaderboard'),
    path('leaderboard/<str:quiz_name>/analysis', views.leaderboard_chart, name='analysis'),
    path('<str:quiz_name>/', views.quiz, name="quiz"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
