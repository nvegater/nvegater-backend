from django.urls import path, include

from . import views

#  http://127.0.0.1:8001/authapp/token/login/
#  https://djoser.readthedocs.io/en/latest/token_endpoints.html#token-create

urlpatterns = [
    path('checkServer/', views.server_status, name='server_status'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
