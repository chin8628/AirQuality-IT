from datetime import datetime, timedelta
from random import randint

from django.urls import reverse
from django.test import TestCase
from .models import AirQuality, Device

from rest_framework.test import APITestCase, APIClient


class AirqualityTest(TestCase):
    def setUp(self):
        Device(name="test_device", longitude='123', latitude='123').save()
        device = Device.objects.all()[0]
        AirQuality(pm25=10, device_id=device).save()

    def test_can_get_latest_airquality(self):
        """Animals that can speak are correctly identified"""
        airq = AirQuality.objects.latest('id')
        self.assertEqual(airq.pm25, 10)


class ApiTest(APITestCase):
    def setUp(self):
        Device(name="test_1", longitude='123', latitude='123').save()
        device = Device(name="test_2", longitude='123', latitude='123')
        device.save()

        self.device = device

        for i in range(10):
            pm100, pm25, pm10 = randint(1, 100), randint(1, 100), randint(1, 100)
            AirQuality(pm100=pm100, pm25=pm25, pm10=pm10, device_id=self.device).save()

        for i in range(5):
            pm100, pm25, pm10 = randint(1, 100), randint(1, 100), randint(1, 100)
            past_date = datetime.today() - timedelta(days=2)

            aqi_inst = AirQuality(pm100=pm100, pm25=pm25, pm10=pm10, device_id=self.device)
            aqi_inst.save()

            # Use update() to override datetime value on auto_add field
            AirQuality.objects.filter(id=aqi_inst.id).update(created_at=past_date)

        self.client = APIClient()

    def test_can_get_all_device(self):
        url = reverse('get_devices')
        res = self.client.get(url, format="json")
        self.assertEqual(len(res.data), 2)

    def test_can_get_24hr_avg_aqi_log(self):
        url = reverse('get_aqi_logs', args=[self.device.device_id, 24])
        res = self.client.get(url, format="json")

        self.assertEqual(len(res.data), 1)

    def test_can_get_specific_device(self):
        url = reverse('get_device', args=[self.device.device_id])
        res = self.client.get(url, format='json')
        self.assertEqual(res.data['name'], self.device.name)
