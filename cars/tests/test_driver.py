from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.models import Driver
from cars.serializers import DriverSerializer


class DriverTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.driver_1 = Driver.objects.create(first_name="fname1", last_name="lname1")
        self.driver_2 = Driver.objects.create(first_name="fname2", last_name="lname2")
        self.driver_3 = Driver.objects.create(first_name="fname3", last_name="lname3")

    def test_count(self):
        self.assertEqual(3, Driver.objects.all().count())

    def test_get_driver(self):
        response = self.client.get(reverse("driver-list"))
        serializer_data = DriverSerializer(
            [self.driver_1, self.driver_2, self.driver_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        data = {"first_name": "TestFirstname", "last_name": "TestLastname"}
        response = self.client.post(reverse("driver-list"), data=data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Driver.objects.all().count())
        self.assertEqual(data["last_name"], Driver.objects.all()[0].last_name)
        self.assertEqual(data["first_name"], Driver.objects.all()[0].first_name)

    def test_create_ru_name(self):
        data = {"first_name": "Иван", "last_name": "Иванов"}
        response = self.client.post(reverse("driver-list"), data=data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Driver.objects.all().count())
        self.assertEqual(data["last_name"], Driver.objects.all()[3].last_name)
        self.assertEqual(data["first_name"], Driver.objects.all()[3].first_name)

    def test_update(self):
        data = {"first_name": "Firstname", "last_name": "Lastname"}
        self.client.force_login(self.user)
        response = self.client.put(
            reverse("driver-detail", kwargs={"pk": self.driver_3.id}),
            data=data,
            format="json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.driver_3.refresh_from_db()
        self.assertEqual(data["first_name"], self.driver_3.first_name)
        self.assertEqual(data["last_name"], self.driver_3.last_name)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse("driver-detail", kwargs={"pk": 2}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Driver.objects.all().count())

    def test_filter_after_date(self):
        response = self.client.get(
            reverse("driver-list") + "?created_at__gte=10-11-2021", format="json"
        )
        serializer_data = DriverSerializer(
            [self.driver_1, self.driver_2, self.driver_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_before_date(self):
        response = self.client.get(
            reverse("driver-list") + "?created_at__lte=16-11-2021", format="json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)

    def test_fail_driver_detail(self):
        response = self.client.get(reverse("driver-detail", kwargs={"pk": 10}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_driver_detail(self):
        response = self.client.get(
            reverse("driver-detail", kwargs={"pk": self.driver_3.id})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json().get("first_name"), "fname3")
        self.assertEqual(response.json().get("last_name"), "lname3")

    def test_driver_str(self):
        self.assertEqual(str(self.driver_1), "lname1 (FNAME1)")
