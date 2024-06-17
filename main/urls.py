from django.urls import path, include
from .views import information_about_api, LoginView
from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    path('info/', information_about_api, name='information_about_api'),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login')
]