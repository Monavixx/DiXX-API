from django.urls import path, include
from .views import SetViewSet, SetView
from rest_framework import routers


#router = routers.DefaultRouter()
#router.register(r'cards/', CardViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('my-sets/', SetViewSet.as_view(), name='my-sets'),
    path('my-sets/<int:id>/', SetView.as_view(), name='set_detailed')
]