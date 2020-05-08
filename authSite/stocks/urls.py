from django.urls import path

from . import views


urlpatterns = [
    path('', views.stock_all, name="stocks"),
    path('upload-csv/', views.csv_upload, name="csv_upload")
]