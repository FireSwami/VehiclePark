from django.urls import path
from rest_framework import routers

from cars import views

router = routers.DefaultRouter()
router.register(r"drivers/driver", views.DriverViewSet, "driver")
router.register(r"vehicles/vehicle", views.VehicleViewSet, "vehicle")

urlpatterns = [
    path(
        "vehicles/set_driver/<vehicle_id>/",
        views.VehicleDriverView.as_view(),
        name="set_driver",
    ),
]

urlpatterns += router.urls
