import django_filters
from cars.models import Car
from jp_center.models import FrontCar

class CarFilter(django_filters.FilterSet):
    make = django_filters.CharFilter(method='filter_make', label="Марка")
    
    model = django_filters.CharFilter(
        method='filter_model', label="Модель"
    )
    priv = django_filters.CharFilter(
        method='filter_priv', label="Привод"
    )
    kpp = django_filters.CharFilter(
        method='filter_kpp', label="КПП", field_name='kpp'
    )
    color = django_filters.CharFilter(method='filter_color',label='Цвет')
    
    mileage_min = django_filters.NumberFilter(
        field_name="mileage", lookup_expr="gte", label="Пробег от"
    )
    mileage_max = django_filters.NumberFilter(
        field_name="mileage", lookup_expr="lte", label="Пробег до"
    )
    year_min = django_filters.NumberFilter(
        field_name="year", lookup_expr="gte", label="Год от"
    )
    year_max = django_filters.NumberFilter(
        field_name="year", lookup_expr="lte", label="Год до"
    )
    price_min = django_filters.NumberFilter(
        field_name="finish", lookup_expr="gte", label="Цена от"
    )
    price_max = django_filters.NumberFilter(
        field_name="finish", lookup_expr="lte", label="Цена до"
    )
    power_min = django_filters.NumberFilter(field_name='pw', lookup_expr='gte', label='Мощность от')
    power_max = django_filters.NumberFilter(field_name='pw', lookup_expr='lte', label='Мощность до')
    
    volume_min = django_filters.NumberFilter(
        label="Объем от",
        lookup_expr='gte',
        field_name ='eng_volume'
    )
    volume_max = django_filters.NumberFilter(
        label="Объем до",
        lookup_expr='lte',
        field_name ='eng_volume'
    )

    class Meta:
        model = Car
        fields = ["make", "model", "priv", "kpp", "color",'power_min','power_max','finish','year_min','year_max','volume_min','volume_max','price_min','price_max']

    def filter_make(self, queryset, name, value):
        return queryset.filter(make__name__iexact=value)
    
    def filter_model(self, queryset, name, value):
        return queryset.filter(model__name__iexact=value)

    def filter_priv(self, queryset, name, value):
        return queryset.filter(priv__true_priv__contains=value)
    
    def filter_kpp(self, queryset, name, value):
        return queryset.filter(kpp__true_kpp__iexact=value)
    
    def filter_color(self, queryset, name, value):
        return queryset.filter(color__true_color__iexact=value)


class MainPageFilter(django_filters.FilterSet):
    country = django_filters.ChoiceFilter(choices = [
        ('Япония','Япония'),
        ('Корея','Корея'),
        ('Китай','Китай')
    ],field_name='export_country',label='Страна')

    class Meta:
        model = FrontCar
        fields = ['country']