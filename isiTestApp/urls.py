
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from isiTestApp.chat import views

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('api/v1/chat/', include('isiTestApp.chat.urls')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token')
]
