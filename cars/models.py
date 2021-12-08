from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        abstract = True


class Driver(DateMixin):
    first_name = models.CharField(max_length=50, help_text="Ivan", verbose_name="Имя")
    last_name = models.CharField(
        max_length=50, help_text="Ivanov", verbose_name="Фамилия"
    )

    def __str__(self):
        return "{} ({})".format(self.last_name, self.first_name.upper())

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ["first_name"]


class Vehicle(DateMixin):
    driver = models.ForeignKey(
        "Driver",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Водитель",
        related_name="vehicles",
    )
    make = models.CharField(
        max_length=30, blank=True, help_text="Opel", verbose_name="Автоконцерн"
    )
    model = models.CharField(
        max_length=30, blank=True, help_text="Corsa D", verbose_name="Модель"
    )
    plate_number = models.CharField(
        max_length=30,
        help_text="AA 1234 OO",
        unique=True,
        blank=True,
        verbose_name="Номерной знак",
    )

    def __str__(self):
        return self.make

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["id"]
