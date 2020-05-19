from django.urls import path
from graphene_django.views import GraphQLView
from . import views


urlpatterns = [
    path('', views.ingredients_all, name="ingredients"),
    path('upload-csv/', views.csv_upload, name="csv_upload"),
    path('graphql', GraphQLView.as_view(graphiql=True)),
]