from django.test import TestCase
from .models import AirQuality, Device


class AirqualityTest(TestCase):
    def setUp(self):
        Device(name="test_device", longitude='123', latitude='123').save()
        device = Device.objects.all()[0]
        AirQuality(pm25=10, device_id=device).save()

    def test_can_get_latest_airquality(self):
        """Animals that can speak are correctly identified"""
        airq = AirQuality.objects.latest('id')

        self.assertEqual(airq.pm25, 10)
