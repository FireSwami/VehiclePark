from distutils.util import strtobool

import django_filters

from .models import Driver, Vehicle


class DriverDateFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        input_formats=["%d-%m-%Y"],
        help_text="example: 10-11-2021",
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        input_formats=["%d-%m-%Y"],
        help_text="example: 16-11-2021",
    )

    class Meta:
        model = Driver
        fields = ["created_at__gte", "created_at__lte"]


class VehicleDriverFilter(django_filters.FilterSet):
    with_drivers = django_filters.TypedChoiceFilter(
        field_name="driver",
        choices=(
            ("yes", "True"),
            ("no", "False"),
        ),
        coerce=strtobool,
        lookup_expr="isnull",
        exclude=True,
    )

    class Meta:
        model = Vehicle
        fields = ["with_drivers"]
