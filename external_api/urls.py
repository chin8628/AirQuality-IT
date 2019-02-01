from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('add/', csrf_exempt(views.add), name='add'),
]
