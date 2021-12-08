from rest_framework import serializers

from .models import Driver, Vehicle


class DriverSerializer(serializers.ModelSerializer):
    """Список водителей"""

    class Meta:
        model = Driver
        fields = ("first_name", "last_name")
        # in case of all information need
        # fields = ('__all__')


class VehicleSerializer(serializers.ModelSerializer):
    """Список автомобилей"""

    class Meta:
        model = Vehicle
        fields = ("make", "model", "plate_number", "driver")
        # in case of all information need
        # fields = ('__all__')


class VehicleDriverSerializer(serializers.Serializer):
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(), allow_null=True
    )
