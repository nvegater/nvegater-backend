from django.urls import path

from . import views


urlpatterns = [
    path('', views.ingredients_all, name="ingredients"),
    path('upload-csv/', views.csv_upload, name="csv_upload")
]