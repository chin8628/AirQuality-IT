from django.urls import path, include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from .views import add, UserViewSet

router = routers.DefaultRouter()
router.register(r'air_quality', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('add/', csrf_exempt(add), name='add'),
]
