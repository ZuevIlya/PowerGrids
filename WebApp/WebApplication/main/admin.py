from django.contrib import admin
from .models import Station, Device, Decision, Directory, Statistic

# Register your models here.

admin.site.register(Station)
admin.site.register(Device)
admin.site.register(Decision)
admin.site.register(Directory)
admin.site.register(Statistic)
