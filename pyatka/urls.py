from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('pyatka/admin/', admin.site.urls),
    path('pyatka/ajax/', include('api.urls')),
    path('pyatka/', include('frontend.urls')),
]
