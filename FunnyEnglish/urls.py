#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='FunnyEnglish-home'),
    path('about/',views.about,name='FunnyEnglish-about'),
]
