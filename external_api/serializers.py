from .models import AirQuality, Device
from rest_framework import serializers


class AirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQuality
        fields = ('pm250', 'pm100', 'pm10', 'created_at', 'device_id')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('device_id', 'name', 'location', 'latitude', 'longitude')
