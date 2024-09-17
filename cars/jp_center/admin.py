from django.contrib import admin
from .models import CarModel, FrontCar,Image,CarContainer
from cars.models import CarPriv, KPP,CarColor


admin.site.register(Image)
admin.site.register(CarContainer)



@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'make')
    list_filter = ('make',)

@admin.register(FrontCar)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'make',
        'model',
        'privod',
        'kpp',
        'color',
        'pw',
        'export_country',
        'body_type',
        'year',
        'final',
        'price_abroad',
        'price_in_russia',
        
    )
    class Media:
        js = ('js/admin/car_admin.js',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "color": 
            kwargs["queryset"] = CarColor.objects.exclude(true_color = 'Цвет не найден').distinct('true_color')
        if db_field.name == 'privod':
            kwargs['queryset'] = CarPriv.objects.exclude(name = '').distinct('true_priv')
        if db_field.name == 'kpp':
            kwargs['queryset'] = KPP.objects.distinct('true_kpp')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        