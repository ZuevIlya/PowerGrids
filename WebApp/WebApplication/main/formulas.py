import math
import random  # импортируем библиотеку для генерации случайных чисел
import statistics  # импортируем библиотеку для статистического анализа данных
import numpy as np  # импортируем библиотеку для работы с массивами
import warnings

from .models import Device


class Values(Device):
    voltage_phase_angle = 30  # угол фазы напряжения
    current_phase_angle = 10  # угол фазы тока
    current = 10  # сила тока
    voltage = 220  # напряжение
    resistance = 50.5  # Текущее значение сопротивления сети
    temperatures_mas = [23, 25, 27, 24, 23, 26, 22]  # задаем несколько значений температуры
    power_factor = 0.8  # фактический коэффициент мощности
    frequency = 59  # частота, Гц
    noise = 3.5  # уровень шума
    interference = 10  # уровень помех
    voltage_mas = [231, 232, 230, 230, 233, 231, 234, 235]  # Напряжения
    current_mas = [10, 12, 11, 10, 11, 9, 13, 12]  # Силы тока


# Тест 1
def phase_shift(voltage_phase_angle, current_phase_angle):
    phi = math.acos(
        math.cos(math.radians(voltage_phase_angle)) * math.cos(math.radians(current_phase_angle)) +
        math.sin(math.radians(voltage_phase_angle)) * math.sin(math.radians(current_phase_angle))
    )
    x = math.degrees(phi)

    # Пороговые значения для каждого критерия
    theta_normal = (0, 120)  # допустимый диапазон смещения фазы
    theta_warning = (120, 180)  # диапазон предупреждения об уровне фазы
    theta_crash = 180  # аварийное значение уровня фазы

    # Проверяем значения каждого критерия и выбираем действие
    if x < theta_normal[1] or x > theta_normal[0]:
        action1 = "Смещение фаз в допустимых пределах"
    elif x < theta_warning[1] or x > theta_warning[0]:
        action1 = "Предупреждение! Смещение фазы выше допустимого значения. Текущее смещение фазы: " + str(x) + "градусов"
    elif x > theta_crash:
        action1 = "Авария! Достигнуто пиковое значение смещения фазы: "+ str(x) + "градусов"

    # Вывод результата
    return action1


# Тест 2

# Симуляция работы электросети с использованием метода Монте-Карло
def simulate_network(current, voltage):
    load = current * voltage
    failures = 0
    num_trials = 100000
    for i in range(num_trials):
        # Генерируем случайные значения нагрузки и температуры окружающей среды
        load_simulated = np.random.normal(load, 50)

        # Оцениваем риск на основе данных о вероятностных распределениях для нагрузки и температуры окружающей среды
        if load_simulated > 4400:
            failures += 1

    failure_prob = failures / num_trials * 100

    # Выполнение симуляции и вывод результатов
    action2 = "Вероятность отказа при данных значениях нагрузки: " + str(failure_prob) + "% на основе 100000 проб"
    return action2


# Тест 3
def prob_failure(temperatures_mas):
    T_ambient = sum(temperatures_mas) / len(temperatures_mas)
    sigma_T = statistics.stdev(temperatures_mas)  # вычисляем стандартное отклонение температуры
    p_fail = 0.95  # задаем отказоустойчивость участка электросети

    n_trials = 1000000
    n_failures = 0  # считаем количество отказов

    for i in range(n_trials):
        T = random.gauss(T_ambient, sigma_T)  # генерируем случайную температуру
        p = 1 - (1 - p_fail) ** (T - T_ambient)  # рассчитываем вероятность отказа в зависимости от температуры
        if random.random() < p:
            n_failures += 1  # считаем отказы

    p_failure = n_failures / n_trials  # рассчитываем вероятность отказа
    action3 = "Вероятность отказа при данных показателях температуры:" + str(p_failure)  # выводим результат
    return action3


# Тест 4
def network_overload(current, voltage, power_factor):
    pf_max = 0.98  # максимальный коэффициент мощности, сделай его константой

    # вычисляем фактическую мощность потребления на узле
    w_actual = voltage * current * power_factor

    # вычисляем максимально допустимую мощность на узле
    w_max = voltage * current * pf_max

    # вычисляем отклонение от нормы
    deviation = (w_actual - w_max) / w_max * 100

    # анализируем причину перегрузки
    if deviation > 20:
        action4 = "Перегрузка связана с проблемами охлаждения оборудования или неполадками в работе насосов или холодильных систем"
    else:
        action4 = "Перегрузка связана со слишком большим количеством подключенных потребителей"
    return action4


# Тест 5
def network_frequency(frequency):
    permissible_error = (0.2 / 100) * frequency  # допустимая погрешность в Гц

    # Задаем критические значения частоты с учетом допустимой погрешности
    critical_freq_low = 49.8 - permissible_error  # нижнее критическое значение частоты
    critical_freq_high = 50.2 + permissible_error  # верхнее критическое значение частоты
    peak_freq = 50.5 + permissible_error  # пиковое значение частоты

    # Сравниваем текущее значение частоты с критическими значениями с учетом допустимой погрешности
    if frequency < critical_freq_low:
        action5 = "Предупреждение! Частота ниже допустимого значения. Текущая частота: " + str(frequency) + "Гц"
    elif frequency > critical_freq_high:
        if frequency > peak_freq:
            action5 = "Авария! Достигнуто пиковое значение частоты: "+ str(frequency) + "Гц"
        else:
            action5 = "Предупреждение! Частота выше допустимого значения. Текущая частота: "+ str(frequency) + "Гц"
    else:
        action5 = "Частота в пределах нормы. Текущая частота: "+ str(frequency) + "Гц"
    return action5


