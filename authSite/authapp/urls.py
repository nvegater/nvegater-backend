from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_auth, name='home_auth'),
]
