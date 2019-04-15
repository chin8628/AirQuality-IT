from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('devices', views.devices, name="get_devices"),
    path('devices/<int:device_id>', views.get_device, name="get_device"),
    path('aqi_logs/<int:device_id>/<int:hours>/', views.airquality_logs, name="get_aqi_logs"),
    path('aqi_logs/<int:device_id>/lastest/', views.lastest_aqi_log, name="get_lastest_aqi_log"),
    path('add/', csrf_exempt(views.add), name='add'),
]
