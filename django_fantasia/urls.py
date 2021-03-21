import os
from pathlib import Path

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

BASE_DIR = Path(__file__).resolve().parent.parent


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fantasia.urls')),
]
urlpatterns += static('/media/', document_root=os.path.join(BASE_DIR, 'media'))
urlpatterns += staticfiles_urlpatterns()