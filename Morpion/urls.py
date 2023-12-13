"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from . import views

urlpatterns = [
    path('', views.partie, name="partie"),
    path('invitations', views.invitation, name="invitations"),
    path('notifications', views.notification, name="notifications"),
    path('statistiques', views.statistique, name="statistiques"),
    path('profil', views.profil, name="profil"),
    path('signin', views.signIn, name="signin"),
    path('signup', views.signUp, name="signup"),
 
]
