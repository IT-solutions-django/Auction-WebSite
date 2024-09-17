import os
import requests
from django.db import models
from cars.models import CarMake,CarPriv, KPP,CarColor,WheelPosition,CarModel
from PIL import Image as image
from django.conf import settings
from .calc import calc_price
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class BodyType(models.Model):
    name  = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class ExportCountry(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=50)
    image_file = models.ImageField(upload_to='static/images/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        img = image.open(self.image_file)
        img = img.convert('RGB')
        
        webp_path = f'{os.path.splitext(self.image_file.name)[0]}.webp'
        webp_fullpath = os.path.join(settings.MEDIA_ROOT, webp_path)
        img.save(webp_fullpath, format='webp', quality=80)

        self.image_file.name = webp_path
        super().save(*args, **kwargs)
    
class FrontCar(models.Model):

    make = models.ForeignKey(CarMake,on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel,on_delete=models.PROTECT)

    grade = models.CharField(max_length=50,blank=True,null=True)
    kpp = models.ForeignKey(KPP,on_delete=models.PROTECT)

    privod = models.ForeignKey(CarPriv,on_delete=models.PROTECT)
    color = models.ForeignKey(CarColor, on_delete=models.PROTECT)

    equip = models.TextField(null=True,blank=True)
    pw = models.FloatField(null=True,blank=True,help_text='Мощность двигателя',validators=[MinValueValidator(0.0)])

    export_country = models.ForeignKey(ExportCountry,on_delete=models.PROTECT,null=False,blank=False,help_text='Страна экспортер')
    final = models.PositiveIntegerField()

    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    year = models.PositiveIntegerField(null=False,blank=False, default=0,validators=[MaxValueValidator(datetime.now().year)])
    
    mileage = models.PositiveIntegerField(null=False,blank=False,default=0)

    images = models.ManyToManyField(Image, related_name='cars',null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    wheel_position = models.ForeignKey(WheelPosition,on_delete=models.PROTECT)
    volume = models.PositiveIntegerField(default=0,null=False,blank=False,help_text='Объем двигателя',validators=[MinValueValidator(0)])

    price_abroad = models.PositiveIntegerField(editable=False,null=True,blank=True)
    price_in_russia = models.PositiveIntegerField(editable=False,null=True,blank=True)

    def save(self, *args, **kwargs):
        response = requests.get('https://auc.autocenter25.com/currency')
        currency = response.json() if response.status_code == 200 else []
        
        
        if str(self.export_country) == 'Япония':
            table = 'japan'
        elif str(self.export_country) == 'Китай':
            table = 'china'
        else:
            table = None  # В случае, если страна не указана
        

        prices = calc_price(price=float(self.final), currency=currency, year=self.year, volume=self.volume, table=table)
        
        # Убедимся, что prices содержит необходимые значения
        if prices:
            self.price_abroad = (int(prices[3]) // 1000) * 1000
            self.price_in_russia = (int(prices[2]) // 1000) * 1000
        else:
            self.price_abroad = 0  
            self.price_in_russia = 0  

        # Теперь вызываем метод save суперкласса
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.make} {self.model} {self.year} {self.color}'
    
class CarContainer(models.Model):
    name = models.CharField(max_length=100)
    cars = models.ManyToManyField(FrontCar, related_name='containers')

    def __str__(self):
        return self.name