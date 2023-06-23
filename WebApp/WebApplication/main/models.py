from django.db import models


# Create your models here.


# Станция
class Station(models.Model):
    title = models.CharField('title', max_length=250)
    address = models.CharField('address', max_length=250)
    coordinates = models.CharField('coordinates', max_length=250, default=0)

    def _str_(self):
        return self.title


# Прибор
class Device(models.Model):
    title = models.CharField('title', max_length=250)
    id_station = models.ForeignKey(Station, verbose_name='id станции', on_delete=models.CASCADE, default=0)
    type = models.CharField('type', max_length=250)
    maker = models.CharField('maker', max_length=250)
    data = models.CharField('data', max_length=250)
    voltage = models.FloatField('Напряжение в сети (вольты)', max_length=250)
    current = models.FloatField('Ток потребления (амперы)', max_length=250)
    power_factor = models.FloatField('Коэффициент мощности (безразмерный параметр)', max_length=250)
    frequency = models.FloatField('Частота тока (герцы)', max_length=250)
    noise = models.FloatField('Уровень шума в сети (дБ)', max_length=250)
    interference = models.FloatField('Уровень помех в сети (дБ)', max_length=250, default=0)
    voltage_phase_angle = models.FloatField('Фазный угол напряжения (градусы)', max_length=250, default=0)
    current_phase_angle = models.FloatField('Фазный угол тока (градусы)', max_length=250, default=0)
    resistance = models.FloatField('Сопротивление проводов и кабелей (омы)', max_length=250)
    temperature = models.FloatField('Температура окружающей среды и оборудования (градусы Цельсия)', max_length=250)

    def _str_(self):
        return self.title


# Решение
class Decision(models.Model):
    title = models.CharField('title', max_length=250)
    id_station = models.ForeignKey(Station, verbose_name='id станции', on_delete=models.CASCADE, default=0)
    data = models.CharField('data', max_length=250)
    type = models.CharField('type', max_length=250)
    description = models.CharField('description', max_length=250)

    def _str_(self):
        return self.title


# Журнал
class Directory(models.Model):
    title = models.CharField('title', max_length=250)
    id_decision = models.ForeignKey(Decision, verbose_name='id решения', on_delete=models.CASCADE, default=0)
    data = models.CharField('data', max_length=250)
    description = models.CharField('description', max_length=250)

    def _str_(self):
        return self.title

# Статистика
class Statistic(models.Model):
    title = models.CharField('title', max_length=250)
    id_device = models.ForeignKey(Device, verbose_name="id прибора", on_delete=models.CASCADE, default=0)
    data = models.CharField('data', max_length=250)
    value = models.FloatField('value', max_length=250)

