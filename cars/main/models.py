
from django.db import models
from django.db.models import Q
from jp_center.models import FrontCar, CarModel
from cars.models import CarColor, CarMake, CarPriv, KPP


class Currency(models.Model):
    currency_name = models.CharField(
        max_length=10, verbose_name="Валюта"
    )  # Поле для хранения названия валюты
    date = models.DateField(verbose_name="Дата")  # Поле для хранения даты курса
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс"
    )  # Поле для хранения курса валюты

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ["date"]  # Сортируем по дате

    def __str__(self):
        return f"{self.currency_name} - {self.exchange_rate} на {self.date}"

"""Дальше будут модели для фильтров"""


class YearFilter(models.Model):
    name =  models.CharField(max_length=4,null=False,blank=False)
    value = models.PositiveIntegerField(null=False,blank=False)

    def __str__(self):
        return self.name

class PowerFilter(models.Model):
    name = models.CharField(max_length=5,null=False,blank=False)
    value = models.PositiveSmallIntegerField(null=False,blank=False)

class VolumeFilter(models.Model):
    name = models.CharField(max_length=5,null=False,blank=False,help_text='Указывайте объем в литрах')
    value = models.FloatField(null=False,blank=False,help_text='Указывайте объем в см^3\n1л = 1000см^3')

    def __str__(self):
        return (f'{self.name}л -- {self.value}см^3')

class MileageMinFilter(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    value = models.PositiveIntegerField(null=False,blank=False)

class MileageMaxFilter(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    value = models.PositiveIntegerField(null=False,blank=False)



