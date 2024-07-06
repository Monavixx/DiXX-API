from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.FriendRequestView.as_view(), name='friend-request'),
    path('accept/', views.AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('list/', views.FriendsViewSet.as_view(), name='friend-list')
]