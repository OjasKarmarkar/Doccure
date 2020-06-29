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
from apis import urls
from django.conf import settings
from restroapp import urls as mainurls
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' , include(urls)),
    path('' , include(mainurls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
