"""RestraVer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restroapp import views

 

urlpatterns = [
    path('' , views.index),
    path('login' , views.login),
    path('logout' , views.signout),
    path('register' , views.register),
    path('doctor' , views.doctordash),
    path('pwdchange' , views.changepassword , name='changepwd'),
    path('doctor/appointments' , views.docappointments),
    path('patient' , views.patientdash),
    path('doctor/profile' , views.doctorset),
    path('patient-settings' , views.patientset),
    path('search' , views.search),
    path('book' , views.book),
    path('checkout' , views.bookSuccess),
]


