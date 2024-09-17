from django.db import models
from jp_center.models import FrontCar

class AbstractCarCatalog(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20)

    class Meta:
        abstract = True  # Указываем, что это абстрактный класс

    def __str__(self):
        return f"{self.country}"