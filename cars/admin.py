from django.contrib import admin

from cars.models import Driver, Vehicle


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    )
    list_display_links = ("last_name",)
    search_fields = (
        "last_name",
        "first_name",
    )
    list_filter = ("created_at",)
    save_on_top = True


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "driver",
        "make",
        "model",
        "plate_number",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("id", "make", "model", "plate_number")
    list_filter = (
        "created_at",
        "driver",
    )


admin.site.site_title = "Админ-панель сайта парковки"
admin.site.site_header = "Админ-панель парковки"
