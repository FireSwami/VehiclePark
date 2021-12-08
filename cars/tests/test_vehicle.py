from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.models import Driver, Vehicle
from cars.serializers import VehicleDriverSerializer, VehicleSerializer


class VehicleTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.driver_1 = Driver.objects.create(first_name="fname1", last_name="lname1")
        self.driver_2 = Driver.objects.create(first_name="fname2", last_name="lname2")
        self.driver_3 = Driver.objects.create(first_name="fname3", last_name="lname3")

        self.vehicle_1 = Vehicle.objects.create(
            driver=self.driver_1,
            make="test_brand",
            model="test_model",
            plate_number="test_number_1",
        )
        self.vehicle_2 = Vehicle.objects.create(
            driver=self.driver_2,
            make="test_brand",
            model="test_model",
            plate_number="test_number_2",
        )
        self.vehicle_3 = Vehicle.objects.create(
            driver=None,
            make="test_brand",
            model="test_model",
            plate_number="test_number_3",
        )

    def test_count(self):
        self.assertEqual(3, Vehicle.objects.all().count())

    def test_get_vehicle(self):
        response = self.client.get(reverse("vehicle-list"))
        serializer_data = VehicleSerializer(
            [self.vehicle_1, self.vehicle_2, self.vehicle_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        data = {
            "driver": 1,
            "make": "test_brand",
            "model": "test_model",
            "plate_number": "test_number_4",
        }

        response = self.client.post(reverse("vehicle-list"), data=data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Vehicle.objects.all().count())
        self.assertEqual(data["plate_number"], Vehicle.objects.all()[3].plate_number)
        self.assertEqual(data["driver"], Vehicle.objects.all()[3].driver.id)

    def test_create_no_driver(self):
        data = {
            "driver": None,
            "make": "test_brand",
            "model": "test_model",
            "plate_number": "test_number_4",
        }

        response = self.client.post(reverse("vehicle-list"), data=data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Vehicle.objects.all().count())
        self.assertEqual(data["plate_number"], Vehicle.objects.all()[3].plate_number)

    def test_create_same_number(self):
        data = {
            "driver": None,
            "make": "test_brand",
            "model": "test_model",
            "plate_number": "test_number_3",
        }

        response = self.client.post(reverse("vehicle-list"), data=data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(3, Vehicle.objects.all().count())
        error = ["Автомобиль с таким Номерной знак уже существует."]
        self.assertEqual(error, response.json().get("plate_number"))

    def test_update(self):
        data = {
            "driver": None,
            "make": "test_brand_update",
            "model": "test_model_update",
            "plate_number": "test_number_update",
        }
        self.client.force_login(self.user)
        response = self.client.put(
            reverse("vehicle-detail", kwargs={"pk": self.vehicle_2.id}),
            data=data,
            format="json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.vehicle_2.refresh_from_db()
        self.assertEqual(data["make"], self.vehicle_2.make)
        self.assertEqual(data["model"], self.vehicle_2.model)
        self.assertEqual(data["plate_number"], self.vehicle_2.plate_number)
        self.assertEqual(data["driver"], self.vehicle_2.driver)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse("vehicle-detail", kwargs={"pk": 2}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Vehicle.objects.all().count())

    def test_filter_no(self):
        response = self.client.get(
            reverse("vehicle-list") + "?with_drivers=no", format="json"
        )
        serializer_data = VehicleSerializer([self.vehicle_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_yes(self):
        response = self.client.get(
            reverse("vehicle-list") + "?with_drivers=yes", format="json"
        )
        serializer_data = VehicleSerializer(
            [self.vehicle_1, self.vehicle_2], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_fail_vehicle_detail(self):
        response = self.client.get(reverse("vehicle-detail", kwargs={"pk": 10}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_vehicle_detail(self):
        response = self.client.get(
            reverse("vehicle-detail", kwargs={"pk": self.vehicle_1.id})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json().get("make"), "test_brand")
        self.assertEqual(response.json().get("model"), "test_model")
        self.assertEqual(response.json().get("plate_number"), "test_number_1")
        self.assertEqual(response.json().get("driver"), self.driver_1.id)

    def test_vehicle_set_driver(self):
        data = {
            "driver": 1,
        }
        self.assertEqual(None, self.vehicle_3.driver)
        response = self.client.post(
            reverse("set_driver", kwargs={"vehicle_id": 3}), data=data, format="json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json().get("driver"), self.driver_1.id)
        self.vehicle_3.refresh_from_db()
        self.assertEqual(data["driver"], Vehicle.objects.all()[2].driver.id)

    def test_serializer(self):
        response = self.client.get(reverse("vehicle-list"))
        serializer_data = VehicleDriverSerializer(
            [self.vehicle_1, self.vehicle_2, self.vehicle_3], many=True
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            serializer_data.data[0].get("driver"), response.json()[0].get("driver")
        )
        self.assertEqual(
            serializer_data.data[1].get("driver"), response.json()[1].get("driver")
        )
        self.assertEqual(
            serializer_data.data[2].get("driver"), response.json()[2].get("driver")
        )

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle_1), "test_brand")
