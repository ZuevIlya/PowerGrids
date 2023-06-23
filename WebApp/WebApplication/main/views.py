import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import json
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginUserForm
from .formulas import *
from .models import Device, Station, Decision


# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def dopInfo(request):
    return render(request, 'main/dopInfo.html')


def jsonPOST(request):
    if request.method == 'POST':

        # Запись данных из JSON файла в словарь
        jsonvalues = json.loads(request.body)
        data = {
            'title': jsonvalues['title'],
            'id_station': jsonvalues['id_station'],
            'type': jsonvalues['type'],
            'maker': jsonvalues['maker'],
            'data': jsonvalues['data'],
            'voltage': jsonvalues['voltage'],
            'current': jsonvalues['current'],
            'power_factor': jsonvalues['power_factor'],
            'frequency': jsonvalues['frequency'],
            'noise': jsonvalues['noise'],
            'interference': jsonvalues['interference'],
            'voltage_phase_angle': jsonvalues['voltage_phase_angle'],
            'current_phase_angle': jsonvalues['current_phase_angle'],
            'resistance': jsonvalues['resistance'],
            'temperature': jsonvalues['temperature'],
        }

        # Запись нового прибора в базу данных
        try:
            device = Device.objects.create(
                title=data.get('title'),
                id_station=Station.objects.get(pk=data.get('id_station')),
                type=data.get('type'),
                maker=data.get('maker'),
                data=data.get('data'),
                voltage=data.get('voltage'),
                current=data.get('current'),
                power_factor=data.get('power_factor'),
                frequency=data.get('frequency'),
                noise=data.get('noise'),
                interference=data.get('interference'),
                voltage_phase_angle=data.get('voltage_phase_angle'),
                current_phase_angle=data.get('current_phase_angle'),
                resistance=data.get('resistance'),
                temperature=data.get('temperature'),
            )
        except ObjectDoesNotExist:
            device = None

        return redirect('/json', data)
    return render(request, 'main/json.html')

# Вывод всех приборов на главную страницу
def deviceOut(request):
    devices = Device.objects.all()
    return render(request, 'main/index.html', {'devices': devices})


def formulas(request, device_id):
    # Получение переменных из базы данных
    device = Device.objects.get(id=device_id)
    voltage = device.voltage
    current = device.current
    power_factor = device.power_factor
    frequency = device.frequency
    noise = device.noise
    interference = device.interference
    voltage_phase_angle = device.voltage_phase_angle
    current_phase_angle = device.current_phase_angle
    resistance = device.resistance

    # Сохранение в список всех приборов с выбранной станции
    list1 = Device.objects.filter(id_station=device.id_station)
    voltage_mas = []
    current_mas = []
    temperatures_mas = []
    for item in list1:
        voltage_mas.append(item.voltage)
        current_mas.append(item.current)
        temperatures_mas.append(item.temperature)


    # Создание словаря со всеми результатами формул
    results = {
        'phase_shift': phase_shift(voltage_phase_angle, current_phase_angle),
        'simulate_network': simulate_network(current, voltage),
        'prob_failure': prob_failure(temperatures_mas),
        'network_overload': network_overload(current, voltage, power_factor),
        'network_frequency': network_frequency(frequency),
        'network_power': network_power(voltage, current),
        'network_noise': network_noise(noise, interference),
        'network_cur_volt': network_cur_volt(voltage_mas, current_mas),
        'analyze_network': analyze_network(resistance),
    }
    counter = 0
    # Запись всех новых решений в базу данных
    for i in results:
        decision = Decision.objects.create(
            title='Решение по параметрам',
            id_station=Station.objects.get(pk=device.id_station.id),
            data=str(datetime.datetime.now()),
            type=list(results.keys())[counter],
            description=list(results.values())[counter]
        )
        counter = counter + 1

    # Создание JSON объекта
    send_json = results
    send_json['title'] = 'Результат тестирования системы'
    send_json['id_station'] = device.id_station.id
    with open("data_file.json", "w") as write_file:
        json.dump(send_json, write_file, ensure_ascii=False, indent=4)

    return render(request, 'main/formulas.html', {'results': results})


class DataMixin:
    paginate_by = 2


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