# Тест 6
def network_power(voltage, current):
    # Рассчитываем текущее значение мощности
    current_power = voltage * current  # Ватты

    # Задаем допустимую погрешность мощности как процент от текущего значения
    permissible_error = (5 / 100) * current_power

    # Задаем критические значения мощности с учетом допустимой погрешности
    critical_power_low = current_power - permissible_error
    critical_power_high = current_power + permissible_error
    peak_power = current_power + permissible_error + (
                10 / 100) * current_power  # пиковое значение мощности с учетом допустимой погрешности

    # Сравниваем текущее значение мощности с критическими значениями с учетом допустимой погрешности
    if current_power < critical_power_low:
        action6 = "Предупреждение! Мощность ниже допустимого значения. Текущая мощность: " + str(current_power) + "Ватт"
    elif current_power > critical_power_high:
        if current_power > peak_power:
            action6 = "Авария! Достигнуто пиковое значение мощности: " + str(current_power) + "Ватт"
        else:
            action6 = "Предупреждение! Мощность выше допустимого значения. Текущая мощность: " + str(current_power) + "Ватт"
    else:
        action6 = "Мощность в пределах нормы. Текущая мощность: " + str(current_power) + "Ватт"
    return action6


# Тест 7
def network_noise(noise, interference):
    # Вычисляем предельные значения с учетом погрешности
    allowed_noise = 3 * 1.1
    allowed_interference = 4 * 1.1

    # Сравниваем средние значения с допустимыми пределами и погрешностью
    if noise > allowed_noise:
        percent_error = (noise - allowed_noise) / allowed_noise * 100
        string1 = f"Предупреждение: Средний уровень шума превышает предел на {percent_error:.2f}%"
    else:
        string1 = f"Уровень шума в пределах нормы"
    if interference > allowed_interference:
        percent_error = (interference - allowed_interference) / allowed_interference * 100
        string2 = f"Предупреждение: Средний уровень помех превышает предел на {percent_error:.2f}%"
    else:
        string2 = f"Уровень помех в пределах нормы"
    action7 = string1 + ". " + string2
    return action7


# Тест 8
def network_cur_volt(voltage_mas, current_mas):
    # Рассчитаем среднее значение и стандартное отклонение для напряжения и тока
    mean_voltage = sum(voltage_mas) / len(voltage_mas)
    mean_current = sum(current_mas) / len(current_mas)

    std_voltage = ((1 / (len(voltage_mas) - 1)) * sum([(i - mean_voltage) ** 2 for i in voltage_mas])) ** 0.5
    std_current = ((1 / (len(current_mas) - 1)) * sum([(i - mean_current) ** 2 for i in current_mas])) ** 0.5

    # Зададим верхние и нижние пределы для напряжения и тока
    upper_voltage = mean_voltage + 2 * std_voltage
    lower_voltage = mean_voltage - 2 * std_voltage

    upper_current = mean_current + 2 * std_current
    lower_current = mean_current - 2 * std_current

    # Проверяем каждое значение на превышение допустимых пределов
    string1 = ""
    string2 = ""
    for v in voltage_mas:
        if v > upper_voltage or v < lower_voltage:
            string1 = f"Предупреждение: Уровень напряжения вышел за допустимый предел: {v}В"
            break
    for c in current_mas:
        if c > upper_current or c < lower_current:
            string2 = f"Предупреждение: Уровень тока вышел за допустимый предел: {c}А"
            break
    if (string1 == "") or (string2 == ""):
        action8 = f"Уровень напряжения и силы тока в допустимых пределах"
        return action8
    else:
        action8 = string1 + ". " + string2
        return action8


# Тест 9
def analyze_network(resistance):
    """
    Функция анализа электрической сети.
    Проверяет, находится ли сопротивление сети в заданных пределах
    (с учетом погрешности от текущего значения).
    В случае, когда сопротивление выходит за пределы безопасности,
    функция выдает предупреждающее либо аварийное сообщение.
    """
    error_percentage = 0.1
    error_value = resistance * error_percentage / 100
    min_resistance = resistance - error_value  # минимальное допустимое сопротивление с учетом погрешности
    max_resistance = resistance + error_value  # максимальное допустимое сопротивление с учетом погрешности
    critical_value = resistance + error_value * 2  # критическое значение (следует учесть ограничения допустимой нагрузки)

    if resistance < min_resistance:
        action9 = "Предупреждение! Сопротивление сети ниже допустимого значения. Текущее сопротивление: {:.2f} Ом, допустимое значение: {:.2f} - {:.2f} Ом".format(
            resistance, min_resistance, max_resistance)
    elif resistance > critical_value:
        action9 = "Авария! Сопротивление сети превысило критическое значение. Текущее сопротивление: {:.2f} Ом, критическое значение: {:.2f} Ом".format(
            resistance, critical_value)
    elif resistance > max_resistance:
        action9 = "Предупреждение! Сопротивление сети превышает допустимое значение. Текущее сопротивление: {:.2f} Ом, допустимое значение: {:.2f} - {:.2f} Ом".format(
            resistance, min_resistance, max_resistance)
    else:
        action9 = "Сопротивление сети в пределах нормы. Текущее сопротивление: {:.2f} Ом".format(resistance)
    return action9
