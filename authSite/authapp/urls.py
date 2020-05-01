from django.urls import path, include

from . import views

urlpatterns = [
    path('checkServer/', views.server_status, name='server_status'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
   # path('company/', views.companyApi),
]
