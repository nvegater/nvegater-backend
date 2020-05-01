from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('authapp/', include('authapp.urls')),
    path('admin/', admin.site.urls),
]
