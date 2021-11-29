"""mydatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from database_app import views
from django.views.static import serve

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', views.login),
    path("home/", views.home),
    path('register/', views.register),
    path('loginout/', views.loginout),
    path('index/', views.index),
    path('schedule/', views.Schedule),
    path('photo/', views.Photo),
    path('usertext/', views.Usertext),
    path('test/', views.ajax_add),
    path('handle/', views.handle),
    path('del/', views.delete),
    path('homepage/', views.homepage),
    path('photo_view/', views.photo_view),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'^captcha$', include('captcha.urls'))
]
