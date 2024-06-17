from django.urls import path
from .views import information_about_api

urlpatterns = [
    path('', information_about_api, name='information_about_api')
]