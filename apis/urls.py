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
from django.urls import path , include
from apis import views
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('login' , views.UserLoginView.as_view() , name = 'login'),
    path('register' , views.UserRegisterView.as_view() , name = 'register'),
    path('doctor_dashboard' , views.DoctorDashboard.as_view() , name = 'doctor-dash'),
    path('patient_dashboard' , views.PatientDashboard.as_view() , name = 'patient-dash'),
    path('search' , views.Search.as_view() , name = 'search'),
    path('get-token', obtain_auth_token, name='token'),
]
