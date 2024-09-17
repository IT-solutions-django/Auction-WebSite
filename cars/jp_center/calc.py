from datetime import datetime


def calc_price(price, currency, year, volume, table):
    try:
        # Инициализация переменных в зависимости от условий
        if table == "china":
            freight = 15000
            freight_vl = 0
            delivery = 0
            brokerServices = 110000
            compane_comision = 150000
            price += (35 * price) // 100
            one_rub = currency['cny'] / 100  # используем CNY для расчета
        elif table == "japan":
            freight_vl = 100000
            freight = 100000 if volume < 1900 else 400000
            delivery = 70000
            brokerServices = 78000
            compane_comision = 50000
            one_rub = currency['jpy'] / 100  # используем JPY для расчета
        else:
            raise ValueError("Неправильная таблица!")

        # Конвертация цены в рубли
        price_rus = round(price * one_rub)

        # Расчет TOF
        tof = calculate_tof(price_rus)

        # Вычисление возраста
        age = datetime.now().year - year

        # Вычисление YTS и пошлину
        yts, duty = calculate_yts_and_duty(age, volume, price_rus, currency['eur'])

        # Расчет окончательной стоимости
        toll = duty * currency['eur'] + tof
        res_rus = toll + yts + compane_comision + brokerServices
        res_jpn = (freight + delivery + freight_vl + price) * one_rub

        return round((res_jpn + res_rus) / 1000) * 1000, int(res_rus), int(res_jpn), toll
    except Exception as e:
        print(e)

def calculate_tof(price_rus):
    """Возвращает TOF в зависимости от цены."""
    if price_rus < 200000:
        return 775
    elif price_rus < 450000:
        return 1550
    elif price_rus < 1200000:
        return 3100
    elif price_rus < 2700000:
        return 8530
    elif price_rus < 4200000:
        return 12000
    elif price_rus < 5500000:
        return 15550
    elif price_rus < 7000000:
        return 20000
    elif price_rus < 8000000:
        return 23000
    elif price_rus < 9000000:
        return 25000
    elif price_rus < 10000000:
        return 27000
    else:
        return 30000

def calculate_yts_and_duty(age, volume, price_rus, eur_rate):
    """Вычисляет YTS и пошлину в зависимости от возраста и объема."""
    if age < 3:
        yts = calculate_yts_under_3(volume)
        duty = calculate_duty_under_3(price_rus, volume, eur_rate)
    elif 3 <= age < 5:
        yts = 1485000 if volume >= 3000 else 5200
        duty = calculate_duty_3_to_5(volume)
    else:  # age >= 5
        yts = 1485000 if volume >= 3000 else 5200
        duty = calculate_duty_above_5(volume)

    return yts, duty

def calculate_yts_under_3(volume):
    """Вычисляет YTS для возраста менее 3 лет."""
    if volume >= 3500:
        return 1235200
    elif volume >= 3000:
        return 970000
    else:
        return 3400

def calculate_duty_under_3(price_rus, volume, eur_rate):
    """Вычисляет пошлину для возраста менее 3 лет."""
    evroprice = price_rus / eur_rate
    duty_rates = [
        (8500, 0.54, 2.5),
        (16700, 0.48, 3.5),
        (42300, 0.48, 5.5),
        (84500, 0.48, 7.5),
        (169000, 0.48, 15),
        (float('inf'), 0.48, 20)
    ]
    for limit, rate, min_duty in duty_rates:
        if evroprice < limit:
            duty = evroprice * rate
            return max(duty, volume * min_duty)

def calculate_duty_3_to_5(volume):
    """Вычисляет пошлину для возраста от 3 до 5 лет."""
    if volume <= 1000:
        return volume * 1.5
    elif volume <= 1500:
        return volume * 1.7
    elif volume <= 1800:
        return volume * 2.5
    elif volume <= 2300:
        return volume * 2.7
    elif volume <= 3000:
        return volume * 3
    else:
        return volume * 3.6

def calculate_duty_above_5(volume):
    """Вычисляет пошлину для возраста старше 5 лет."""
    if volume <= 1000:
        return volume * 3
    elif volume <= 1500:
        return volume * 3.2
    elif volume <= 1800:
        return volume * 3.5
    elif volume <= 2300:
        return volume * 4.8
    elif volume <= 3000:
        return volume * 5
    else:
        return volume * 5.7