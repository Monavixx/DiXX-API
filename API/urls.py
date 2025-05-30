
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('cards/', include('cards.urls')),
    path('friends/', include('friends.urls'))
]
