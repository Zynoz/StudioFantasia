from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('fantasia/', include('fantasia.urls')),
    path('admin/', admin.site.urls),
]