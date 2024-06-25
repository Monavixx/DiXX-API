from django.urls import path, include
from . import views
from rest_framework import routers


#router = routers.DefaultRouter()
#router.register(r'cards/', CardViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('sets/my/', views.MySetsViewSet.as_view(), name='my-sets'),
    path('set/<int:id>/', views.SetView.as_view(), name='set-detailed'),
    path('set/<int:id>/random-learn/', views.LearnRandomView.as_view(), name='random-learn'),
    path('create-new-set/', views.CreateSetView.as_view(), name='create-new-set'),
    path('remove-set/', views.RemoveSetView.as_view(), name='remove-set'),
    path('edit-set/<int:pk>/', views.EditSetView.as_view(), name='edit-set'),
    path('set/<int:pk>/add-card/', views.AddCardView.as_view(), name='add-card')
]