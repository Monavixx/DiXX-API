from django.urls import path, include
from .views import information_about_api, LoginView, RegenerateTokenView, RegistrationView
from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    path('info/', information_about_api, name='information_about_api'),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('regenerate-token/', RegenerateTokenView.as_view(), name='regenerate-token'),
    path('signup/', RegistrationView.as_view(), name='signup') 
]