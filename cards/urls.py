from django.urls import path, include
from .views import MySetViewSet, SetView, LearnRandomView
from rest_framework import routers


#router = routers.DefaultRouter()
#router.register(r'cards/', CardViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('sets/my/', MySetViewSet.as_view(), name='my-sets'),
    path('sets/<int:id>/', SetView.as_view(), name='set_detailed'),
    path('sets/<int:id>/random-learn/', LearnRandomView.as_view(), name='random-learn')
]