from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .filters import DriverDateFilter, VehicleDriverFilter
from .models import Driver, Vehicle
from .serializers import (DriverSerializer, VehicleDriverSerializer,
                          VehicleSerializer)


class DriverViewSet(viewsets.ModelViewSet):
    """Перечень водителей"""

    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DriverSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = DriverDateFilter
    ordering_fields = ["id", "first_name", "last_name", "created_at", "updated_at"]


class VehicleViewSet(viewsets.ModelViewSet):
    """Перечень машин"""

    queryset = Vehicle.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = VehicleDriverFilter
    ordering_fields = [
        "id",
        "driver",
        "make",
        "model",
        "plate_number",
        "created_at",
        "updated_at",
    ]


class VehicleDriverView(CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDriverSerializer
    lookup_url_kwarg = "vehicle_id"
    lookup_field = "id"

    def create(self, request, vehicle_id):
        vehicle = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vehicle.driver_id = serializer.data["driver"]
        vehicle.save()

        return Response(VehicleSerializer(instance=vehicle).data)
