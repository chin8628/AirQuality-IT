from django.contrib import admin
from .models import AirQuality, Device

class DeviceAdmin(admin.ModelAdmin):
      readonly_fields=('token', )

admin.site.register(AirQuality)
admin.site.register(Device, DeviceAdmin)
