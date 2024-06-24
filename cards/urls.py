from django.urls import path, include
from .views import MySetsViewSet, SetView, LearnRandomView, CreateSetView
from rest_framework import routers


#router = routers.DefaultRouter()
#router.register(r'cards/', CardViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('sets/my/', MySetsViewSet.as_view(), name='my-sets'),
    path('set/<int:id>/', SetView.as_view(), name='set-detailed'),
    path('set/<int:id>/random-learn/', LearnRandomView.as_view(), name='random-learn'),
    path('create-new-set/', CreateSetView.as_view(), name='create-set-view')
]