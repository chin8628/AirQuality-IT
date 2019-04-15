from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from external_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('external_api.urls')),
]
