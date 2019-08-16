from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include('api_v1.urls'))
]