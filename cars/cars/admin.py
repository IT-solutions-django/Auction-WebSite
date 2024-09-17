from django.contrib import admin
from .models import Car, CarBody, CarColor, CarCountry, CarFuel,  CarMake, KPP, CarPriv



class CarColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'true_color')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('true_color').distinct('true_color')

class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'country',
        "make",
        "model",
        'color',
        'fuel',
        'kpp',
        'priv',
        'kuzov',
        'grade',
        "year",
        'mileage',
        'eng_volume',
        'wheel_position',
        'images',
        'price_abroad',
        'price_in_russia',
        'rate',
        'finish',       
    )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "color": 
            kwargs["queryset"] = CarColor.objects.distinct('true_color')
        if db_field.name == 'priv':
            kwargs['queryset'] = CarPriv.objects.distinct('true_priv')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register((CarBody, CarCountry,  CarFuel,  CarMake,  KPP))
admin.site.register(Car,CarAdmin)
admin.site.register(CarColor, CarColorAdmin)



