import datetime
import json
from django.db import models


class CarPriv(models.Model):
    name = models.CharField(max_length=30)
    true_priv = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} {self.true_priv}"


class CarAuction(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.CharField(max_length=100, null=False, blank=False)


class CarCountry(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CarMake(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class CarFuel(models.Model):
    name = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.name


class CarBody(models.Model):
    """Сначала хотел реализовать по аналогии через choices, но потом понял, что лучше оставить возможность
    конечном пользователю самому добавлять какие его душе угодно варианты кузова"""

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CarColor(models.Model):
    name = models.CharField(max_length=30)
    true_color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.true_color}"


class KPP(models.Model):
    name = models.CharField(max_length=30)  # автомат/механика
    type = models.CharField(max_length=3)  # в исходной бд 1/2
    true_kpp = models.CharField(max_length=8)  # автомат/механика

    def __str__(self):
        return f"{self.true_kpp}"


class WheelPosition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    make = models.ForeignKey(CarMake, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Car(models.Model):
    """Тут еще вопрос на подумать кто будет администрировать сайт после его сдачи.
    Вероятно будет очень неприятно если человек случайно удалит страну, а вместе с ней 30% автомобилей
    """

    id = models.CharField(max_length=15, primary_key=True)
    auction = models.ForeignKey(CarAuction, on_delete=models.CASCADE)

    country = models.ForeignKey(CarCountry, on_delete=models.CASCADE, null=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, null=False)

    fuel = models.ForeignKey(CarFuel, on_delete=models.CASCADE, null=True)
    kpp = models.ForeignKey(KPP, on_delete=models.CASCADE)

    kuzov = models.ForeignKey(CarBody, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=250, null=True)

    year = models.PositiveIntegerField(null=False, blank=False)
    """в исходной бд по запросу выдать значения, где mileage %(10-1000) не выдает ничего > можно использовать инт"""
    mileage = models.PositiveIntegerField(null=False, blank=False, default=0)

    age = models.PositiveIntegerField(editable=False, null=True)
    is_sanction = models.BooleanField(editable=False, default=False)

    eng_volume = models.PositiveIntegerField(
        help_text="Объем двигателя в литрах",
    )

    wheel_position = models.ForeignKey(
        WheelPosition, on_delete=models.CASCADE, null=True
    )
    images = models.TextField(default="[]")

    equip = models.CharField(max_length=60, null=True)
    pw = models.PositiveIntegerField(default=0,null=True,blank=True)

    priv = models.ForeignKey(CarPriv, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(CarColor, on_delete=models.CASCADE, null=True)

    price_abroad = models.IntegerField(null=True, editable=False)
    price_in_russia = models.IntegerField(null=True, editable=False)

    rate = models.CharField(max_length=5, null=True, blank=True)
    finish = models.DecimalField(max_digits=10, decimal_places=2)

    def __save__(self, *args, **kwagrs):
        current_year = datetime.timezone.now().year
        self.age = current_year - self.year
        self.is_sanction = self.age in [3, 5]
        super(Car, self).save(*args, **kwagrs)

    def get_image_urls(self):
        """Получение списка URL изображений."""
        return json.loads(self.images)

    def set_image_urls(self, url_list):
        """Установка списка URL изображений."""
        self.images = json.dumps(url_list)

    def __str__(self):
        return f"{self.make} {self.model} {self.year}\n {self.kuzov}\n {self.eng_volume} {self.mileage}"
