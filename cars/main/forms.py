from django import forms
from cars.models import CarMake, CarPriv, CarColor, KPP
from jp_center.models import CarModel
from main.models import YearFilter,PowerFilter,VolumeFilter,MileageMaxFilter,MileageMinFilter


class CarFilterForm(forms.Form):
    make = forms.ModelChoiceField(
        queryset=CarMake.objects.all(),  
        required=False,
        empty_label="Выберите марку",  
    )
    # model = forms.CharField(required=False)
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(), required=False, empty_label="Выберите модель"
    )
    priv = forms.ChoiceField(
        required=False,
    )
    kpp = forms.ChoiceField(
        required=False,
    )
    volume_min = forms.ChoiceField(
        required=False,
        label="Объем от",
    )

    volume_max = forms.ChoiceField(
        required=False,
        label="Объем до",
    )
    color = forms.ChoiceField(
        required=False,
        label="Цвет",
    )
    mileage_min = forms.ChoiceField(
        choices=[
            ("", "Выберите"),
            (1000, "1000km"),
            (5000, "5000km"),
            (10_000, "10000km"),
            (20_000, "20000km"),
            (50_000, "50000km"),
            (100_000, "100000km"),
        ],
        required=False,
        label="Пробег от",
    )
    mileage_max = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Выберите"),
            (30_000, "30000km"),
            (40_000, "40000km"),
            (50_000, "50000km"),
            (60_000, "60000km"),
            (70_000, "70000km"),
            (80_000, "80000km"),
            (100_000, "100000km"),
            (150_000, "150000km"),
            (200_000, "200000km"),
            (250_000, "250000km"),
        ],
        label="Пробег до",
    )
    power_min = forms.ChoiceField(
        required=False,
        label="Мощность от",
    )
    power_max = forms.ChoiceField(
        required=False,
        label="Мощность до",
    )
    price_min = forms.FloatField(required=False, label="Цена от")
    price_max = forms.FloatField(required=False, label="Цена до")
    year_min = forms.ChoiceField(required=False, label="Год от")
    year_max = forms.ChoiceField(required=False, label="Год до")

    def __init__(self, *args, **kwargs):
        """Реюзаем модельки, которые уже подходят и вынесены в админку"""
        super(CarFilterForm,self).__init__(*args, **kwargs)

        choices_map = {
            'color': (CarColor, 'true_color', 'Цвет не найден'),
            'priv': (CarPriv, 'true_priv', ''),
            'kpp': (KPP, 'true_kpp', ''),
            'volume_min': (VolumeFilter,),
            'volume_max': (VolumeFilter,),
            'year_min': (YearFilter,),
            'year_max': (YearFilter,),
            'power_min': (PowerFilter,),
            'power_max': (PowerFilter,),
            'mileage_min': (MileageMinFilter,),
            'mileage_max': (MileageMaxFilter,)
        }
        for field, model_info in choices_map.items():
            if field in ['color','priv','kpp']:
                model_class, field_name, exclude_name = model_info
                self.fields[field].choices = self._get_choices(model_class, field_name, exclude_name)
            else:
                self.fields[field].choices = self._get_choices_filterclasses(model_info[0])

        """Пробежались по словарику и накидали choices в поля"""
        

    

    def _get_choices(self, model_class, field_name, exclude_name=None):
        """Получаем выборки для значений с true значениями"""
        if exclude_name:
            choices = [
                (str(getattr(item, field_name)), str(getattr(item, field_name)))
                for item in model_class.objects.exclude(name=exclude_name).distinct(field_name)
            ]
        else:
            choices = [
                (str(getattr(item, field_name)), str(getattr(item, field_name)))
                for item in model_class.objects.distinct(field_name)
            ]
        
        choices.insert(0, ('', 'Выберите'))
        return choices
    
    def _get_choices_filterclasses(self, model_class):
        """Получаем выборки для специально созданных фильтрклассов"""
        choices = [
            (item.value , str(getattr(item, 'name'))) for item in model_class.objects.distinct('value')
        ]
        choices.insert(0,('','Выберите'))

        return choices
