from django.contrib.auth import login
from django.urls import path
from . import views
from .views import RegisterUser, LoginUser, logout_user

urlpatterns = [
    path('', views.deviceOut, name='home'),
    path('about', views.about, name='about'),
    path('dopInfo', views.dopInfo, name='dopInfo'),
    path('json', views.jsonPOST, name='json'),
    path('formulas/<int:device_id>', views.formulas, name='formulas'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]