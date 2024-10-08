from django import forms
from cars.models import CarMake, CarPriv, CarColor, KPP
from jp_center.models import CarModel


class CarFilterForm(forms.Form):
    # make = forms.CharField(required=False)
    make = forms.ModelChoiceField(
        queryset=CarMake.objects.all(),  # Получаем все записи из CarMake
        required=False,
        empty_label="Выберите марку",  # Параметр для отображения пустого значения
    )
    # model = forms.CharField(required=False)
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(), required=False, empty_label="Выберите модель"
    )
    privod = forms.ChoiceField(
        choices=[
            ("", "Выберите"),
            ("Передний привод", "Передний"),
            ("Задний привод", "Задний"),
            ("Полный привод", "Полный"),
        ],
        required=False,
    )
    kpp = forms.ChoiceField(
        choices=[
            ("", "Выберите"),
            ("Механика", "Механика"),
            ("Автомат", "Автомат"),
        ],
        required=False,
    )
    volume_min = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Выберите"),
            (700, "0.7"),
            (800, "0.8"),
            (1000, "1"),
            (1100, "1.1"),
            (1200, "1.2"),
            (1300, "1.3"),
            (1400, "1.4"),
            (1500, "1.5"),
            (1600, "1.6"),
            (1700, "1.7"),
            (1800, "1.8"),
            (1900, "1.9"),
            (2000, "2"),
            (2200, "2.2"),
            (2300, "2.3"),
            (2400, "2.4"),
            (2500, "2.5"),
            (2700, "2.7"),
            (2800, "2.8"),
            (3000, "3"),
            (3200, "3.2"),
            (3300, "3.3"),
            (3500, "3.5"),
            (3600, "3.6"),
            (4000, "4"),
            (4200, "4.2"),
            (4400, "4.4"),
            (4500, "4.5"),
            (4600, "4.6"),
            (4700, "4.7"),
            (5000, "5"),
            (5500, "5.5"),
            (5700, "5.7"),
            (6000, "6"),
        ],
        label="Объем от",
    )

    volume_max = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Выберите"),
            (700, "0.7"),
            (800, "0.8"),
            (1000, "1"),
            (1100, "1.1"),
            (1200, "1.2"),
            (1300, "1.3"),
            (1400, "1.4"),
            (1500, "1.5"),
            (1600, "1.6"),
            (1700, "1.7"),
            (1800, "1.8"),
            (1900, "1.9"),
            (2000, "2"),
            (2200, "2.2"),
            (2300, "2.3"),
            (2400, "2.4"),
            (2500, "2.5"),
            (2700, "2.7"),
            (2800, "2.8"),
            (3000, "3"),
            (3200, "3.2"),
            (3300, "3.3"),
            (3500, "3.5"),
            (3600, "3.6"),
            (4000, "4"),
            (4200, "4.2"),
            (4400, "4.4"),
            (4500, "4.5"),
            (4600, "4.6"),
            (4700, "4.7"),
            (5000, "5"),
            (5500, "5.5"),
            (5700, "5.7"),
            (6000, "6"),
        ],
        label="Объем до",
    )
    color = forms.ChoiceField(
        choices=[
            ("", "Выберите"),
            ("Белый", "Белый"),
            ("Бежевый", "Бежевый"),
            ("Бирюзовый", "Бирюзовый"),
            ("Бордовый", "Бордовый"),
            ("Желтый", "Желтый"),
            ("Зеленый", "Зеленый"),
            ("Золотой", "Золотой"),
            ("Индиго", "Индиго"),
            ("Кораловый", "Кораловый"),
            ("Коричневый", "Коричневый"),
            ("Красный", "Красный"),
            ("Кремовый", "Кремовый"),
            ("Лиловый", "Лиловый"),
            ("Мятный", "Мятный"),
            ("Оливковый", "Оливковый"),
            ("Оранжевый", "Оранжевый"),
            ("Персиковый", "Персиковый"),
            ("Пурпурный", "Пурпурный"),
            ("Розовый", "Розовый"),
            ("Серебристый", "Серебристый"),
            ("Серый", "Серый"),
            ("Синий", "Синий"),
            ("Темно-синий", "Темно-синий"),
            ("Угольный", "Угольный"),
            ("Фиолетовый", "Фиолетовый"),
            ("Черный", "Черный"),
            ("Шоколадный", "Шоколадный"),
        ],
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
        choices=[
            ("", "Выберите"),
            (50, "50"),
            (75, "75"),
            (100, "100"),
            (125, "125"),
            (150, "150"),
            (175, "175"),
            (200, "200"),
            (225, "225"),
            (250, "250"),
            (275, "275"),
            (300, "300"),
        ],
        label="Мощность от",
    )
    power_max = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Выберите"),
            (50, "50"),
            (75, "75"),
            (100, "100"),
            (125, "125"),
            (150, "150"),
            (175, "175"),
            (200, "200"),
            (225, "225"),
            (250, "250"),
            (275, "275"),
            (300, "300"),
        ],
        label="Мощность до",
    )
    price_min = forms.FloatField(required=False, label="Цена от")
    price_max = forms.FloatField(required=False, label="Цена до")
    year_min = forms.ChoiceField(required=False,choices=[
        ('','Выберите'),
        (2008,'2008'),
        (2009,'2009'),
        (2010,'2010'),
        (2011,'2011'),
        (2012,'2012'),
        (2013,'2013'),
        (2014,'2014'),
        (2015,'2015'),
        (2016,'2016'),
        (2017,'2017'),
        (2018,'2018'),
        (2019,'2019'),
        (2020,'2020'),
        (2021,'2021'),
        (2022,'2022'),
        (2023,'2023'),
        (2024,'2024')
    ], label="Год от")
    year_max = forms.ChoiceField(required=False,choices=[
        ('', 'Выберите'),
        (2008,'2008'),
        (2009,'2009'),
        (2010,'2010'),
        (2011,'2011'),
        (2012,'2012'),
        (2013,'2013'),
        (2014,'2014'),
        (2015,'2015'),
        (2016,'2016'),
        (2017,'2017'),
        (2018,'2018'),
        (2019,'2019'),
        (2020,'2020'),
        (2021,'2021'),
        (2022,'2022'),
        (2023,'2023'),
        (2024,'2024')
    ], label="Год до")
