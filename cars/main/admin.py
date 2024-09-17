from django.contrib import admin
from .models import YearFilter,PowerFilter,VolumeFilter,MileageMaxFilter,MileageMinFilter



admin.site.register((YearFilter,PowerFilter,VolumeFilter,MileageMaxFilter,MileageMinFilter))
