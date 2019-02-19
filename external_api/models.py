import hashlib
import random

from django.db import models


def generate_token():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=1000, null=True)
    longitude = models.CharField(max_length=25, null=True)
    latitude = models.CharField(max_length=25, null=True)
    token = models.CharField(max_length=500, null=True)

    def __str__(self):
        return '%s (ID: %s)' % (self.name, self.device_id)

    def save(self):
        if (self.token == None):
            self.token = generate_token()

        super(Device, self).save()


class AirQuality(models.Model):
    pm250 = models.FloatField(verbose_name="PM2.5 (µm/m^3)", default=0)
    pm100 = models.FloatField(verbose_name="PM10 (µm/m^3)", default=0)
    pm10 = models.FloatField(verbose_name="PM1 (µm/m^3)", default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    device_id = models.ForeignKey(
        Device, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '%s (%s)' % (self.device_id, self.created_at.strftime("%d/%m/%Y %H:%M:%S"))

    class Meta:
        verbose_name = "Air Quality"
        verbose_name_plural = 'Air Quality'
